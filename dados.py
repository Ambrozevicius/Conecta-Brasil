#Salva e consulta os dados das contagens
import json
import math
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID, uuid4

RAIZ = Path(__file__).resolve().parent
ROTULOS = {"empty": "Sem pessoas detectadas", "low": "Baixa", "moderate": "Moderada",
           "high": "Alta", "very_high": "Muito alta", "unavailable": "Indisponível"}


def agora_utc():
    return datetime.now(timezone.utc)


def instante(texto):
    valor = datetime.fromisoformat(texto)
    if valor.tzinfo is None:
        raise ValueError("Timestamp precisa incluir timezone.")
    return valor.astimezone(timezone.utc)


def numero(valor):
    return type(valor) in (int, float) and math.isfinite(valor)


def classificar(contagem):
    if contagem is None:
        return "unavailable"
    if type(contagem) is not int or contagem < 0:
        raise ValueError("Contagem deve ser um inteiro não negativo ou null.")
    if contagem == 0:
        return "empty"
    elif contagem <= 2:
        return "low"
    elif contagem == 3:
        return "moderate"
    elif contagem <= 5:
        return "high"
    return "very_high"


def carregar_config(caminho=RAIZ / "config.json"):
    config = json.loads(Path(caminho).read_text(encoding="utf-8"))
    try:
        for chave in ("project_name", "area_id", "area_name"):
            if not isinstance(config[chave], str) or not config[chave].strip():
                raise ValueError(f"{chave} deve ser texto não vazio.")
        if config["environment"] != "demo" or config["threshold_version"] != "demo-v1":
            raise ValueError("Este piloto usa environment demo e threshold_version demo-v1.")
        roi = config["roi"]
        if (not isinstance(roi, list) or len(roi) != 4 or
                not all(numero(v) and 0 <= v <= 1 for v in roi) or
                not (roi[0] < roi[2] and roi[1] < roi[3])):
            raise ValueError("roi: esperado [x1,y1,x2,y2], ordenado entre 0 e 1.")
        for chave in ("camera_index", "frame_width", "frame_height", "image_size"):
            minimo = 0 if chave == "camera_index" else 1
            if type(config[chave]) is not int or config[chave] < minimo:
                raise ValueError(f"{chave}: inteiro >= {minimo} obrigatório.")
        if config["image_size"] % 32:
            raise ValueError("image_size deve ser múltiplo de 32.")
        if not numero(config["confidence"]) or not 0 < config["confidence"] <= 1:
            raise ValueError("confidence deve estar entre 0 (exclusivo) e 1.")
        if config["model"] != "yolo11n.pt" or config["device"] not in ("cpu", "cuda:0"):
            raise ValueError("Use yolo11n.pt e device cpu (ou cuda:0 explicitamente).")
        if not numero(config["record_interval_seconds"]) or config["record_interval_seconds"] <= 0:
            raise ValueError("Intervalo deve ser positivo.")
    except (KeyError, TypeError) as erro:
        raise ValueError(f"Configuração incompleta ou inválida: {erro}") from erro
    return config


def criar_leitura(config, contagem, horario=None):
    status = classificar(contagem)
    return {"reading_id": str(uuid4()), "area_id": config["area_id"],
            "measured_at": (horario or agora_utc()).isoformat(), "source": "camera",
            "environment": config["environment"], "people_count": contagem,
            "quality": "camera_error" if contagem is None else "ok",
            "threshold_version": config["threshold_version"], "occupancy_status": status,
            "forecast_10min": None,
            "forecast_status": "unavailable" if contagem is None else "insufficient_history",
            "forecast_method": None}


def validar_leitura(leitura):
    UUID(leitura["reading_id"])
    instante(leitura["measured_at"])
    contagem = leitura["people_count"]
    if leitura["occupancy_status"] != classificar(contagem):
        raise ValueError("Faixa incompatível com contagem.")
    if leitura["quality"] != ("camera_error" if contagem is None else "ok"):
        raise ValueError("Qualidade incompatível com contagem.")
    for chave in ("area_id", "environment", "threshold_version"):
        if not isinstance(leitura[chave], str) or not leitura[chave]:
            raise ValueError(f"{chave} inválido.")
    if leitura["source"] != "camera":
        raise ValueError("Fonte inválida.")
    previsao = leitura["forecast_10min"]
    estado = leitura["forecast_status"]
    metodo = leitura["forecast_method"]
    if previsao is not None:
        if (not numero(previsao) or previsao < 0 or estado != "ok" or
                metodo != "linear_recent_window_v1" or contagem is None):
            raise ValueError("Projeção inválida.")
    elif estado not in ("insufficient_history", "stale", "unavailable", "invalid_fit") or metodo is not None:
        raise ValueError("Estado de projeção inválido.")
    if contagem is None and estado != "unavailable":
        raise ValueError("Câmera inválida exige previsão indisponível.")
    json.dumps(leitura, allow_nan=False)


def nova_sessao(config):
    return {"session_id": str(uuid4()), "started_at": agora_utc().isoformat(),
            "config": config.copy(), "readings": []}


def salvar_sessao(sessao, pasta):
    pasta = Path(pasta)
    UUID(sessao["session_id"])
    for leitura in sessao["readings"]:
        validar_leitura(leitura)
    conteudo = json.dumps(sessao, ensure_ascii=False, indent=2, allow_nan=False)
    pasta.mkdir(parents=True, exist_ok=True)
    destino = pasta / (sessao["session_id"] + ".json")
    temporario = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=pasta,
                                         suffix=".tmp", delete=False) as arquivo:
            temporario = Path(arquivo.name)
            arquivo.write(conteudo)
            arquivo.flush()
            os.fsync(arquivo.fileno())
        os.replace(temporario, destino)
    finally:
        if temporario is not None:
            temporario.unlink(missing_ok=True)
    return destino


def compativel(leitura, config):
    return all(leitura.get(chave) == config[chave]
               for chave in ("area_id", "environment", "threshold_version"))


def registrar_leitura(sessao, config, contagem):
    leitura = criar_leitura(config, contagem)
    sessao["readings"].append(leitura)
    return salvar_sessao(sessao, RAIZ / "data")


def estatisticas(leituras, config):
    validas = []
    for leitura in leituras:
        try:
            validar_leitura(leitura)
            if (compativel(leitura, config) and leitura["quality"] == "ok"
                    and instante(leitura["measured_at"]) <= agora_utc()):
                validas.append(leitura)
        except (ValueError, KeyError, TypeError, AttributeError):
            continue
    contagens = [leitura["people_count"] for leitura in validas]
    return {"quantidade": len(validas),
            "media": sum(contagens) / len(contagens) if contagens else None,
            "maior": max(contagens) if contagens else None,
            "ultima": max((l["measured_at"] for l in validas), key=instante) if validas else None}


def carregar_historico(config, pasta=RAIZ / "data", avisar=print):
    leituras = []
    for caminho in sorted(Path(pasta).glob("*.json")):
        try:
            sessao = json.loads(caminho.read_text(encoding="utf-8"))
            lote = sessao["readings"]
            if not isinstance(lote, list):
                raise ValueError("readings deve ser lista.")
            for leitura in lote:
                validar_leitura(leitura)
            leituras.extend(l for l in lote if compativel(l, config))
        except (OSError, ValueError, KeyError, TypeError, AttributeError) as erro:
            avisar(f"Histórico ignorado e preservado: {caminho}: {erro}")
    return sorted(leituras, key=lambda l: instante(l["measured_at"]))
