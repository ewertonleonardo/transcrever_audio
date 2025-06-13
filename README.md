# Transcrever Áudio

Aplicativo para transcrição de áudio e vídeo em português usando Whisper.

## 📦 Dependências

- Python 3.13+
- Bibliotecas:
  - `faster-whisper`: Transcrição de áudio
  - `librosa` + `soundfile`: Processamento de áudio
  - `moviepy`: Processamento de vídeo
  - `flask`: Interface web
  - `colorama`: Cores no terminal

## 🚀 Como Usar

1. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

2. Para usar a interface web:

   ```bash
   python app.py
   ```

   Acesse: <http://localhost:5000>

3. Para usar o script de linha de comando:

   ```bash
   python transcribe.py
   ```

   Os arquivos devem estar na pasta `source`.

## ✅ Formatos Suportados

- Áudio: WAV, MP3, FLAC, OPUS
- Vídeo: MP4, AVI, MOV, MKV

## 🔧 Arquivos de Configuração

- `gunicorn.conf.py`: Configuração do servidor web

## 📝 Notas

- Otimizado para Python 3.13
- Não requer FFmpeg instalado
- Modelo Whisper base (145MB) carregado automaticamente

## Licença

Todos os direitos reservados

## Render.com

Build Command: pip install -r requirements.txt
Start command: gunicorn app:app
