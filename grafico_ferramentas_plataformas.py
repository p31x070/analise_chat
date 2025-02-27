import matplotlib.pyplot as plt
import pandas as pd
import datetime

# 1. Dados para o Gráfico de Barras - DEFINIDOS DIRETAMENTE NO CÓDIGO
ferramentas_plataformas = ['DeepSeek', 'Perplexity AI', 'Obsidian', 'ChatGPT', 'Zotero', 'Google AI Studio/Gemini', 'Claude', 'Ollama', 'Outras Ferramentas'] # Ferramentas e Plataformas em Português
frequencia_mencoes = [30, 20, 20, 15, 10, 10, 8, 5, 12] # Frequências aproximadas de menção

# 2. Criar DataFrame Pandas
df_ferramentas = pd.DataFrame({'Ferramenta/Plataforma': ferramentas_plataformas, 'Frequência de Menções': frequencia_mencoes})
df_ferramentas = df_ferramentas.sort_values(by='Frequência de Menções', ascending=False) # Ordenar por frequência

# 3. Gerar Gráfico de Barras
plt.figure(figsize=(14, 7))
bars = plt.bar(df_ferramentas['Ferramenta/Plataforma'], df_ferramentas['Frequência de Menções'], color='coral')

# 4. Configurações do Gráfico (em Português)
plt.title('Frequência de Ferramentas e Plataformas de IA Mencionadas', fontsize=14)
plt.xlabel('Ferramentas e Plataformas de IA', fontsize=12)
plt.ylabel('Frequência de Menções (Contagem Aproximada)', fontsize=12)
plt.xticks(rotation=45, ha='right') # Rotacionar rótulos do eixo X
plt.grid(axis='y') # Grade no eixo Y

# Adicionar Legenda (Opcional, mas útil)
plt.legend(bars, ['Contagem Aproximada de Menções no Log de Chat'], title='Legenda', loc='upper right')

plt.tight_layout()

# 5. Salvar o Gráfico em Arquivo PNG
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f'{timestamp}_tool_platform_frequency_pt_standalone.png' # Nome do arquivo com timestamp
plt.savefig(filename) # Salvar com nome significativo
plt.show()

print("Gráfico de frequência de ferramentas e plataformas gerado e salvo como 'tool_platform_frequency_pt_standalone.png'")