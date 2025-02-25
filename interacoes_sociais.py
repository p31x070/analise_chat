import re
import pandas as pd

chat_file = "Conversa do WhatsApp com Núcleo de Estudos IA Generativa Aplicada ao Direito.txt" # Seu arquivo de chat

def extract_interactions_from_whatsapp_log(file_path):
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
                        if last_sender and last_sender != current_sender:
                            interactions.append((last_sender, current_sender)) # Adiciona interação: quem respondeu (last_sender) -> quem foi respondido (current_sender)
                        last_sender = current_sender
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado: {file_path}")
        return None
    return interactions

# Extrair interações do log do chat
interacoes_grupo = extract_interactions_from_whatsapp_log(chat_file)

if interacoes_grupo:
    df_interacoes = pd.DataFrame(interacoes_grupo, columns=['Responder', 'Respondido_por'])
    print("DataFrame df_interacoes gerado com sucesso.")

    # Salvar df_interacoes para um arquivo CSV
    df_interacoes.to_csv('df_interacoes_grupo.csv', index=False) # Salva sem o índice do DataFrame
    print("DataFrame df_interacoes salvo em 'df_interacoes_grupo.csv'")

else:
    print("Não foi possível extrair interações do arquivo.")