import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import datetime # Importar datetime

# 1. Carregar DataFrame df_mensagens_temas do arquivo CSV
df_mensagens_temas = pd.read_csv('chat_messages_temas_grupo.csv') # Carrega mensagens com tópicos

# 2. Definir Cores para os Tópicos Principais (para a nuvem de palavras) - NÃO USADO NESTA VERSÃO - Removido color_func
topic_colors = { # REMOVIDO - Não estamos usando color_func nesta versão
    'Ferramentas e Plataformas': 'skyblue',
    'Aplicações Jurídicas Práticas': 'coral',
    'Código Aberto e Custo': 'lightgreen',
    'Conceitos Técnicos e Fundamentos de IA': 'gold',
    'Questões Éticas, Regulatórias e Sociais': 'plum',
    'Interdisciplinaridade e Fundamentos Teóricos': 'cyan'
}

# 3. Carregar Stopwords do arquivo TXT stopwords-pt.txt
stopwords = set() # Inicializa um conjunto (set) vazio para stopwords
with open('stopwords-pt.txt', 'r', encoding='utf-8') as f: # Abre o arquivo stopwords.txt
    for line in f:
        stopword = line.strip() # Lê cada linha, remove espaços em branco extras
        stopwords.add(stopword) # Adiciona cada stopword ao conjunto

# 4. Gerar Nuvens de Palavras para Cada Tópico Principal - MODIFICADO para fundo preto e cores automáticas
for topico_principal in df_mensagens_temas['Tópico'].unique(): # Iterar sobre tópicos únicos
    if topico_principal == 'Outros' or topico_principal is None: # Ignorar categoria 'Outros' e valores None
        continue

    text_topico = " ".join(mensagem for mensagem in df_mensagens_temas[df_mensagens_temas['Tópico'] == topico_principal]['Mensagem']) # Filtrar mensagens por tópico e concatenar

    # Gerar WordCloud para o tópico atual - MODIFICADO para fundo preto e cores automáticas
    wordcloud = WordCloud(width=800, height=400,
                          background_color='black', # Fundo preto - MODIFICADO
                          # colormap=topic_colors.get(topico_principal, 'viridis'), # REMOVIDO colormap argument
                          # color_func=topic_color_func, # REMOVIDO color_func argument
                          max_words=200,
                          collocations=False, # Desativar colocations para palavras individuais
                          stopwords=stopwords) # Usar stopwords CARREGADAS DO TXT

    wordcloud.generate(text_topico) # Chamar .generate() para calcular a wordcloud

    plt.title(f'{topico_principal}', fontsize=16, color='white') # **RESTAURADO e VERIFICADO: Título inclui o tópico e cor branca**
    plt.imshow(wordcloud, interpolation='bilinear') # Agora wordcloud JÁ FOI CALCULADA
    plt.axis("off")
    plt.tight_layout(pad=0)

    # **Gerar Timestamp para o nome do arquivo**
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'{timestamp}_wordcloud_{topico_principal}_blackbg.png' # Nome do arquivo com timestamp e nome do tópico - MODIFICADO nome do arquivo
    plt.savefig(filename, facecolor='black') # Salvar nuvem de palavras com fundo preto e timestamp
    plt.show()

    print(f"\nNuvem de palavras gerada para o tópico: {topico_principal} (fundo preto)") # Mensagem de confirmação ajustada