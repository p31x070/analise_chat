import re
import pandas as pd
from datetime import datetime, timedelta

chat_file = "Conversa do WhatsApp com Núcleo de Estudos IA Generativa Aplicada ao Direito.txt" # Seu arquivo de chat

# Dicionário de palavras-chave para tópicos EXPANDIDO - Nova variável
topic_keywords_expandido = {
    'Ferramentas e Plataformas': {
        'Geral': ['ferramentas', 'plataformas', 'software', 'aplicativos', 'sistemas', 'soluções', 'ferramenta', 'plataforma'],
        'Obsidian': ['obsidian', 'anotações', 'notas', 'segundo cérebro', 'smart connections', 'plugin', 'vault'],
        'Zotero': ['zotero', 'bibliografia', 'referências', 'citações', 'artigos', 'livros', 'fontes', 'fichamento'],
        'LLMs e Modelos': ['perplexity', 'deepseek', 'chatgpt', 'ollama', 'gemini', 'claude', 'gpt-4', 'gpt-3', 'llm', 'modelos de linguagem', 'ai generativa', 'deep seek', 'deepseek-r1', 'gemini flash', 'gpt o1', 'gpt o3', 'gpt 3.5', 'gpt 4o', 'gpt4o mini', 'deepseek-v3', 'deepseek v.3', 'deepseek r1', 'claude 3 opus', 'claude 3.5 sonnet', 'deepseek-r1-lite-preview', 'r1-lite-preview', 'r1'],
        'IDEs com LLM': ['aider', 'vscode', 'cursor', 'windsurf', 'ide com llm'],
        'Código e Bibliotecas': ['código', 'bibliotecas', 'python', 'javascript', 'js', 'sdk', 'api', 'apis', 'api pública', 'api gratuita', 'api do whatsapp']
    },
    'Aplicações Jurídicas Práticas': {
        'Pesquisa Jurídica e Jurisprudencial': ['jurisprudência', 'precedentes', 'stj', 'stf', 'cnj', 'datajud', 'escavador', 'jusbrasil', 'buscas', 'informativos', 'ementas', 'precedente qualificado', 'repetitivos', 'paradigmáticos', 'acórdam', 'acórdão'],
        'Documentos Jurídicos e Peças Processuais': ['contrato', 'petição', 'parecer', 'inicial', 'recurso', 'sentença', 'decisão', 'documentos', 'peças', 'minutas', 'relatórios', 'cláusulas', 'instrumento', 'procuração', 'prececentes'], # Adicionado 'prececentes'
        'Processos e Fluxos de Trabalho Jurídicos': ['processo', 'fluxo de trabalho', 'automação', 'tarefas repetitivas', 'eficiência', 'produtividade', 'celeridade', 'rotina', 'gestão', 'workflow', 'etapas', 'threads', 'paralelo', 'computador humano', 'cluster jurídico humano', 'cluster jurídico', 'girlpower', 'gp'],
        'Áreas do Direito': ['direito bancário', 'direito consumidor', 'direito tributário', 'direito ambiental', 'direito constitucional', 'direito penal', 'direito civil', 'direito do trabalho', 'direito empresarial', 'direito digital', 'direito tecnologia', 'direito eleitoral', 'direito previdenciário', 'direito médico', 'direito administrativo', 'direito autoral', 'direito imobiliário', 'direito internacional', 'direito medico'] # Adicionado 'direito medico'
    },
    'Código Aberto e Custo': {
        'Open Source e Transparência': ['opensource', 'código aberto', 'aberto', 'comunidade', 'gratuito', 'free', 'licença aberta', 'transparência', 'controle', 'engenharia aberta', 'modelo aberto', 'open source'],
        'Custo e Viabilidade Econômica': ['custo', 'preço', 'barato', 'grátis', 'economia', 'orçamento', 'investimento', 'api gratuita', 'plano gratuito', 'versão gratuita', 'conta', 'gratuita', 'grátis', 'assinatura', 'mensalidade', 'dólares', 'reais', 'pagar', 'pago', 'paga']
    },
    'Conceitos Técnicos e Fundamentos de IA': {
        'Fundamentos de IA e LLMs': ['algoritmo', 'redes neurais', 'machine learning', 'deep learning', 'inteligência artificial', 'ia', 'modelo de ia', 'agentes', 'tokens', 'parâmetros', 'llms', 'modelos de linguagem', 'power girl', 'gp', 'agi', 'superinteligência', 'consciência coletiva', 'algoritmos', 'llm', 'rede neural'],
        'Raciocínio, Lógica e Semântica': ['raciocínio', 'razão', 'lógica', 'inferência', 'semântica', 'conhecimento', 'cadeia de raciocínio', 'deep thinking', 'raciocinio avançado', 'raciocínio profundo', 'raciocínio semântico', 'reasoning', 'chain of thought', 'smart connections'],
        'Hardware e Infraestrutura': ['gpu', 'cpu', 'tpu', 'hardware', 'servidores', 'nuvem', 'local', 'raspberry pi', 'orange pi', 'edge computing', 'nvidia jetson', 'gpu', 'tpu', 'vram', 'memória ram', 'processamento', 'computador', 'servidor', 'infraestrutura']
    },
    'Questões Éticas, Regulatórias e Sociais': {
        'Ética e Moralidade em IA': ['ética', 'moral', 'valores', 'responsabilidade', 'transparência', 'vieses', 'justiça', 'equidade', 'discriminação', 'impacto social', 'ética em ia', 'roboética', 'bioética', 'ética algorítmica', 'ética e ia'],
        'Regulação, Direito e Governança da IA': ['regulação', 'legislação', 'normas', 'lei', 'direitos autorais', 'privacidade', 'lgpd', 'governança', 'controle', 'auditabilidade', 'marcos regulatórios', 'cnj', 'direito e ia', 'direito da ia', 'regulamentação da ia', 'direito digital', 'direito autoral', 'direitos humanos e ia'],
        'Impacto Social e no Trabalho': ['futuro do trabalho', 'mercado de trabalho', 'emprego', 'desemprego', 'automação do trabalho', 'substituição do trabalho humano', 'impacto social da ia', 'impacto da ia no trabalho', 'transformação do trabalho', 'mercado de trabalho da ia']
    },
    'Interdisciplinaridade e Fundamentos Teóricos': {
        'Interdisciplinaridade': ['interdisciplinaridade', 'multidisciplinaridade', 'transdisciplinaridade', 'diálogo', 'integração', 'conexões', 'campos do conhecimento', 'áreas do saber', 'saberes', 'conhecimentos', 'abordagem multidisciplinar', 'abordagem interdisciplinar'],
        'Fundamentos Teóricos': ['teoria', 'teórico', 'conceito', 'definição', 'modelo teórico', 'fundamentos', 'epistemologia', 'paradigma', 'doutrina', 'dogmática', 'dogmático', 'metodologia', 'método', 'abordagem teórica', 'construção teórica'],
        'Matemática e Estatística': ['matemática', 'estatística', 'cálculo', 'probabilidade', 'algebra', 'geometria', 'dados quantitativos', 'dados estatísticos', 'método matemático', 'método estatístico', 'analise matematica', 'análise estatística', 'modelagem matemática', 'modelagem estatística'],
        'Informática e Tecnologia': ['informática', 'tecnologia', 'computação', 'programação', 'código', 'sistema', 'software', 'hardware', 'digital', 'tecnológico', 'computacional', 'programático', 'sistema computacional', 'sistema digital', 'sistema tecnológico'],
        'Filosofia e Humanidades': ['filosofia', 'ética', 'moral', 'humanidades', 'humano', 'existencial', 'ontologia', 'epistemologia', 'hermenêutica', 'fenomenologia', 'filosófico', 'humanístico', 'reflexão filosófica', 'reflexão humanística', 'visão filosófica', 'visão humanística']
    },
    'Outros': ['geral', 'outros', 'diversos', 'variados', 'assuntos gerais', 'comunicação', 'grupo', 'pessoal', 'pessoal,', 'olá', 'opa', 'salve', 'boa tarde', 'bom dia', 'boa noite', 'obrigado', 'obrigada', 'agradeço', 'por favor', 'por gentileza', 'legal', 'muito bom', 'sensacional', 'ótimo', 'excelente', 'parabéns', 'gostei', 'concordo', 'acho', 'creio', 'dúvida', 'dúvidas', 'pergunta', 'perguntas', 'questionamento', 'questionamentos', 'elogios', 'elogio', 'congratulações', 'congratulação']
}

