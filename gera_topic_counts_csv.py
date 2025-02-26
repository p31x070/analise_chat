import pandas as pd

# 1. Carregar DataFrame df_mensagens_temas do arquivo CSV
df_mensagens_temas = pd.read_csv('chat_messages_temas_grupo.csv') # Carrega mensagens com tópicos

# 2. Aggregate Topic Frequencies
topic_counts = df_mensagens_temas['Tópico'].value_counts()
df_topic_counts = pd.DataFrame({'Tópico': topic_counts.index, 'Frequência': topic_counts.values})

# Salvar df_topic_counts para CSV
df_topic_counts.to_csv('topic_frequency_messages_bar_chart_data.csv', index=False, encoding='utf-8')
print("DataFrame df_topic_counts salvo em 'topic_frequency_messages_bar_chart_data.csv'") # Confirmation message

print("\nFrequência de Tópicos de Discussão (Ordenada):\n")
print(df_topic_counts.to_string(index=False))