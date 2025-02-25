import re
import pandas as pd
from datetime import datetime, timedelta

chat_file = "Conversa do WhatsApp com Núcleo de Estudos IA Generativa Aplicada ao Direito.txt" # Seu arquivo de chat
time_threshold_minutes = 5 # Limite de tempo em minutos para considerar interação "próxima" e aumentar o peso

def extract_weighted_interactions_from_whatsapp_log(file_path):
    interactions_weighted = []
    last_sender = None
    last_datetime = None
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                match = re.match(r'(\d{2}/\d{2}/\d{4} \d{2}:\d{2}) - (.*?): (.*)', line)
                if match:
                    date_time_str, sender, message_text = match.groups()
                    current_datetime = datetime.strptime(date_time_str, '%d/%m/%Y %H:%M')
                    current_sender = sender.strip()

                    # Ignorar mensagens de sistema, apagadas e iniciais
                    if "Mídia oculta" not in message_text and "Mensagem apagada" not in message_text and not message_text.startswith("As mensagens e as ligações são protegidas"):
                        interaction_weight = 1 # Peso padrão
                        if last_sender and last_sender != current_sender and last_datetime:
                            time_diff = current_datetime - last_datetime
                            if time_diff <= timedelta(minutes=time_threshold_minutes):
                                interaction_weight = 2 # Peso maior se interação for próxima no tempo

                            interactions_weighted.append({'Responder': last_sender, 'Respondido_por': current_sender, 'Peso': interaction_weight})

                        last_sender = current_sender
                        last_datetime = current_datetime # Atualiza o datetime da última mensagem
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado: {file_path}")
        return None
    return interactions_weighted

# Extrair interações ponderadas do log do chat
interacoes_grupo_ponderadas = extract_weighted_interactions_from_whatsapp_log(chat_file)

if interacoes_grupo_ponderadas:
    df_interacoes_ponderadas = pd.DataFrame(interacoes_grupo_ponderadas)
    print("DataFrame df_interacoes_ponderadas gerado com sucesso.")
    df_interacoes_ponderadas.to_csv('df_interacoes_ponderadas_grupo.csv', index=False) # Salva df_interacoes_ponderadas para CSV
    print("DataFrame df_interacoes_ponderadas salvo em 'df_interacoes_ponderadas_grupo.csv'")

    # Exemplo de Contagem de interações ponderadas (opcional)
    contagem_interacoes_ponderadas = df_interacoes_ponderadas.groupby(['Responder', 'Respondido_por'])['Peso'].sum().reset_index(name='Peso')
    print("\nContagem de Interações Ponderadas (Exemplo):\n", contagem_interacoes_ponderadas.head())

else:
    print("Não foi possível extrair interações ponderadas do arquivo.")

# (Mantenha a parte para salvar df_mensagens.csv se você ainda estiver usando o script sentimentos.py)
# if chat_messages:
#     df_mensagens = pd.DataFrame({'Mensagem': chat_messages}) # DataFrame para mensagens
#     df_mensagens.to_csv('chat_messages_grupo.csv', index=False, encoding='utf-8', sep=',') # Salva df_mensagens para CSV