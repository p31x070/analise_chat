import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib

# 1. Carregar o DataFrame df_interacoes do arquivo CSV
df_interacoes = pd.read_csv('df_interacoes_grupo.csv') # Carrega o DataFrame do arquivo CSV

# 2. Construir o Grafo (Rede) - (o restante do código permanece quase o mesmo)
grafo_interacao_grupo = nx.Graph() # Grafo não direcionado

# Adicionar arestas ao grafo a partir do DataFrame de interações
for index, row in df_interacoes.iterrows():
    responder = row['Responder']
    respondido_por = row['Respondido_por']
    grafo_interacao_grupo.add_edge(responder, respondido_por)

# 3. Calcular a Centralidade de Grau
centralidade_grau = nx.degree_centrality(grafo_interacao_grupo)

# 4. Visualizar a Rede
plt.figure(figsize=(14, 10))
pos = nx.spring_layout(grafo_interacao_grupo, k=0.3, iterations=50) # Layout para melhor visualização, ajuste k e iterations se necessário
nx.draw(grafo_interacao_grupo, pos,
        with_labels=True,
        node_size=[v * 8000 for v in centralidade_grau.values()], # Tamanho dos nós proporcional à centralidade de grau
        node_color='skyblue',
        edge_color='gray',
        alpha=0.7,
        font_size=10,
        font_weight='bold',
        width=0.5)

plt.title('Rede de Interação entre Membros do Grupo', fontsize=16)
plt.xlabel('Membros (Nós)', fontsize=12)
plt.ylabel('Interações (Arestas)', fontsize=12)
plt.savefig('network_graph_interacao_grupo.png') # Salvar imagem
plt.show()

# 5. Imprimir Resultados da Centralidade de Grau (Ordenado)
print("Centralidade de Grau dos Membros (Ordenada):\n")
centralidade_ordenada = sorted(centralidade_grau.items(), key=lambda item: item[1], reverse=True) # Ordenar por centralidade
for membro, centralidade in centralidade_ordenada:
    print(f"{membro}: {centralidade:.4f}") # Formatar para 4 casas decimais