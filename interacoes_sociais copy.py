import re
import pandas as pd

chat_file = "Conversa do WhatsApp com Núcleo de Estudos IA Generativa Aplicada ao Direito.txt" # Seu arquivo de chat

def extract_messages_from_whatsapp_log(file_path):
    messages = []
    interactions = []
    last_sender = None
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                match = re.match(r'(\d{2}/\d{2}/\d{4} \d{2}:\d{2}) - (.*?): (.*)', line)
                if match:
                    date_time, sender, message_text = match.groups()
                    current_sender = sender.strip() # Remover espaços extras
                    # Ignorar mensagens de sistema, apagadas e mensagens iniciais
                    if "Mídia oculta" not in message_text and "Mensagem apagada" not in message_text and not message_text.startswith("As mensagens e as ligações são protegidas"):
                        messages.append(message_text) # Adiciona a mensagem para análise de sentimento
                        if last_sender and last_sender != current_sender:
                            interactions.append((last_sender, current_sender)) # Adiciona interação
                        last_sender = current_sender
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado: {file_path}")
        return None, None # Retorna None para ambos em caso de erro
    return messages, interactions

# Extrair mensagens e interações do log do chat
chat_messages, interacoes_grupo = extract_messages_from_whatsapp_log(chat_file)

if chat_messages:
    print("First 10 extracted chat_messages (example):\n", chat_messages[:10]) # Debug: Print first 10 messages

    df_mensagens = pd.DataFrame({'Mensagem': chat_messages}) # DataFrame para mensagens
    print("DataFrame df_mensagens gerado com sucesso.")

    # Debugging: Print df_mensagens.head() to console *before* saving to CSV
    print("Head of df_mensagens before saving to CSV:\n", df_mensagens.head().to_string())

    df_mensagens.to_csv('chat_messages_grupo.csv', index=False, encoding='utf-8', sep=',') # Explicit CSV parameters: delimiter and encoding
    print("DataFrame df_mensagens salvo em 'chat_messages_grupo.csv'")
else:
    print("Não foi possível extrair mensagens do arquivo.")

if interacoes_grupo:
    df_interacoes = pd.DataFrame(interacoes_grupo, columns=['Responder', 'Respondido_por']) # DataFrame para interações
    print("DataFrame df_interacoes gerado com sucesso.")
    df_interacoes.to_csv('df_interacoes_grupo.csv', index=False) # Salva df_interacoes para CSV
    print("DataFrame df_interacoes salvo em 'df_interacoes_grupo.csv'")
else:
    print("Não foi possível extrair interações do arquivo.")