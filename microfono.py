import requests
import vosk
import sounddevice as sd
import queue
import sys
import json
from vosk import Model, KaldiRecognizer


# Ruta a la carpeta del modelo descargado
MODEL_PATH = r"C:\Users\aj.montalvo\Desktop\Nueva carpeta\Python - Vosk\vosk-model-es-0.42"

# Cargar modelo
model = Model(MODEL_PATH)
rec = KaldiRecognizer(model, 16000)

# Configurar cola de audio
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

# Iniciar captura de audio
with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                       channels=1, callback=callback):
    print("🎤 Hablá algo... Ctrl+C para salir")
    try:
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                print("Texto:", result.get("text", ""))
    except KeyboardInterrupt:
        print("\n⏹ Finalizado")