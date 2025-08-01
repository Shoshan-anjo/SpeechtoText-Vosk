import wave
import json
from vosk import Model, KaldiRecognizer

# === CONFIGURACIÓN ===
MODEL_PATH = r"C:\Users\aj.montalvo\Desktop\Nueva carpeta\Python - Vosk\vosk-model-es-0.42"
AUDIO_PATH = r"C:\Users\aj.montalvo\Desktop\Nueva carpeta\Python - Vosk\audio_prueba.wav"
ARCHIVO_TXT = r"C:\Users\aj.montalvo\Desktop\Nueva carpeta\Python - Vosk\transcripcion_final.txt"

# === CARGAR MODELO ===
model = Model(MODEL_PATH)

# === ABRIR AUDIO ===
wf = wave.open(AUDIO_PATH, "rb")

# Validar formato
if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
    raise ValueError("El archivo debe estar en formato WAV PCM 16kHz mono")

rec = KaldiRecognizer(model, wf.getframerate())

# === TRANSCRIBIR ===
texto_completo = ""

print("🕵️ Transcribiendo...")

while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        result = json.loads(rec.Result())
        texto_completo += result.get("text", "") + " "

# Último fragmento
final_result = json.loads(rec.FinalResult())
texto_completo += final_result.get("text", "")

# === GUARDAR EN ARCHIVO TXT ===
with open(ARCHIVO_TXT, "w", encoding="utf-8") as f:
    f.write(texto_completo.strip())

print(f"✅ Transcripción final guardada en: {ARCHIVO_TXT}")