def get_approximate_topic(message_text, topic_keywords): # Função para atribuir tópico aproximado - MANTIDA VERSÃO ANTERIOR
    message_text_lower = message_text.lower()
    for topic, keywords in topic_keywords.items():
        for keyword in keywords:
            if keyword in message_text_lower:
                return topic # Retorna o primeiro tópico que encontrar correspondência
    return 'Outros' # Tópico padrão se não encontrar correspondência

def get_hierarchical_topic(message_text, topic_keywords_hierarchical): # NOVA função para classificação hierárquica
    message_text_lower = message_text.lower()
    for top_topic, subtopics in topic_keywords_hierarchical.items():
        for subtopic, keywords in subtopics.items():
            for keyword in keywords:
                if keyword in message_text_lower:
                    return top_topic  # Retorna o TÓPICO PRINCIPAL (pode ser modificado para retornar subtema se necessário)
    return 'Outros' # Tópico padrão se não encontrar correspondência


def extract_messages_with_topics_from_whatsapp_log(file_path, topic_keywords_hierarchical): # MODIFICADO para usar topic_keywords_hierarchical
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

                        message_topic = get_hierarchical_topic(message_text, topic_keywords_hierarchical) # Usar a NOVA função para classificar

                        if message_topic == 'Outros' and last_assigned_topic != 'Outros': # Se for 'Outros' e o tópico anterior NÃO for 'Outros'
                            message_topic = last_assigned_topic # Herda o tópico anterior

                        messages_with_topics.append({'Mensagem': message_text, 'Tópico': message_topic}) # Armazenar mensagem com tópico
                        last_assigned_topic = message_topic # Atualiza o tópico anterior para o tópico da mensagem atual


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