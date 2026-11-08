# Uso de Inteligência Artificial no Projeto "Conecta Brasil"

Este documento foi criado para registrar como as ferramentas de Inteligência Artificial (IA) foram utilizadas durante o desenvolvimento do projeto **Conecta Brasil**. O objetivo aqui é mostrar de forma transparente quais partes eu fiz manualmente (que foi a maior parte do sistema) e onde eu precisei pedir uma ajudinha da IA.

## 1. Quais ferramentas de IA foram utilizadas
Durante o desenvolvimento deste projeto, utilizei principalmente o **ChatGPT** (e em alguns momentos o **Codex**). Eles foram usados como assistentes virtuais para tirar dúvidas de código e sugerir exemplos práticos.

## 2. Explicar a finalidade de cada ferramenta
Eu construí a base do projeto inteiro sozinho. A organização dos arquivos, a ideia de como eles iam se conectar e a lógica principal do programa foram feitas à mão.

A IA foi utilizada com uma finalidade bem específica: atuar como um "professor particular" ou um consultor. Eu recorri a ela apenas quando não conhecia muito bem alguma biblioteca nova, como foi o caso do OpenCV (para mexer com a imagem da câmera) e do YOLO (para a inteligência artificial de reconhecimento visual). Eu também usei a IA para me ajudar a escrever algumas funções repetitivas ou que eu estava com dificuldade de começar.

## 3. Registrar os prompts utilizados durante o desenvolvimento

Como eu já tinha o projeto organizado na minha cabeça, meus prompts foram como conversas com um colega mais experiente. Eu passava bastante contexto para que a IA não fizesse o projeto por mim, mas sim me ajudasse no que faltava:

**Para o módulo de Inteligência Visual (`detector.py`):**
> "Eu estou fazendo um projeto em Python chamado 'Conecta Brasil'. Eu já criei os arquivos e a lógica principal, mas preciso de ajuda para fazer o arquivo `detector.py`. Eu quero usar o modelo YOLO para reconhecer pessoas pela webcam. Como eu nunca usei o YOLO antes, leia o projeto inteiro e integre o Yolo com o código mais simples possível, e adicione comentários para facilitar meu entendimento. Precisa ser uma classe que carrega o modelo, recebe a imagem do OpenCV, faz a detecção apenas de pessoas, e depois me devolve a imagem com um overlay quadrado verde desenhado e a quantidade de pessoas que aparecem na câmera."

**Para o módulo de Interface e Vídeo (`monitoramento.py`):**
> "No meu arquivo `monitoramento.py`, Já está abrindo a câmera com o OpenCV, mas falta o overlay e a contagem de pessoas. Você pode criar duas funções para mim? A primeira seria a `iniciar()` para começar o loop da câmera. A segunda seria a `desenhar_overlay()`. Nessa função, eu quero que ela pegue o número de pessoas detectadas e coloque um texto verde na tela, com uma caixa preta atrás para ficar fácil de ler. Como eu uso o `cv2.putText` e o `cv2.rectangle` pra fazer isso?"

**Para o módulo de Salvar Arquivos (`dados.py`):**
> "Eu preciso salvar o histórico do meu projeto em arquivos para não perder os dados quando eu fechar o programa. No arquivo `dados.py`, me ajude a criar algumas funções. Preciso da `carregar_config()` para ler um arquivo JSON de configurações. Quero também uma função `validar_leitura()` só para garantir que os dados não estão vindo zerados ou com erro antes de salvar. Depois, crie a `salvar_sessao()` para escrever no arquivo e a `carregar_historico()` para ler. Use `try` e `except` para fallback em caso de erro, pensando em evitar do meu programa não fechar sozinho se o arquivo não existir na primeira vez que eu rodar"

