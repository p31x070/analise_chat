import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib

# 1. Carregar DataFrames dos arquivos CSV
df_interacoes_ponderadas = pd.read_csv('df_interacoes_ponderadas_grupo.csv') # Interações ponderadas
df_mensagens_temas = pd.read_csv('chat_messages_grupo.csv') # Mensagens com tópicos

# 2. Agregar Peso das Interações por Tópico
interacao_peso_por_topico = {} # Dicionário para armazenar peso total por tópico

for index, row in df_interacoes_ponderadas.iterrows():
    topic = row['Tópico']
    peso = row['Peso']
    if topic not in interacao_peso_por_topico:
        interacao_peso_por_topico[topic] = 0
    interacao_peso_por_topico[topic] += peso

# Converter dicionário para DataFrame para facilitar o plot (opcional)
df_peso_por_topico = pd.DataFrame(list(interacao_peso_por_topico.items()), columns=['Tópico', 'Peso Total Interação'])
df_peso_por_topico = df_peso_por_topico.sort_values(by='Peso Total Interação', ascending=False) # Ordenar por peso


# 3. Visualizar Importância dos Tópicos (Gráfico de Barras)
plt.figure(figsize=(12, 7))
bars = plt.bar(df_peso_por_topico['Tópico'], df_peso_por_topico['Peso Total Interação'], color='purple')
plt.title('Importância dos Tópicos nas Interações Ponderadas', fontsize=14)
plt.xlabel('Tópicos de Discussão', fontsize=12)
plt.ylabel('Peso Total de Interação', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y')

# Adicionar rótulos com o peso total em cada barra (ajustado para melhor leitura)
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, int(yval), ha='center', va='bottom', fontsize=10)


plt.tight_layout()
plt.savefig('topic_importance_weighted_interactions.png')
plt.show()


print("\nPeso Total de Interação por Tópico (Ordenado):\n")
print(df_peso_por_topico.to_string(index=False))