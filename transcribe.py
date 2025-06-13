import os
import datetime
import speech_recognition as sr
from pydub import AudioSegment
from moviepy import VideoFileClip
from colorama import just_fix_windows_console, Fore, Style

# Ativa o suporte a ANSI no Windows
just_fix_windows_console()

# Caminho da pasta "source" onde estão os vídeos e áudios (agora ajustado para `TranscriptLocal/source`)
source_path = os.path.join(os.getcwd(), "source")

# Função para delimitar todo o processo com linhas de "="
def log_divider():
    print(Fore.LIGHTCYAN_EX + "=" * 50 + Style.RESET_ALL)

# Função para exibir mensagens com quebras de linha
def log_message(message, color, newline_before=True, newline_after=True):
    if newline_before:
        print()  # Quebra de linha antes
    print(color + message + Style.RESET_ALL)
    if newline_after:
        print()  # Quebra de linha depois

# Função para transcrever áudio usando Google Speech API
def transcrever_audio(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
    try:
        texto = recognizer.recognize_google(audio_data, language='pt-BR')
        return texto.strip()
    except Exception as e:
        log_message(f"Erro ao transcrever com Google: {e}", Fore.LIGHTRED_EX)
        return None

# Função para converter formatos de áudio e vídeo para WAV
def converter_para_wav(file_path):
    log_message("CONVERSÃO PARA WAV", Fore.LIGHTMAGENTA_EX, newline_before=False)
    log_message(file_path, Fore.LIGHTWHITE_EX, newline_before=False, newline_after=False)
    wav_path = file_path.replace(file_path.split('.')[-1], 'wav')
    if file_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
        try:
            with VideoFileClip(file_path) as video:
                if video.audio:
                    video.audio.write_audiofile(wav_path, codec='pcm_s16le')
                else:
                    log_message(f"Video file {os.path.basename(file_path)} has no audio track. Skipping.", Fore.YELLOW_EX)
                    return None # Indicate failure to create wav_path
        except Exception as e:
            log_message(f"Error processing video {os.path.basename(file_path)} with MoviePy: {e}. Skipping.", Fore.RED_EX)
            return None # Indicate failure
    else:
        audio = AudioSegment.from_file(file_path)
        audio.export(wav_path, format="wav")
    return wav_path

# Função principal para processar todos os arquivos na pasta "source"
def processar_arquivos_na_pasta(base_path):
    log_divider()
    log_message("INICIANDO O PROCESSO DE TRANSCRIÇÃO PARA TODOS OS ARQUIVOS", Fore.LIGHTCYAN_EX, newline_before=False)
    log_divider()
    
    start_time = datetime.datetime.now()
    
    for filename in os.listdir(base_path):
        file_path = os.path.join(base_path, filename)
        nome_base, extensao = os.path.splitext(filename)
        
        # Indicação do início do processo para o arquivo
        log_divider()
        log_message(f"INICIANDO PROCESSO PARA {filename}", Fore.LIGHTGREEN_EX, newline_before=False)
        
        # Verifica se o tipo de arquivo é suportado
        if extensao.lower() in [".wav", ".mp3", ".flac", ".opus", ".mp4", ".avi", ".mov", ".mkv"]:
            # Converte para .wav
            wav_path = converter_para_wav(file_path)
            
            # Realiza a transcrição
            if wav_path: # This existing check will handle the None return
                log_message("PROCESSANDO:", Fore.LIGHTMAGENTA_EX, newline_before=True, newline_after=False)
                log_message(filename, Fore.LIGHTWHITE_EX, newline_before=False)
                texto_transcricao = transcrever_audio(wav_path)

                if texto_transcricao:
                    output_path = os.path.join(base_path, f"{nome_base}.md")
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(f"# Transcrição do arquivo: {filename}\n\n")
                    f.write(texto_transcricao)
                
                # Mensagem de sucesso com o caminho do arquivo salvo
                log_message("TRANSCRIÇÃO SALVA EM:", Fore.LIGHTGREEN_EX, newline_before=True, newline_after=False)
                log_message(output_path, Fore.LIGHTWHITE_EX, newline_before=False)
            
            # Remove o arquivo WAV temporário
            if os.path.exists(wav_path):
                os.remove(wav_path)
        else:
            # Mensagem de formato não suportado
            log_message("FORMATO NÃO SUPORTADO", Fore.LIGHTYELLOW_EX)
            log_message(filename, Fore.LIGHTWHITE_EX, newline_before=False)
        
        # Indicação de fim do processo para o arquivo
        log_message(f"FIM DO PROCESSO PARA {filename}", Fore.LIGHTGREEN_EX)
        log_divider()

    # Tempo total de execução
    end_time = datetime.datetime.now()
    total_time = end_time - start_time
    
    log_divider()
    log_message(f"PROCESSO DE TRANSCRIÇÃO CONCLUÍDO", Fore.LIGHTGREEN_EX, newline_before=False)
    log_message(f"Tempo total de execução: {total_time}", Fore.LIGHTWHITE_EX, newline_before=False)
    log_divider()

# Executa o script
if __name__ == "__main__":
    processar_arquivos_na_pasta(source_path)
