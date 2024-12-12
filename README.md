# Transcrição de Áudio para Texto

Uma aplicação web para transcrição de áudio e vídeo para texto usando Python, Flask e Google Speech Recognition.

## Funcionalidades

- Upload de arquivos de áudio/vídeo via interface web
- Suporte para múltiplos formatos (.wav, .mp3, .flac, .opus, .mp4, .avi, .mov, .mkv)
- Transcrição automática usando Google Speech Recognition
- Interface moderna e responsiva
- Funcionalidade de copiar texto com um clique

## Requisitos

- Python 3.12+
- Flask
- SpeechRecognition
- pydub
- moviepy
- colorama

## Instalação

1. Clone o repositório:
```bash
git clone [URL_DO_SEU_REPOSITORIO]
cd [NOME_DO_REPOSITORIO]
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute a aplicação:
```bash
python app.py
```

4. Acesse no navegador:
```
http://localhost:5000
```

## Uso

1. Acesse a aplicação pelo navegador
2. Arraste e solte um arquivo de áudio/vídeo ou clique para selecionar
3. Aguarde o processamento
4. O texto transcrito será exibido na tela
5. Use o botão "Copiar" para copiar o texto para a área de transferência

## Licença

MIT
