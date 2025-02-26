#!/bin/bash

# Script para adicionar stopwords ao arquivo stopwords-pt.txt

STOPWORDS_FILE="stopwords-pt.txt"

if [ ! -f "$STOPWORDS_FILE" ]; then
  echo "Erro: Arquivo $STOPWORDS_FILE não encontrado."
  exit 1
fi

echo "Adicionando stopwords ao arquivo $STOPWORDS_FILE..."

# Lista de stopwords adicionais PREDEFINIDAS NO SCRIPT
STOPWORDS_TO_ADD=(
  jpg img "arquivo anexado" del pdf html https www http link href url mídia oculta vídeo áudio webp
  periodicos uninove br riae article download scielo ufrj bitstream 11422 14360 1 rcoliveira
  periodicos.uninove.br
  pessoal olá opa salve "boa tarde" "bom dia" "boa noite" obrigado obrigada agradeço "por favor" "por gentileza" legal "muito bom" sensacional ótimo excelente parabéns gostei concordo acho creio dúvida dúvidas pergunta perguntas questionamento questionamentos elogios elogio congratulações congratulação # Palavras "perturbadoras" adicionadas
  "tudo bem" gente aqui aí né sim não ok blz valeu abraços # Mais palavras "perturbadoras" genéricas
  area éramos és último # Novas palavras "perturbadoras" do print final do arquivo stopwords-pt.txt
  vem vão vos zero a às # Novas palavras "perturbadoras" do print final do arquivo stopwords-pt.txt - CONTINUAÇÃO
)

# Primeiro, processar stopwords PREDEFINIDAS no array STOPWORDS_TO_ADD
echo "Processando stopwords predefinidas..."
for word in "${STOPWORDS_TO_ADD[@]}"; do 
  word_lower=$(echo "$word" | tr '[:upper:]' '[:lower:]')
  grep -q -F -x "$word_lower" "$STOPWORDS_FILE"
  if [ $? -ne 0 ]; then 
    echo "Adicionada (predefinida): $word_lower"
    echo "$word_lower" >> "$STOPWORDS_FILE"
  else
    echo "Palavra já existe (predefinida, ignorada): $word_lower"
  fi
done

# Depois, processar stopwords FORNECIDAS COMO ARGUMENTOS (se houver) - REINTRODUZIDO LOOP DE ARGUMENTOS
if [ ! -z "$1" ]; then # Check IF arguments were provided
  echo "\nProcessando stopwords fornecidas como argumentos..."
  for word in "$@"; do # Loop through command line arguments AGAIN
    word_lower=$(echo "$word" | tr '[:upper:]' '[:lower:]')
    grep -q -F -x "$word_lower" "$STOPWORDS_FILE"
    if [ $? -ne 0 ]; then
      echo "Adicionada (argumento): $word_lower"
      echo "$word_lower" >> "$STOPWORDS_FILE"
    else
      echo "Palavra já existe (argumento, ignorada): $word_lower"
    fi
  done
fi

echo "\nProcesso concluído."