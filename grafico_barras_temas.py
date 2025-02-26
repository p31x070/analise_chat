import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
import datetime  # Importar datetime

# 1. Carregar DataFrame df_topic_counts do arquivo CSV (gerado por gera_topic_counts_csv.py)
df_topic_counts = pd.read_csv('topic_frequency_messages_bar_chart_data.csv') # Carrega topic frequency data


# 2. Visualizar Frequência dos Tópicos (Gráfico de Barras)
plt.figure(figsize=(12, 7))
bars = plt.bar(df_topic_counts['Tópico'], df_topic_counts['Frequência'], color='purple')
plt.title('Frequência de Tópicos de Discussão nas Mensagens', fontsize=14)
plt.xlabel('Tópicos de Discussão', fontsize=12)
plt.ylabel('Frequência (Contagem de Mensagens)', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y')

# Adicionar rótulos com o peso total em cada barra
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, int(yval), ha='center', va='bottom', fontsize=10)

plt.tight_layout()

# **Gerar Timestamp para o nome do arquivo**
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f'{timestamp}_topic_frequency_messages_bar_chart.png' # Nome do arquivo com timestamp
plt.savefig(filename) # Salvar gráfico com timestamp no nome do arquivo

plt.show()

print("\nFrequência de Tópicos de Discussão (Ordenada):\n")
print(df_topic_counts.to_string(index=False))