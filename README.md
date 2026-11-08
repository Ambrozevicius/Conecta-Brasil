# Conecta Brasil

## Monitoramento de ocupação em áreas de espera

**Global Solution FIAP | CitizenTech | Engenharia de Software**

O **Conecta Brasil** é um projeto que propõe utilizar tecnologia para ajudar passageiros a conhecer as condições de uma área de espera antes de chegar ao transporte público. O Terminal Jabaquara, em São Paulo, foi escolhido como referência para o projeto.

Nesta entrega, o protótipo Python utiliza uma webcam e um modelo de detecção de pessoas para mostrar quantas pessoas estão visíveis em uma região da imagem. As leituras são armazenadas em JSON e podem ser consultadas pelo terminal, junto com estatísticas simples.

## Sumário

1. [Problema e público-alvo](#1-problema-e-público-alvo)
2. [Solução proposta e objetivos](#2-solução-proposta-e-objetivos)
3. [Nossa Equipe](#3-nossa-equipe)
4. [Escopo desta entrega](#4-escopo-desta-entrega)
5. [Funcionamento e regras de contagem](#5-funcionamento-e-regras-de-contagem)
6. [Tecnologias e requisitos](#6-tecnologias-e-requisitos)
7. [Instalação e execução](#7-instalação-e-execução)
8. [Opções do menu](#8-opções-do-menu)
9. [Configuração](#9-configuração)
10. [Armazenamento e consultas](#10-armazenamento-e-consultas)
11. [Organização e conteúdos de Python](#11-organização-e-conteúdos-de-python)
14. [Privacidade, limitações e próximos passos](#14-privacidade-limitações-e-próximos-passos)

## 1. Problema e público-alvo

O projeto parte da seguinte situação: um passageiro pretende utilizar um terminal em um horário movimentado, mas não dispõe de uma informação recente sobre a quantidade de pessoas na área em que aguardará. Essa incerteza pode dificultar a decisão sobre quando sair de casa, principalmente para quem tem alguma flexibilidade de horário.

O público-alvo são passageiros que desejam consultar as condições da área de espera antes de chegar ao local. O Terminal Jabaquara foi escolhido para delimitar o contexto, mas a demonstração representa apenas uma área monitorada por câmera, não todo o terminal.


## 2. Solução proposta e objetivos

O Conecta Brasil transforma imagens capturadas por uma câmera em registros de contagem, classificação e horário. A solução foi organizada em três etapas:

1. **Observar:** capturar a imagem e detectar as pessoas visíveis na região definida.
2. **Registrar:** guardar as contagens e seus horários, formando um histórico.
3. **Informar:** apresentar a última leitura, a classificação de ocupação, o histórico e suas estatísticas pelo menu do terminal.

O objetivo da entrega de Python é demonstrar esse fluxo funcionando localmente, com um menu simples, validações e persistência em arquivo.

A relação com **Cidades e Comunidades Sustentáveis**, está na proposta de ampliar o acesso à informação sobre o uso do transporte público e apoiar o planejamento dos deslocamentos.

## 3. Nossa Equipe

| Integrante | RM | Responsabilidade no projeto integrado |
|---|---|---|
| Isaac Ambrozevicius | 569166 | Python e Cálculo |
| Joao Lucca | 569562 |IoT |
| Thalles Almeida | 569925 | Storytelling, Software e Total Experience |
| Murillo Marim | 569045 | Web e Front-end|


## 4. Escopo desta entrega

| Features |
|---|
| Captura por webcam e detecção de pessoas 
| Contagem dentro de uma região configurável 
| Exibição de caixas, contagem e faixa na imagem 
| Gravação periódica em JSON | 
| Consulta da última leitura e do histórico 
| Estatísticas simples pelo terminal | 
 

## 5. Funcionamento e regras de contagem

Ao iniciar o monitoramento, o programa carrega o modelo YOLO11n, abre a câmera e processa seus quadros. Somente a detecção de pessoas é considerada.

A região de interesse, chamada `roi`, delimita a parte da imagem monitorada. Uma detecção entra na contagem quando o centro da caixa que envolve a pessoa está dentro dessa região, incluindo a borda. **Não é necessário que o corpo inteiro esteja dentro do retângulo**.

A janela mostra a região, as caixas das pessoas contadas, a quantidade detectada e a faixa correspondente. A contagem é atualizada conforme os quadros são processados. A primeira leitura é salva assim que o primeiro quadro é processado; as próximas seguem o intervalo configurado, de cinco segundos por padrão.

### Faixas de ocupação

| Quantidade detectada | Faixa exibida | Valor salvo |
|---|---|---|
| 0 | Sem pessoas detectadas | `empty` |
| 1 a 2 | Baixa | `low` |
| 3 | Moderada | `moderate` |
| 4 a 5 | Alta | `high` |
| 6 ou mais | Muito alta | `very_high` |
| Leitura indisponível | Indisponível | `unavailable` |

Esses limites são apenas exemplos, eles se devem a dificuldade de encaixar certa quantidade de pessoas em uma imagem da Webcam para a simulação.


## 6. Tecnologias e requisitos

| Tecnologia | Utilização |
|---|---|
| Python | Menu, regras, consultas, persistência e integração dos módulos |
| Ultralytics / YOLO11n pré-treinado | Detecção de pessoas |
| OpenCV | Acesso à webcam e desenho das informações na imagem |
| tzdata / zoneinfo | Exibição dos horários no fuso de São Paulo |
| JSON | Armazenamento local das sessões |

O ambiente utilizado para o projeto foi o **Windows com Python 3.12.10** 

São necessários uma webcam, espaço para dependências e modelo, e acesso à internet durante a instalação e o primeiro download.

O arquivo `requirements.txt` contém as dependências necessarias para rodar o programa. 

**Alerta: após a instalação das depencências, o projeto vai contabilizar mais ou menos 1GB de armazenamento !!!**

## 7. Instalação e execução

Para rodar o programa: Abra o PowerShell na pasta que contém `main.py` e `requirements.txt`.

### 7.1 Crie o ambiente virtual com este comando

```powershell
py -3.12 -m venv .venv
```

### 7.2 Instale as dependências com este comando (pode demorar um pouco)

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 7.3 Inicie o programa com este comando

```powershell
.\.venv\Scripts\python.exe main.py
```


## 8. Opções do menu

| Opção | Funcionamento |
|---|---|
| **1 - Iniciar monitoramento** | Abre a webcam, mostra a contagem e registra as leituras |
| **2 - Consultar última leitura** | Mostra o último registro, seu horário, faixa e tempo decorrido |
| **3 - Consultar histórico e estatísticas** | Mostra até dez registros recentes e o resumo de todas as leituras válidas do conjunto |
| **4 - Sobre o projeto** | Breve explicação sobre o projeto |
| **0 - Sair** | Encerra o programa |

Durante a captura, **Q ou Esc** encerram o monitoramento e retornam ao menu.

### Como testar 

1. Inicie o programa e escolha a opção 1.
2. Observe a contagem sem pessoas e depois com participantes entrando na imagem (é possível mostrar uma imagem no celular com pessoas).
3. Aguarde a gravação de algumas leituras e pressione Q ou Esc.
4. Consulte a última leitura pela opção 2.
5. Consulte o histórico, a média e a maior contagem pela opção 3.
6. Inicie outra captura para demonstrar o reinício e encerre pela opção 0.

As consultas ficam disponíveis após o retorno ao menu.

## 9. Configuração

Edite `config.json` com o monitoramento encerrado e preserve a sintaxe JSON.

| Campo | Padrão | Significado |
|---|---|---|
| `project_name` | `Conecta Brasil` | Identificação descritiva da configuração |
| `area_id` | `jabaquara-demo-01` | Identificador da área monitorada |
| `area_name` | `Área piloto de espera` | Nome exibido nas consultas |
| `environment` | `demo` | Identifica a demonstração |
| `threshold_version` | `demo-v1` | Versão |
| `camera_index` | `0` | Índice da webcam |
| `roi` | `[0, 0, 1, 1]` | Região monitorada; o padrão cobre toda a imagem |
| `model` | `yolo11n.pt` | Modelo pré-treinado utilizado |
| `confidence` | `0.4` | Limiar de confiança das detecções |
| `device` | `cpu` | Dispositivo usado na detecção |
| `frame_width` / `frame_height` | `640` / `480` | Resolução solicitada à câmera |
| `image_size` | `416` | Tamanho de entrada utilizado na inferência |
| `record_interval_seconds` | `5` | Intervalo entre registros |

A ROI segue `[x1, y1, x2, y2]`, com coordenadas proporcionais entre 0 e 1. O ponto `(0, 0)` corresponde ao canto superior esquerdo da imagem. Para monitorar um retângulo central, use `[0.25, 0.25, 0.75, 0.75]` por exemplo.


## 10. Armazenamento e consultas

Cada sessão recebe um identificador UUID. Quando há uma leitura, ela é persistida em `data/<UUID>.json`. O documento contém `session_id`, `started_at`, uma cópia de `config` e a lista `readings`.

### Campos de cada leitura

| Campo | Descrição |
|---|---|
| `reading_id` | Identificador único do registro |
| `area_id` | Área à qual a leitura pertence |
| `measured_at` | Horário da leitura em ISO 8601, com fuso UTC |
| `source` | Origem do dado: `camera` |
| `environment` | Ambiente de demonstração |
| `people_count` | Inteiro não negativo ou `null` quando a leitura está indisponível |
| `quality` | `ok` para contagem válida ou `camera_error` para falha registrada |
| `threshold_version` | Versão dos limites da classificação |
| `occupancy_status` | Faixa correspondente à contagem |


Nas novas leituras válidas, os campos de previsão ficam nulos, com estado `insufficient_history`; nas falhas registradas, o estado é `unavailable`.

Zero pessoas é diferente de falha. Quando a câmera não abre ou retorna uma leitura sem quadro, o programa registra `null` com `camera_error`. Outros erros, como falha de inferência ou de disco, interrompem a operação com a mensagem de erro, foi utilizado **try/except** para fazer isso.

A gravação utiliza um arquivo temporário seguido da substituição do arquivo de destino.

### Estatísticas e atualização

A consulta reúne arquivos de `data/` compatíveis com a área, ambiente e versão das faixas atuais. Mostra até dez registros recentes, mas calcula as estatísticas sobre todas as leituras válidas desse conjunto:

- Quantidade de leituras válidas.
- Média das contagens.
- Maior contagem observada.
- Horário da última leitura válida.

A média é calculada por leitura, sem ponderação pela duração dos intervalos.

Os horários são salvos em UTC e apresentados no fuso de São Paulo.

## 11. Organização e conteúdos de Python

### Arquivos publicados no repositório

| Arquivo | O que contém |
|---|---|
| `README.md` | Documentação do projeto, instalação e uso |
| `prompts.md` | Documentação explicando como a IA foi utilizada durante o projeto |
| `config.json` | Configuração do monitor |
| `dados.py` | Validação, classificação, sessões, persistência e estatísticas |
| `detector.py` | Carregamento do modelo e detecção de pessoas |
| `main.py` | Menu e apresentação das consultas |
| `monitoramento.py` | Captura, seleção da região, contagem e informações na imagem |
| `requirements.txt` | Dependências para fazer download |

### Pastas criadas localmente

Estas pastas não fazem parte dos arquivos publicados:

| Pasta | Quando é criada e para que serve |
|---|---|
| `.venv/` | Criada pelo comando de instalação para isolar as dependências |
| `models/` | Criada ao carregar o detector para armazenar o modelo YOLO11n |
| `data/` | Criada na primeira gravação para armazenar sessões em JSON |

O Python e as bibliotecas também podem criar pastas de cache durante a execução.

### Aplicação dos conteúdos da disciplina

| Conteúdo | Aplicação no código |
|---|---|
| `while` e `input()` | Repetição do menu e recebimento da opção em `main()` |
| `match/case` | Seleção da ação do menu |
| `if/elif/else` | Classificação, validações e apresentação do tempo decorrido |
| `for` | Consulta de registros, processamento de arquivos e desenho das detecções |
| Funções com parâmetros e retornos | Separação das regras de contagem, classificação, persistência e estatísticas |
| Listas | Leituras das sessões e caixas detectadas |
| Tuplas | Coordenadas da região em pixels |
| Dicionários | Configuração, sessões e registros |
| `try/except/finally` | Tratamento de erros e liberação da câmera |
| Arquivos e JSON | Armazenamento e recuperação do histórico |



## 14. Privacidade, limitações e próximos passos

O programa não grava fotos ou vídeos, não identifica pessoas e não realiza reconhecimento facial. São armazenadas contagens, horários, configuração e metadados de funcionamento.

A iluminação, o enquadramento, e a distância podem prejudicar a detecção. Uma leitura de zero significa que não houve detecções naquela região.

Como uma possível continuidade, nós pensamos em disponibilizar as leituras por uma API e uma interface web. Uma possível expansão para outras áreas, sensores e informações do transporte   puxando de uma API como a do **Olho vivo** da SPtrans .
