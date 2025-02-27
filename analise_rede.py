import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
import datetime # Importar datetime

# 1. Carregar o DataFrame df_interacoes_ponderadas do arquivo CSV
df_interacoes_ponderadas = pd.read_csv('df_interacoes_grupo.csv') # Carrega do CSV ponderado

# 2. Construir o Grafo (Rede)
grafo_interacao_grupo = nx.Graph() # Grafo não direcionado

# Adicionar arestas ao grafo a partir do DataFrame de interações ponderadas
for index, row in df_interacoes_ponderadas.iterrows():
    responder = row['Responder']
    respondido_por = row['Respondido_por']
    grafo_interacao_grupo.add_edge(responder, respondido_por)

# 3. Calcular a Centralidade de Grau
centralidade_grau = nx.degree_centrality(grafo_interacao_grupo)

# 4. Visualizar a Rede
plt.figure(figsize=(14, 10), facecolor='black')  # Fundo escuro
ax = plt.gca()
ax.set_facecolor('black')  # Cor da área do gráfico
plt.rcParams['savefig.facecolor'] = 'black' # Cor do fundo da imagem salva
plt.rcParams['savefig.edgecolor'] = 'black' # Cor da borda da imagem salva

pos = nx.spring_layout(grafo_interacao_grupo, k=0.5, iterations=100, seed=42)  # Layout otimizado

# Gerar cores dos nós usando colormap viridis
node_colors = plt.cm.viridis(range(len(centralidade_grau)))

nx.draw(grafo_interacao_grupo, pos,
        with_labels=True,
        node_size=[v * 8000 for v in centralidade_grau.values()],
        node_color=node_colors,
        edgecolors='black',  # Borda contrastante
        linewidths=0.5,
        edge_color='black',  # Cinza claro
        alpha=0.7,
        font_size=12,  # Aumentar tamanho da fonte
        font_color='black',  # Texto branco
        font_weight='bold',
        width=0.3)

plt.title('Rede de Interação entre Membros do Grupo', fontsize=13, color='black')
plt.xlabel('Membros (Nós)', fontsize=12, color='black')
plt.ylabel('Interações (Arestas)', fontsize=12, color='black')
plt.tight_layout()

# **Gerar Timestamp para o nome do arquivo**
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f'{timestamp}_network_graph_interacao_grupo.png' # Nome do arquivo com timestamp
plt.savefig(filename, facecolor=plt.gcf().get_facecolor(), edgecolor=plt.gcf().get_edgecolor(), transparent=False)
 # Salvar gráfico com timestamp no nome do arquivo

plt.show()

# 5. Imprimir Resultados da Centralidade de Grau (Ordenado)
print("Centralidade de Grau dos Membros (Ordenada):\n")
centralidade_ordenada = sorted(centralidade_grau.items(), key=lambda item: item[1], reverse=True)
for membro, centralidade in centralidade_ordenada:
    print(f"{membro}: {centralidade:.4f}")
