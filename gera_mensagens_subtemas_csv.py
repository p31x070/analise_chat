import re
import pandas as pd
from datetime import datetime, timedelta
import json  # Importar biblioteca json

chat_file = "Conversa do WhatsApp com Núcleo de Estudos IA Generativa Aplicada ao Direito.txt" # Seu arquivo de chat

# Carregar dicionário de palavras-chave de topic_keywords.json - MODIFICADO
with open('topic_keywords.json', 'r', encoding='utf-8') as f:
    topic_keywords_expandido = json.load(f)

# Debugging: Print type and keys of topic_keywords_expandido - ADICIONADO
print("Debugging: topic_keywords_expandido type:", type(topic_keywords_expandido))
print("Debugging: topic_keywords_expandido keys:", topic_keywords_expandido.keys())

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
    return None, None  # Retorna None, None se não houver correspondência - CORRIGIDO para retornar None, None

def extract_messages_with_subtopics_from_whatsapp_log(file_path, topic_keywords_hierarchical): # MODIFICADO - Nome da função e para retornar df_mensagens_subtemas
    messages_subtemas_list = [] # MODIFICADO - Lista para armazenar dicionários para df_mensagens_subtemas
    last_assigned_topic = ('Outros', None) # Inicializa o tópico anterior como 'Outros' e subtema None
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                match = re.match(r'(\d{2}/\d{2}/\d{4} \d{2}:\d{2}) - (.*?): (.*)', line)
                if match:
                    date_time_str, sender, message_text = match.groups()
                    current_datetime = datetime.strptime(date_time_str, '%d/%m/%Y %H:%M') # Converter string para datetime object

                    # Ignorar mensagens de sistema, apagadas e iniciais
                    if "Mídia oculta" not in message_text and "Mensagem apagada" not in message_text and not message_text.startswith("As mensagens e as ligações são protegidas"):

                        topico_principal, subtopico = get_hierarchical_topic(message_text, topic_keywords_hierarchical) # Recebe ambos (MODIFICADO)


                        if topico_principal is not None and last_assigned_topic[0] != 'Outros': # Herança de tópico principal - MODIFICADO para verificar None
                            if topico_principal is None: # **MODIFICADO**: Herda apenas se o tópico atual NÃO foi classificado
                                topico_principal = last_assigned_topic[0]
                                subtopico = None # Subtema não é herdado, permanece None
                        elif topico_principal is None: # **MODIFICADO**: Se o tópico principal AINDA é None após herança, define como 'Outros'
                            topico_principal = 'Outros' # Define como 'Outros' se não foi possível classificar
                            subtopico = None

                        messages_subtemas_list.append({'Mensagem': message_text, 'Tópico': topico_principal, 'Subtópico': subtopico, 'Data': current_datetime, 'Remetente': sender.strip()}) # MODIFICADO - Adiciona ao messages_subtemas_list
                        last_assigned_topic = (topico_principal, subtopico) # Atualiza ambos (MODIFICADO para tupla)


    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado: {file_path}")
        return None
    return messages_subtemas_list # MODIFICADO - Retorna messages_subtemas_list


# Extrair mensagens com tópicos do log do chat
messages_subtemas_grupo = extract_messages_with_subtopics_from_whatsapp_log(chat_file, topic_keywords_expandido) # MODIFICADO - Usar nova função e variável para DataFrame


if messages_subtemas_grupo: # Salvar mensagens com tópicos
    df_mensagens_subtemas = pd.DataFrame(messages_subtemas_grupo) # MODIFICADO - Nome do DataFrame para df_mensagens_subtemas
    print("DataFrame df_mensagens_subtemas gerado com sucesso.") # MODIFICADO - Menciona df_mensagens_subtemas
    df_mensagens_subtemas.to_csv('chat_messages_subtemas_grupo.csv', index=False, encoding='utf-8') # MODIFICADO - Nome do arquivo CSV para chat_messages_subtemas_grupo.csv
    print("DataFrame df_mensagens_subtemas salvo em 'chat_messages_subtemas_grupo.csv'") # MODIFICADO - Menciona df_mensagens_subtemas
else:
    print("Não foi possível extrair mensagens com subtemas do arquivo.") # MODIFICADO - Mensagem ajustada