**Para o módulo Principal (`main.py`):**
> "Para finalizar, no meu `main.py`, eu quero que, antes de abrir a tela da câmera, ele mostre no terminal o histórico. Você pode me ajudar a criar as funções `consultar_ultima_leitura()` e `consultar_historico()`? Elas só precisam puxar as informações do arquivo `dados.py` e imprimir de um no terminal"

## 4. Identificar quais funcionalidades foram desenvolvidas ou modificadas com auxílio da IA

A maior parte do controle do sistema foi feita por mim. A IA ajudou ativamente nas seguintes partes:

*   **No arquivo `detector.py`:** Quase o arquivo inteiro. Como eu nunca tinha usado o YOLO, a IA ficou responsável por montar a estrutura da detecção para mim.
*   **No arquivo `monitoramento.py`:** A IA ajudou a construir a função `iniciar()` e a função `desenhar_overlay()` (a parte gráfica do OpenCV).
*   **No arquivo `dados.py`:** A IA gerou a base das funções `carregar_config()`, `validar_leitura()`, `salvar_sessao()` e `carregar_historico()`, para lidar com arquivos JSON.
*   **No arquivo `main.py`:** A IA ajudou a formatar as funções `consultar_ultima_leitura()` e `consultar_historico()`.

## 5. Explicar como os resultados gerados pela IA foram verificados

Mesmo sem nunca ter usado Yolo, eu tinha uma ideia bem clara de o que eu estava fazendo, e eu já havia construido a estrutura do meu código. Por isso, quando a IA gerava um código, eu não copiei e colei de qualquer jeito. 
O que eu fiz foi ler linha por linha do que ela gerou. Usei muito `print()` no meio do código para ver o que cada variável estava guardando. Se a IA criava uma função com nomes de variáveis diferentes do resto do meu projeto, eu alterava manualmente para manter o padrão que eu mesmo criei. A IA funcionou mais como uma inspiração de lógica.

## 6. Registrar os testes realizados

Eu testei o projeto em várias etapas para ter certeza de que o código da IA estava funcionando com o meu:
*   **Teste de arquivos:** Fui na pasta do projeto e apaguei o arquivo JSON de histórico. Depois rodei o código para ver se as funções `try/except` da IA seguravam o erro. E funcionou, ele criou um arquivo novo sem quebrar o programa.
*   **Teste da câmera e interface:** Coloquei o programa para rodar e testei a função `desenhar_overlay()`. Fiquei passando na frente da câmera para ver se o contador atualizava na tela sem atrasos.
*   **Teste geral:** Executei o `main.py` do zero para ver se ele consultava o histórico antigo no terminal antes de abrir a câmera, confirmando que a união de todos os arquivos deu certo.

## 7. Apresentar os benefícios e limitações do uso da IA

**Benefícios:** 
Foi incrível para me poupar tempo. Em vez de ficar horas lendo tutoriais complexos sobre como instalar e usar o YOLO ou sobre como desenhar um retângulo transparente no OpenCV, a IA me deu exemplos muito diretos. Isso me deixou livre para focar em organizar o projeto e aprender a lógica.

**Limitações:** 
A IA não tem a visão do projeto inteiro. Muitas vezes ela me dava um código que funcionava sozinho, mas que não se encaixava direito no meu `main.py`. Além disso, às vezes ela usava códigos muito avançados ou lógicas muito confusas que eu ainda não aprendi, me obrigando a pedir para ela simplificar.

## 8. Registrar as dificuldades encontradas

Um desafio encontrado foi transformar as detecções do YOLO na contagem necessária para o projeto. O modelo identifica objetos na imagem, mas precisávamos considerar somente pessoas dentro da região monitorada.

Com auxílio da IA, utilizamos o filtro da classe pessoa e as coordenadas das caixas detectadas. Definimos que uma pessoa seria contada quando o centro de sua caixa estivesse dentro da região configurada. Depois, verificamos esse comportamento posicionando pessoas dentro e fora da área.

Essa integração exigiu compreender quais informações o YOLO retorna e como utilizá-las na lógica do programa.
