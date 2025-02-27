# Documentação do Fluxo de Análise de Dados do Grupo

## Visão Geral do Processamento
```mermaid
graph TD
    A[Arquivo .txt do WhatsApp] --> B[gera_mensagens_temas_csv_v2.py]
    B --> C[chat_messages_temas_grupo.csv]
    C --> D1[sentimentos.py]
    C --> D2[interacoes_sociais.py]
    B --> E[topic_keywords.json]
    E --> F[nuvem_palavras_temas.py]
    E --> G[grafico_barras_temas.py]
    E --> H[treemap_topics.py]
    D2 --> I[df_interacoes_ponderadas_temporal_grupo.csv]
    I --> J[analise_rede.py]
    J --> K[Gráficos de Rede]
    D1 --> L[Gráfico de Sentimentos]
    F --> M[Wordclouds Temáticos]
    G --> N[Gráfico de Barras]
    H --> O[Treemap de Tópicos]
    crescimento_membros.py --> P[Gráfico de Crescimento]
```

## 1. Pré-processamento de Dados
**Scripts principais:**
- `gera_mensagens_temas_csv_v2.py`  
  _Entrada:_ `Conversa do WhatsApp...txt` + `topic_keywords.json`  
  _Saída:_ `chat_messages_temas_grupo.csv` (mensagens classificadas por tópico)

## 2. Análise Central
**Módulos:**
- `interacoes_sociais.py`  
  _Entrada:_ Chat original (.txt)  
  _Saída:_ `df_interacoes_ponderadas_temporal_grupo.csv` (interações temporais)

- `sentimentos.py`  
  _Entrada:_ `chat_messages_temas_grupo.csv`  
  _Saída:_ Gráfico de pizza de sentimentos

## 3. Visualizações
**Scripts de geração de gráficos:**
- `analise_rede.py` → Network graphs  
- `nuvem_palavras_temas.py` → Wordclouds temáticos  
- `grafico_barras_temas.py` → Distribuição de tópicos  
- `treemap_topics.py` → Hierarquia de tópicos  
- `crescimento_membros.py` → Evolução de membros

## Ordem Recomendada de Execução
1. Atualizar `topic_keywords.json` (se necessário)
2. Rodar `gera_mensagens_temas_csv_v2.py`
3. Executar análise de sentimentos e interações:
   ```bash
   python sentimentos.py
   python interacoes_sociais.py
   ```
4. Gerar visualizações:
   ```bash
   python analise_rede.py
   python nuvem_palavras_temas.py
   python grafico_barras_temas.py
   python treemap_topics.py
   python crescimento_membros.py
   ```

## Dependências Críticas
- Todos scripts requerem Python 3.8+
- Bibliotecas essenciais: pandas, matplotlib, seaborn, wordcloud
- `topic_keywords.json` deve manter estrutura hierárquica
