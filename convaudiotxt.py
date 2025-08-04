import wave
import json
import os
import subprocess
from vosk import Model, KaldiRecognizer
import time

inicio = time.time()
print("🚀 Iniciando Proceso...")

def seleccionar_audio_desde_carpeta():
    carpeta = input("📁 Ingresá la ruta de la carpeta que contiene los audios:\n> ").strip('" ')

    if not os.path.isdir(carpeta):
        print("❌ Esa carpeta no existe.")
        exit(1)

    # Listar archivos .wav
    archivos = [f for f in os.listdir(carpeta) if f.lower().endswith(".wav")]
    if not archivos:
        print("❌ No se encontraron archivos .wav en la carpeta.")
        exit(1)

    print("\n🎧 Audios encontrados:")
    for i, archivo in enumerate(archivos):
        print(f"  [{i + 1}] {archivo}")

    # Elegir uno
    try:
        seleccion = int(input("\n🔊 Ingresá el número del audio que querés transcribir: "))
        if seleccion < 1 or seleccion > len(archivos):
            raise ValueError
    except ValueError:
        print("❌ Selección inválida.")
        exit(1)

    archivo_seleccionado = os.path.join(carpeta, archivos[seleccion - 1])
    print(f"\n✅ Audio seleccionado: {archivo_seleccionado}")
    return archivo_seleccionado


# === FUNCION: Convertir audio con ffmpeg si es necesario ===
def convertir_audio_si_necesario(entrada, salida):
    try:
        with wave.open(entrada, 'rb') as wf:
            if wf.getnchannels() == 1 and wf.getsampwidth() == 2 and wf.getframerate() == 16000:
                print("✅ Audio ya está en formato compatible.")
                return entrada  # No necesita conversión
    except:
        print("⚠️ Formato no compatible o no es WAV estándar. Convirtiendo...")

    print("🔄 Convirtiendo a WAV 16kHz mono con ffmpeg...")
    comando = [
        "ffmpeg",
        "-y",
        "-i", entrada,
        "-ar", "16000",
        "-ac", "1",
        "-c:a", "pcm_s16le",
        salida
    ]
    resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if resultado.returncode != 0:
        print("❌ Error al convertir audio:", resultado.stderr)
        raise RuntimeError("Fallo la conversión con ffmpeg.")

    return salida


# === FUNCION PRINCIPAL ===
def transcribir_audio_a_txt(model_path, audio_original):
    # Generar nombres automáticos
    base_name = os.path.splitext(audio_original)[0]
    audio_convertido = base_name + "_convertido.wav"
    salida_txt = base_name + "_transcripcion.txt"

    # Convertir si es necesario
    audio_ok = convertir_audio_si_necesario(audio_original, audio_convertido)

    # Cargar modelo
    model = Model(model_path)

    # Abrir archivo convertido
    wf = wave.open(audio_ok, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())

    texto_completo = ""

    print("🕵️ Transcribiendo...")

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            texto_completo += result.get("text", "") + " "

    # Agregar último fragmento
    final_result = json.loads(rec.FinalResult())
    texto_completo += final_result.get("text", "")

    # Guardar en archivo
    with open(salida_txt, "w", encoding="utf-8") as f:
        f.write(texto_completo.strip())

    print(f"\n✅ Transcripción guardada en: {salida_txt}")
    os.startfile(salida_txt)  # Esto abrirá el archivo automáticamente (solo en Windows)


# === EJECUCIÓN ===
MODEL_PATH = r"C:\Users\aj.montalvo\Desktop\Nueva carpeta\Python - Vosk\vosk-model-es-0.42"
AUDIO_ORIGINAL = seleccionar_audio_desde_carpeta()
transcribir_audio_a_txt(MODEL_PATH, AUDIO_ORIGINAL)

fin = time.time()
print(f"✅ Proceso completado en {fin - inicio:.2f} segundos.")
