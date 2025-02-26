import re
import pandas as pd
from datetime import datetime, timedelta
import json # Importar biblioteca json

chat_file = "Conversa do WhatsApp com Núcleo de Estudos IA Generativa Aplicada ao Direito.txt" # Seu arquivo de chat

# Carregar dicionário de palavras-chave de topic_keywords.json - MODIFICADO
with open('topic_keywords.json', 'r', encoding='utf-8') as f: # Carrega topic_keywords.json
    topic_keywords_expandido = json.load(f)

def get_hierarchical_topic(message_text, topic_keywords_hierarchical): # Função para classificação hierárquica - MODIFICADA para retornar subtema
    message_text_lower = message_text.lower()
    for top_topic, subtopics in topic_keywords_hierarchical.items():
        if isinstance(subtopics, dict): # **Adicionado: Check if subtopics is a dictionary**
            for subtopic, keywords in subtopics.items():
                for keyword in keywords:
                    if keyword in message_text_lower:
                        return top_topic, subtopic  # Retorna TÓPICO PRINCIPAL e SUBTÓPICO quando encontra correspondência
        else: # **Debugging: If subtopics is NOT a dict, print a warning**
            print(f"Warning: Subtopics for '{top_topic}' is NOT a dictionary! Type: {type(subtopics)}")
    return 'Outros', None  # Retorna 'Outros' para tópico principal e None para subtema se não houver correspondência - CORRIGIDO

def extract_messages_with_topics_from_whatsapp_log(file_path, topic_keywords_hierarchical):
    messages_with_topics = [] # Lista para armazenar mensagens com tópicos
    last_assigned_topic = ('Outros', None) # Inicializa o tópico anterior como 'Outros' e subtema None
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                match = re.match(r'(\d{2}/\d{2}/\d{4} \d{2}:\d{2}) - (.*?): (.*)', line)
                if match:
                    date_time_str, sender, message_text = match.groups()

                    # Ignorar mensagens de sistema, apagadas e iniciais
                    if "Mídia oculta" not in message_text and "Mensagem apagada" not in message_text and not message_text.startswith("As mensagens e as ligações são protegidas"):

                        topico_principal, subtopico = get_hierarchical_topic(message_text, topic_keywords_hierarchical) # Recebe ambos (MODIFICADO)


                        if topico_principal == 'Outros' and last_assigned_topic[0] != 'Outros': # Herança de tópico principal (MODIFICADO para acessar o tópico principal da tupla)
                            topico_principal = last_assigned_topic[0]
                            subtopico = None # Subtema não é herdado, permanece None

                        messages_with_topics.append({'Mensagem': message_text, 'Tópico': topico_principal, 'Subtópico': subtopico}) # Armazenar mensagem com tópico e subtopico (MODIFICADO)
                        last_assigned_topic = (topico_principal, subtopico) # Atualiza ambos (MODIFICADO para tupla)


    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado: {file_path}")
        return None
    return messages_with_topics # Retorna apenas mensagens com tópicos


# Extrair mensagens com tópicos do log do chat
messages_topics_grupo = extract_messages_with_topics_from_whatsapp_log(chat_file, topic_keywords_expandido) # Usar topic_keywords_expandido

if messages_topics_grupo: # Salvar mensagens com tópicos
    df_mensagens_temas = pd.DataFrame(messages_topics_grupo)
    print("DataFrame df_mensagens_temas gerado com sucesso.")
    df_mensagens_temas.to_csv('chat_messages_temas_grupo.csv', index=False, encoding='utf-8', sep=',')
    print("DataFrame df_mensagens_temas salvo em 'chat_messages_temas_grupo.csv'")
else:
    print("Não foi possível extrair mensagens com tópicos do arquivo.")