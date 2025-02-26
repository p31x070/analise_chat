import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
import datetime # Importar datetime


# 1. Carregar o DataFrame df_interacoes_ponderadas do arquivo CSV
df_interacoes_ponderadas = pd.read_csv('df_interacoes_ponderadas_temporal_grupo.csv') # Carrega do CSV ponderado temporal

# 2. Construir o Grafo Ponderado
grafo_ponderado_grupo = nx.Graph() # Grafo não direcionado

# Adicionar arestas ponderadas ao grafo a partir do DataFrame de interações ponderadas
for index, row in df_interacoes_ponderadas.iterrows():
    responder = row['Responder']
    respondido_por = row['Respondido_por']
    peso = row['Peso'] # Obter o peso da interação
    grafo_ponderado_grupo.add_edge(responder, respondido_por, weight=peso) # Adicionar aresta com peso

# 3. Calcular a Centralidade de Grau Ponderada (Weighted Degree Centrality)
centralidade_grau_ponderada = nx.degree_centrality(grafo_ponderado_grupo)

# 4. Visualizar a Rede Ponderada com Estilo Personalizado
fig, ax1 = plt.subplots(figsize=(14, 10), facecolor='darkgreen') # Definir facecolor na criação da figura
fig.patch.set_facecolor('darkgreen') # **Adicionado**: Definir facecolor diretamente no patch da figura

ax = fig.add_subplot(111) # Adicionar subplot ao invés de plt.subplots (mais controle sobre a figura base)
ax.set_facecolor('darkgreen') # Definir cor de fundo dos eixos (subplot) - Manter esta linha

pos = nx.spring_layout(grafo_ponderado_grupo, k=0.3, iterations=50)
edges = grafo_ponderado_grupo.edges(data=True) # Obter arestas com dados (pesos)
weights = [edge_data['weight'] for _, _, edge_data in edges] # Extrair pesos para espessura das arestas

nx.draw(grafo_ponderado_grupo, pos,
        ax=ax, # Especificar explicitamente os eixos 'ax' para nx.draw
        with_labels=True,
        node_size=[v * 8000 for v in centralidade_grau_ponderada.values()],
        node_color='lightgreen', # Define nodos verde claro
        edge_color='lightgray', # Cor das arestas alterada para cinza claro para melhor contraste
        width=weights, # Usar pesos para espessura das arestas
        alpha=0.7,
        font_size=10,
        font_color='black', # Cor da fonte alterada para branco para melhor contraste com fundo escuro
        font_weight='bold')

plt.title('Rede de Interação Ponderada entre Membros do Grupo', fontsize=16, color='black') # Título em branco
plt.xlabel('Membros (Nós)', fontsize=12, color='black') # Rótulo do eixo X em branco
plt.ylabel('Interações Ponderadas (Arestas)', fontsize=12, color='black')


# Ajustar cor dos ticks dos eixos para branco para contraste com fundo escuro
ax.tick_params(axis='x', colors='black')
ax.tick_params(axis='y', colors='black')
ax.spines['bottom'].set_color('black')
ax.spines['top'].set_color('black')
ax.spines['left'].set_color('black')
ax.spines['right'].set_color('black')


# **Gerar Timestamp para o nome do arquivo**
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f'{timestamp}_network_graph_interacao_ponderada_grupo_verde.png' # Nome do arquivo com timestamp
plt.savefig(filename, facecolor=fig.get_facecolor()) # Salvar imagem com fundo verde escuro e timestamp

plt.show()

# 5. Imprimir Resultados da Centralidade de Grau Ponderada (Ordenada) - (sem alterações)
print("Centralidade de Grau Ponderada dos Membros (Ordenada):\n")
centralidade_ordenada_ponderada = sorted(centralidade_grau_ponderada.items(), key=lambda item: item[1], reverse=True)
for membro, centralidade in centralidade_ordenada_ponderada:
    print(f"{membro}: {centralidade:.4f}")