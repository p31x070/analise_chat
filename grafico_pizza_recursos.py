import matplotlib.pyplot as plt
import pandas as pd
import datetime

chat_file = "Conversa do WhatsApp com Núcleo de Estudos IA Generativa Aplicada ao Direito.txt" # Seu arquivo de chat

def analyze_resource_types_from_whatsapp_log(file_path):
    document_count = 0
    link_count = 0
    media_count = 0
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line_lower = line.lower()
                if ".pdf" in line_lower or ".ots" in line_lower: # Very basic keyword check for documents
                    document_count += 1
                elif "http://" in line_lower or "https://" in line_lower: # Basic check for links
                    link_count += 1
                elif "webp (arquivo anexado)" in line_lower or "imagem" in line_lower or "vídeo" in line_lower or "<mídia oculta>" in line_lower or "(arquivo anexado)" in line_lower and (".jpg" in line_lower or ".png" in line_lower or ".jpeg" in line_lower or ".mp4" in line_lower or ".mov" in line_lower or ".mpeg" in line_lower): # Basic check for media
                    media_count += 1 # Improved media detection keywords
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado: {file_path}")
        return None

    return {'Documents': document_count, 'Links': link_count, 'Media (Audio/Video/Images)': media_count}


resource_counts = analyze_resource_types_from_whatsapp_log(chat_file)

if resource_counts:
    df_resources = pd.DataFrame(list(resource_counts.items()), columns=['Resource Type', 'Count'])

    # Plotting Pie Chart
    plt.figure(figsize=(8, 8))
    plt.pie(df_resources['Count'], labels=df_resources['Resource Type'], autopct='%1.1f%%', startangle=140, colors=['lightcoral', 'lightskyblue', 'lightgreen'])
    plt.title('Distribuição de Tipos de Recursos Compartilhados', fontsize=14)
    plt.tight_layout()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'{timestamp}resource_types.png' # Nome do arquivo com timestamp
    plt.savefig(filename) # Save pie chart to file
    plt.show()

    print("\nContagem de Tipos de Recursos:\n", df_resources.to_string(index=False))
else:
    print("Não foi possível analisar os tipos de recursos do arquivo.")