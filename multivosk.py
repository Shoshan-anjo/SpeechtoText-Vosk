import os
import wave
import json
import subprocess
import time
from vosk import Model, KaldiRecognizer

MODEL_PATH = r"C:\Users\aj.montalvo\Desktop\Nueva carpeta\Python - Vosk\vosk-model-es-0.42"
CARPETA_AUDIOS = input("📁 Ingresá la ruta de la carpeta con los audios .wav:\n> ").strip('" ')

def convertir_audio_si_necesario(entrada, salida):
    try:
        with wave.open(entrada, 'rb') as wf:
            if wf.getnchannels() == 1 and wf.getsampwidth() == 2 and wf.getframerate() == 16000:
                return entrada
    except:
        pass

    comando = ["ffmpeg", "-y", "-i", entrada, "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", salida]
    resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if resultado.returncode != 0:
        raise RuntimeError(f"❌ Error al convertir {entrada}:\n{resultado.stderr}")
    return salida

def transcribir_archivo(audio_path, model):
    base = os.path.splitext(audio_path)[0]
    convertido = base + "_convertido.wav"
    salida_txt = base + "_transcripcion.txt"

    audio_ok = convertir_audio_si_necesario(audio_path, convertido)
    wf = wave.open(audio_ok, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    texto = ""

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            texto += result.get("text", "") + " "
    texto += json.loads(rec.FinalResult()).get("text", "")

    with open(salida_txt, "w", encoding="utf-8") as f:
        f.write(texto.strip())
    print(f"✅ {os.path.basename(audio_path)} transcrito a: {salida_txt}")

def procesar_todos_los_audios():
    if not os.path.isdir(CARPETA_AUDIOS):
        print("❌ Carpeta inválida.")
        return

    audios = [f for f in os.listdir(CARPETA_AUDIOS) if f.lower().endswith(".wav")]
    if not audios:
        print("❌ No se encontraron archivos .wav.")
        return

    print(f"🎧 {len(audios)} audios encontrados. Iniciando transcripción...")

    model = Model(MODEL_PATH)
    inicio = time.time()

    for archivo in audios:
        path = os.path.join(CARPETA_AUDIOS, archivo)
        try:
            transcribir_archivo(path, model)
        except Exception as e:
            print(f"⚠️ Error con {archivo}: {e}")

    fin = time.time()
    print(f"\n🏁 Transcripción finalizada en {fin - inicio:.2f} segundos.")

# Ejecutar
procesar_todos_los_audios()
