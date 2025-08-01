import wave
import json
from vosk import Model, KaldiRecognizer

# Ruta al modelo Vosk (ya descomprimido)
MODEL_PATH = r"C:\Users\aj.montalvo\Desktop\Nueva carpeta\Python - Vosk\vosk-model-es-0.42"

# Ruta del archivo de audio (asegurate de que sea WAV mono 16KHz)
AUDIO_PATH = r"C:\Users\aj.montalvo\Desktop\Nueva carpeta\Python - Vosk\audio_convertido.wav"

# Cargar modelo
model = Model(MODEL_PATH)

# Abrir archivo de audio
wf = wave.open(AUDIO_PATH, "rb")

# Validar formato
if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
    raise ValueError("El archivo debe estar en formato WAV PCM 16kHz mono")

# Crear reconocedor
rec = KaldiRecognizer(model, wf.getframerate())

print("🕵️ Transcribiendo...")

# Leer y procesar audio
while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        result = json.loads(rec.Result())
        print("🗣️ Texto:", result.get("text", ""))

# Último fragmento
final_result = json.loads(rec.FinalResult())
print("📝 Resultado final:", final_result.get("text", ""))
