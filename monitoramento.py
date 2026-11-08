#Conta pessoas pela webcam e salva as leituras
import time
import unicodedata


def regiao_pixels(regiao, largura, altura):
    return tuple(valor * dimensao for valor, dimensao in
                 zip(regiao, (largura, altura, largura, altura)))


def selecionar_caixas(caixas, regiao):
    x1, y1, x2, y2 = regiao
    return [caixa for caixa in caixas
            if x1 <= (caixa[0] + caixa[2]) / 2 <= x2
            and y1 <= (caixa[1] + caixa[3]) / 2 <= y2]


def desenhar_overlay(cv, quadro, caixas, regiao, faixa):
    cv.rectangle(quadro, tuple(map(int, regiao[:2])), tuple(map(int, regiao[2:])),
                 (255, 180, 0), 2)
    for caixa in caixas:
        cv.rectangle(quadro, tuple(map(int, caixa[:2])), tuple(map(int, caixa[2:])),
                     (0, 220, 0), 2)
    textos = ["DEMO LOCAL - nao implantado no terminal", f"Pessoas: {len(caixas)} | {faixa}",
              "Q / Esc: voltar | apenas pessoas visiveis na regiao"]
    for indice, texto in enumerate(textos):
        texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
        ponto = (10, 24 + indice * 26)
        cv.putText(quadro, texto, ponto, cv.FONT_HERSHEY_SIMPLEX, .55, (0, 0, 0), 4)
        cv.putText(quadro, texto, ponto, cv.FONT_HERSHEY_SIMPLEX, .55, (255, 255, 255), 1)


def iniciar(config):
    """Uma sessão de webcam: contar, exibir e salvar a cada cinco segundos."""
    import cv2 as cv
    from detector import carregar_modelo, detectar
    from dados import classificar, ROTULOS, nova_sessao, registrar_leitura
    carregar_modelo(config["model"])
    sessao = nova_sessao(config)
    camera = None
    try:
        camera = cv.VideoCapture(config["camera_index"])
        if not camera.isOpened():
            registrar_leitura(sessao, config, None)
            print("Câmera indisponível. Confira índice, conexão e permissão do Windows.")
            return
        camera.set(cv.CAP_PROP_FRAME_WIDTH, config["frame_width"])
        camera.set(cv.CAP_PROP_FRAME_HEIGHT, config["frame_height"])
        proximo = time.monotonic()
        while True:
            sucesso, quadro = camera.read()
            if not sucesso or quadro is None:
                registrar_leitura(sessao, config, None)
                print("Falha de leitura: câmera indisponível. Sessão encerrada.")
                break
            altura, largura = quadro.shape[:2]
            regiao = regiao_pixels(config["roi"], largura, altura)
            caixas = selecionar_caixas(detectar(quadro, config), regiao)
            agora = time.monotonic()
            if agora >= proximo:
                registrar_leitura(sessao, config, len(caixas))
                intervalo = config["record_interval_seconds"]
                # Mantém os prazos originais e pula os perdidos, sem inventar capturas.
                proximo += (int((agora - proximo) // intervalo) + 1) * intervalo
            desenhar_overlay(cv, quadro, caixas, regiao, ROTULOS[classificar(len(caixas))])
            cv.imshow("Conecta Brasil - demonstracao local", quadro)
            if cv.waitKey(1) & 0xFF in (ord("q"), ord("Q"), 27):
                break
            if cv.getWindowProperty("Conecta Brasil - demonstracao local", cv.WND_PROP_VISIBLE) < 1:
                break
    except KeyboardInterrupt:
        print("Monitoramento interrompido.")
    except cv.error as erro:
        raise RuntimeError(f"OpenCV: {erro}. Confira webcam e suporte a janelas (opencv-python).") from erro
    finally:
        if camera is not None:
            camera.release()
        cv.destroyAllWindows()
