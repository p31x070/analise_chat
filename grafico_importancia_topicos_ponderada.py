import matplotlib.pyplot as plt
import pandas as pd
import datetime

# 1. Carregar DataFrame df_interacoes_ponderadas do arquivo CSV
df_interacoes_ponderadas = pd.read_csv('df_interacoes_ponderadas_temporal_grupo.csv') # Carrega do CSV ponderado temporal

# 2. Agregar Peso das Interações por Tópico
interacao_peso_por_topico = {} # Dicionário para armazenar peso total por tópico

for index, row in df_interacoes_ponderadas.iterrows():
    topic = row['Tópico']
    peso = row['Peso']
    if topic not in interacao_peso_por_topico:
        interacao_peso_por_topico[topic] = 0
    interacao_peso_por_topico[topic] += peso

# Converter dicionário para DataFrame para facilitar o plot
df_peso_por_topico = pd.DataFrame(list(interacao_peso_por_topico.items()), columns=['Tópico', 'Peso Total Interação'])
df_peso_por_topico = df_peso_por_topico.sort_values(by='Peso Total Interação', ascending=False) # Ordenar por peso


# 3. Gerar Gráfico de Barras
plt.figure(figsize=(12, 7))
bars = plt.bar(df_peso_por_topico['Tópico'], df_peso_por_topico['Peso Total Interação'], color='purple')

# 4. Configurações do Gráfico (em Português)
plt.title('Importância dos Tópicos em Interações Ponderadas por Tempo', fontsize=14)
plt.xlabel('Tópicos de Discussão', fontsize=12)
plt.ylabel('Peso Total de Interação', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y')

# Adicionar rótulos com o peso total em cada barra (ajustado para melhor leitura)
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, int(yval), ha='center', va='bottom', fontsize=10)

plt.tight_layout()

# 5. Salvar o Gráfico em Arquivo PNG
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f'{timestamp}_topic_importance_weighted_temporal_interactions_standalone.png' # Nome do arquivo com timestamp

plt.savefig(filename) # Salvar com nome significativo
plt.show()

print("\nGráfico de importância dos tópicos em interações ponderadas gerado e salvo como 'topic_importance_weighted_temporal_interactions_standalone.png'")