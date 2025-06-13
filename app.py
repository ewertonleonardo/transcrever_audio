import os
from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
from pydub import AudioSegment
from moviepy import VideoFileClip
import tempfile

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac', 'opus', 'mp4', 'avi', 'mov', 'mkv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def converter_para_wav(file_path):
    wav_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_audio.wav')
    if file_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
        try:
            with VideoFileClip(file_path) as video:
                if video.audio:
                    video.audio.write_audiofile(wav_path, codec='pcm_s16le')
                else:
                    raise ValueError("Video file does not contain an audio track.")
        except Exception as e:
            # Propagate error to be handled by the caller
            raise e
    else:
        audio = AudioSegment.from_file(file_path)
        audio.export(wav_path, format="wav")
    return wav_path

def transcrever_audio(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
    try:
        texto = recognizer.recognize_google(audio_data, language='pt-BR')
        return texto.strip()
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
