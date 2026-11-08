#Detecta pessoas na imagem com o YOLO
import os
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
_modelo = None


def carregar_modelo(nome="yolo11n.pt"):
    global _modelo
    if _modelo is None:
        os.environ.setdefault("YOLO_CONFIG_DIR", str(RAIZ / ".cache" / "ultralytics"))
        from ultralytics import YOLO
        pasta = RAIZ / "models"
        pasta.mkdir(exist_ok=True)
        try:
            _modelo = YOLO(str(pasta / nome))
        except (OSError, RuntimeError, ValueError) as erro:
            raise RuntimeError("Não foi possível carregar YOLO11n. Confira internet no primeiro "
                               "download e o arquivo models/yolo11n.pt. " + str(erro)) from erro
    return _modelo


def detectar(quadro, config):
    modelo = carregar_modelo(config["model"])
    resultado = modelo.predict(quadro, classes=[0], conf=config["confidence"],
                               device=config["device"], imgsz=config["image_size"],
                               verbose=False, save=False)[0]
    return resultado.boxes.xyxy.cpu().tolist()
