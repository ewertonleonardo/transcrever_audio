import os
from flask import Flask, render_template, request, jsonify
from faster_whisper import WhisperModel
import librosa
import soundfile as sf
from moviepy.editor import VideoFileClip
import tempfile

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

# Carrega o modelo Whisper
modelo_whisper = WhisperModel("base", device="cpu", compute_type="int8")

ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac', 'opus', 'mp4', 'avi', 'mov', 'mkv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def converter_para_wav(file_path):
    wav_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_audio.wav')
    
    try:
        if file_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            # Para vídeos, usa moviepy
            video = VideoFileClip(file_path)
            video.audio.write_audiofile(wav_path, codec='pcm_s16le')
        else:
            # Para áudios, usa librosa
            audio_data, sample_rate = librosa.load(file_path, sr=16000)
            sf.write(wav_path, audio_data, sample_rate)
    except Exception as e:
        raise Exception(f"Erro na conversão: {str(e)}")
    
    return wav_path

def transcrever_audio(audio_path):
    try:
        segments, info = modelo_whisper.transcribe(audio_path, language='pt')
        texto_completo = ""
        for segment in segments:
            texto_completo += segment.text + " "
        return texto_completo.strip()
    except Exception as e:
        return f"Erro na transcrição: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
    
    if file and allowed_file(file.filename):
        # Salva o arquivo temporariamente
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(temp_path)
        
        try:
            # Converte para WAV se necessário
            wav_path = converter_para_wav(temp_path)
            
            # Realiza a transcrição
            transcricao = transcrever_audio(wav_path)
            
            # Limpa os arquivos temporários
            os.remove(temp_path)
            if os.path.exists(wav_path):
                os.remove(wav_path)
            
            return jsonify({'transcricao': transcricao})
        except Exception as e:
            return jsonify({'error': f'Erro no processamento: {str(e)}'}), 500
    
    return jsonify({'error': 'Tipo de arquivo não permitido'}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
