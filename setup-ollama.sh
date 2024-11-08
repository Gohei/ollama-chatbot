#!/bin/bash

# Ollamaコンテナを起動する
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

# コンテナの起動を待機する
sleep 10

# モデルをダウンロードする
docker exec ollama ollama pull tinyllama