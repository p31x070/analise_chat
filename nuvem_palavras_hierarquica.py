import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import datetime # Importar datetime
import json # Importar biblioteca json - ADICIONADO

# Carregar dicionário de palavras-chave de topic_keywords.json - ADICIONADO JSON LOADING
with open('topic_keywords.json', 'r', encoding='utf-8') as f: # **ADICIONADO**: Carregar topic_keywords.json
    topic_keywords_expandido = json.load(f)


# 1. Carregar DataFrame df_mensagens_temas do arquivo CSV
df_mensagens_subtemas = pd.read_csv('chat_messages_temas_grupo.csv') # MODIFICADO - Carrega df_mensagens_subtemas

# 2. Definir Cores para os Tópicos Principais (para colorir as nuvens de palavras dos subtemas)
# topic_colors = { # Mantendo as mesmas cores dos tópicos principais
#     'Ferramentas e Plataformas': 'skyblue',
#     'Aplicações Jurídicas Práticas': 'coral',
#     'Código Aberto e Custo': 'lightgreen',
#     'Conceitos Técnicos e Fundamentos de IA': 'gold',
#     'Questões Éticas, Regulatórias e Sociais': 'plum',
#     'Interdisciplinaridade e Fundamentos Teóricos': 'cyan' # Cor para o novo tópico
# }

# 3. Carregar Stopwords do arquivo TXT stopwords-pt.txt
stopwords = set() # Inicializa um conjunto (set) vazio para stopwords
with open('stopwords-pt.txt', 'r', encoding='utf-8') as f: # Abre o arquivo stopwords.txt
    for line in f:
        stopword = line.strip() # Lê cada linha, remove espaços em branco extras
        stopwords.add(stopword) # Adiciona cada stopword ao conjunto

# 4. Gerar Nuvens de Palavras para Cada SUBTÓPICO - MODIFICADO para iterar por subtema
for topico_principal, subtopics_dict in topic_keywords_expandido.items(): # Iterar sobre tópicos PRINCIPAIS e SUBTEMAS
    if topico_principal == 'Outros': # Ignorar categoria 'Outros'
        continue
    for subtopico in subtopics_dict.keys(): # Iterar sobre SUBTEMAS dentro de cada tópico principal

        text_subtopico = " ".join(mensagem for mensagem in df_mensagens_subtemas[(df_mensagens_subtemas['Tópico'] == topico_principal) & (df_mensagens_subtemas['Subtópico'] == subtopico)]['Mensagem']) # Filtrar mensagens por TÓPICO PRINCIPAL e SUBTÓPICO

        # Gerar WordCloud para o SUBTÓPICO atual
        wordcloud = WordCloud(width=800, height=400,
                              background_color='black', # Fundo preto
                            #   colormap=topic_colors.get(topico_principal, 'viridis'), # Usar cor do tópico PRINCIPAL
                              max_words=100, # Reduzido max_words para nuvens de subtemas (opcional)
                              collocations=False, # Desativar colocations para palavras individuais
                              stopwords=stopwords)
        
        wordcloud.generate(text_subtopico) # Chamar .generate() para calcular a wordcloud

        titulo_nuvem = f'Nuvem de Palavras - Tópico: {topico_principal} - Subtópico: {subtopico}' # Título INCLUI Tópico e Subtópico
        plt.title(titulo_nuvem, fontsize=14, color='white') # Título em branco para fundo preto
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.tight_layout(pad=0)

        # **Gerar Timestamp para o nome do arquivo**
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'{timestamp}_wordcloud_{topico_principal}_{subtopico}_blackbg.png' # Nome do arquivo com timestamp, tópico e subtopico
        plt.savefig(filename, facecolor='black') # Salvar nuvem de palavras com fundo preto e timestamp
        plt.show()

        print(f"\nNuvem de palavras gerada para o subtopico: {subtopico} (tópico: {topico_principal}, fundo preto)") # Mensagem de confirmação ajustada