import re
import pandas as pd
from datetime import datetime, timedelta

chat_file = "Conversa do WhatsApp com Núcleo de Estudos IA Generativa Aplicada ao Direito.txt" # Seu arquivo de chat

# Dicionário de palavras-chave para tópicos
topic_keywords = {
    'Ferramentas e Plataformas': ['obsidian', 'zotero', 'perplexity', 'deepseek', 'chatgpt', 'ollama', 'api', 'github', 'zotero', 'vercel'],
    'Aplicações Jurídicas Práticas': ['jurisprudência', 'precedentes', 'contrato', 'petição', 'parecer', 'audiência', 'cnj', 'stj', 'stf', 'datajud', 'escavador', 'jusbrasil', 'processo'],
    'Código Aberto e Custo': ['opensource', 'código aberto', 'gratuito', 'barato', 'custo', 'preço', 'api gratuita', 'deepseek v3', 'modelo aberto'],
    'Conceitos Técnicos': ['algoritmo', 'llm', 'redes neurais', 'tokens', 'raciocínio', 'clustering', 'machine learning', 'deep learning', 'power girl', 'inteligência artificial'],
    'Questões Éticas e Regulatórias': ['ética', 'regulação', 'lgpd', 'direitos autorais', 'vieses', 'segurança', 'privacidade', 'carta ética']
}

def get_approximate_topic(message_text, topic_keywords): # Função para atribuir tópico aproximado
    message_text_lower = message_text.lower()
    for topic, keywords in topic_keywords.items():
        for keyword in keywords:
            if keyword in message_text_lower:
                return topic # Retorna o primeiro tópico que encontrar correspondência
    return 'Outros' # Tópico padrão se não encontrar correspondência


def extract_messages_with_topics_from_whatsapp_log(file_path, topic_keywords):
    messages_with_topics = [] # Lista para armazenar mensagens com tópicos
    last_assigned_topic = 'Outros' # Inicializa o tópico anterior como 'Outros' ou None
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                match = re.match(r'(\d{2}/\d{2}/\d{4} \d{2}:\d{2}) - (.*?): (.*)', line)
                if match:
                    date_time_str, sender, message_text = match.groups()

                    # Ignorar mensagens de sistema, apagadas e iniciais
                    if "Mídia oculta" not in message_text and "Mensagem apagada" not in message_text and not message_text.startswith("As mensagens e as ligações são protegidas"):

                        message_topic = get_approximate_topic(message_text, topic_keywords) # Tenta classificar o tópico da mensagem atual

                        if message_topic == 'Outros' and last_assigned_topic != 'Outros': # Se for 'Outros' e o tópico anterior NÃO for 'Outros'
                            message_topic = last_assigned_topic # Herda o tópico anterior

                        messages_with_topics.append({'Mensagem': message_text, 'Tópico': message_topic}) # Armazenar mensagem com tópico
                        last_assigned_topic = message_topic # Atualiza o tópico anterior para o tópico da mensagem atual


    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado: {file_path}")
        return None
    return messages_with_topics # Retorna apenas mensagens com tópicos


# Extrair mensagens com tópicos do log do chat
messages_topics_grupo = extract_messages_with_topics_from_whatsapp_log(chat_file, topic_keywords) # Passa topic_keywords para a função

if messages_topics_grupo: # Salvar mensagens com tópicos
    df_mensagens_temas = pd.DataFrame(messages_topics_grupo)
    print("DataFrame df_mensagens_temas gerado com sucesso.")
    df_mensagens_temas.to_csv('chat_messages_temas_grupo.csv', index=False, encoding='utf-8', sep=',')
    print("DataFrame df_mensagens_temas salvo em 'chat_messages_temas_grupo.csv'")
else:
    print("Não foi possível extrair mensagens com tópicos do arquivo.")