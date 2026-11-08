#Mostra o menu
from zoneinfo import ZoneInfo
from dados import carregar_config, carregar_historico, instante, agora_utc, estatisticas, ROTULOS

def linha():
    print("-" * 60)


def exibir_menu():
    linha()
    print("Conecta Brasil — demonstração local")
    linha()
    print("1 - Iniciar monitoramento")
    print("2 - Consultar última leitura")
    print("3 - Consultar histórico e estatísticas")
    print("4 - Sobre o projeto")
    print("0 - Sair")
    linha()


def iniciar_monitoramento():
    linha()
    from monitoramento import iniciar
    iniciar(carregar_config())


def horario_local(texto):
    return instante(texto).astimezone(ZoneInfo("America/Sao_Paulo")).strftime("%d/%m/%Y %H:%M:%S")


def mostrar_leitura(leitura):
    contagem = leitura['people_count']
    pessoas = str(contagem) if contagem is not None else 'indisponível (falha de câmera)'
    print(f"{horario_local(leitura['measured_at'])} | Pessoas: {pessoas} | {ROTULOS[leitura['occupancy_status']]}")


def formatar_tempo_decorrido(segundos):
    if segundos < 60:
        quantidade = int(segundos)
        unidade = "segundo"
    elif segundos < 3600:
        quantidade = int(segundos // 60)
        unidade = "minuto"
    else:
        quantidade = int(segundos // 3600)
        unidade = "hora"
    if quantidade != 1:
        unidade += "s"
    return f"{quantidade} {unidade}"


def consultar_ultima_leitura():
    linha()
    historico = carregar_historico(carregar_config())
    if not historico:
        print("Nenhuma leitura disponível em data/ para esta área.")
        return
    ultima = historico[-1]
    mostrar_leitura(ultima)
    tempo_decorrido = (agora_utc() - instante(ultima['measured_at'])).total_seconds()
    if tempo_decorrido < 0:
        print("Horário futuro inválido: confira o relógio da captura.")
    else:
        print(f"Último registro feito há {formatar_tempo_decorrido(tempo_decorrido)}.")
        if tempo_decorrido > 30:
            print("Registro histórico: a contagem pode não representar a situação atual.")
        else:
            print("Registro recente (feito nos últimos 30 segundos).")


def consultar_historico():
    linha()
    config = carregar_config()
    historico = carregar_historico(config)
    print(f"Conjunto: arquivos de data/ | Área: {config['area_name']} ({config['area_id']})")
    print(f"Ambiente: {config['environment']} | Faixas: {config['threshold_version']}")
    if not historico:
        print("Histórico inexistente, vazio ou sem leituras válidas para esta área.")
    else:
        print("Até 10 registros mais recentes — horário de São Paulo:")
        for leitura in historico[-10:]:
            mostrar_leitura(leitura)
    resultado = estatisticas(historico, config)
    linha()
    print(f"Estatísticas de todas as leituras válidas desse conjunto: {resultado['quantidade']}")
    if resultado['quantidade']:
        print(f"Média: {resultado['media']:.2f} pessoas | Maior contagem: {resultado['maior']}")
        print("Última leitura válida:", horario_local(resultado['ultima']))
    else:
        print("Sem dados válidos para calcular média, maior contagem e último horário.")


def sobre_projeto():
    linha()
    print("SOBRE O PROJETO — Conecta Brasil / Global Solution FIAP")
    print("O objetivo é explorar como informar passageiros sobre pessoas")
    print("presentes em uma área de espera, no contexto do Terminal Jabaquara")
    print("e do ODS 11 — Cidades e Comunidades Sustentáveis.")
    print("Uma webcam e o YOLO contam pessoas visíveis na região delimitada.")
    print("As contagens e horários são salvos para consultar histórico e estatísticas.")
    print("É uma demonstração local com voluntários, sem implantação no terminal.")
    print("Não mede pessoas únicas, entradas acumuladas ou o terminal inteiro.")
    print("Não identifica pessoas nem salva fotos ou vídeos.")
    print("A qualidade da contagem depende da visibilidade e exige avaliação manual.")
    linha()
    print("Equipe:")
    print("Isaac Ambrozevicius — RM 569166 | Joao Lucca — RM 569562")
    print("Thalles Almeida — RM 569925 | Murillo Marim — RM 569045")
    linha()


def main():
    while True:
        try:
            exibir_menu()
            opcao = input("Opção: ").strip()
            match opcao:
                case "1":
                    iniciar_monitoramento()
                case "2":
                    consultar_ultima_leitura()
                case "3":
                    consultar_historico()
                case "4":
                    sobre_projeto()
                case "0":
                    return
                case _:
                    print("Opção inválida. Digite um número do menu.")
        except ImportError as erro:
            print(f"Dependência ausente: {erro}. Instale requirements.txt no ambiente virtual.")
        except (OSError, ValueError, RuntimeError) as erro:
            print(f"Operação interrompida: {erro}")
        except (KeyboardInterrupt, EOFError):
            print("\nSaindo.")
            return


if __name__ == "__main__":
    main()
