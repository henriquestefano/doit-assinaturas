#!/bin/bash
# Dois cliques para publicar no GitHub

cd "$(dirname "$0")"

echo "📦 Adicionando alterações..."
git add .

echo "💬 Criando commit..."
git commit -m "Atualização automática - $(date '+%d/%m/%Y %H:%M')"

echo "🚀 Enviando para o GitHub..."
git push origin main

echo ""
echo "✅ Projeto atualizado com sucesso!"
echo "🌐 Acesse: https://henriquestefano.github.io/doit-assinaturas"
echo ""
read -p "Pressione Enter para fechar..."
