import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob

# 1. Carregar o DataFrame df_mensagens do arquivo CSV
df_sentimentos_real = pd.read_csv('chat_messages_grupo.csv') # Carrega as mensagens do arquivo CSV

def get_sentiment(text):
    try:  # Bloco try começa aqui
        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity # Analyze sentiment directly in original language
        if polarity > 0.1:
            return 'Positivo'
        elif polarity < -0.1:
            return 'Negativo'
        else:
            return 'Neutro'
    except Exception as e:  # Bloco except alinhado com try
        return 'Erro na Análise'  # Lidar com erros de tradução ou análise

df_sentimentos_real['Sentimento'] = df_sentimentos_real['Mensagem'].apply(get_sentiment)

contagem_sentimentos_real = df_sentimentos_real['Sentimento'].value_counts()

# Gráfico de Pizza com dados reais
plt.figure(figsize=(8, 8))
plt.pie(contagem_sentimentos_real, labels=contagem_sentimentos_real.index, autopct='%1.1f%%', colors=['lightgreen', 'lightcoral', 'lightskyblue'])
plt.title('Distribuição de Sentimentos nas Mensagens do Grupo', fontsize=14)
plt.ylabel('Sentimento') # Adicionado label ao ylabel para clareza
plt.tight_layout()
plt.savefig('sentiment_pie_chart_real.png')
plt.show()

print(df_sentimentos_real.head())
print("\nContagem de Sentimentos Real:\n", contagem_sentimentos_real)