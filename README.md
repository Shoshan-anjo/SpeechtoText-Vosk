# 🗣️ Speech-to-Text con Vosk (Español)

Este proyecto permite transcribir audio a texto utilizando el modelo offline de Vosk. Incluye scripts para convertir archivos de audio en texto, ya sea desde archivos pregrabados o directamente desde el micrófono.

## 📁 Estructura del proyecto

- `convaudiotxt.py`: Transcribe audios `.wav` desde una carpeta, convierte si es necesario y guarda el resultado en un archivo `.txt`.
- `audiotxt.py`: Transcribe un único archivo `.wav` (ya en formato correcto) y guarda la transcripción.
- `audiorealtime.py`: Transcribe un archivo de audio en tiempo real mientras lo procesa.
- `microfono.py`: Transcribe en vivo desde el micrófono usando el modelo de Vosk.

## 🧩 Requisitos

- Python 3.7+
- Dependencias:
  ```bash
  pip install vosk sounddevice
  ```
- FFmpeg instalado y agregado al PATH (para conversión de audio en `convaudiotxt.py`).
- Modelo de Vosk en español descargado y descomprimido (ej: `vosk-model-es-0.42`).

## ⚙️ Scripts

### `convaudiotxt.py` – Transcripción interactiva desde carpeta
Este script permite:
- Seleccionar un archivo `.wav` desde una carpeta.
- Convertir el audio a WAV 16kHz mono si es necesario.
- Transcribir el audio usando Vosk.
- Guardar la transcripción en un archivo `.txt`.

💡 Ideal para lotes de audios grabados con distintos formatos.

---

### `audiotxt.py` – Transcripción rápida desde archivo específico
Este script:
- Abre directamente un archivo `.wav` específico.
- Verifica que esté en formato mono 16kHz.
- Transcribe y guarda el resultado en un archivo `.txt`.

🧪 Útil para pruebas simples con un solo audio.

---

### `audiorealtime.py` – Transcripción progresiva desde archivo
Este script:
- Abre un archivo `.wav` en formato compatible.
- Muestra progresivamente cada segmento reconocido.
- Imprime el texto parcial y final por consola.

📡 Útil para visualizar el reconocimiento mientras se procesa.

---

### `microfono.py` – Transcripción en vivo desde micrófono
Este script:
- Usa la librería `sounddevice` para capturar el audio del micrófono en tiempo real.
- Muestra en consola el texto reconocido al hablar.
- Finaliza con `Ctrl+C`.

🎙️ Perfecto para prototipos de asistentes de voz u otros proyectos en vivo.

---
## 🌀 multivosk.py – Transcripción de múltiples audios en lote

Este script permite seleccionar una carpeta con múltiples archivos `.wav`, convertirlos si es necesario, y transcribir cada uno usando el modelo de Vosk. Guarda un archivo `.txt` por cada audio con su respectiva transcripción.

---

### 🧠 ¿Qué hace?

- Recorre automáticamente todos los archivos `.wav` en una carpeta.
- Convierte los audios al formato compatible (WAV 16kHz mono) usando FFmpeg si es necesario.
- Transcribe el contenido de cada archivo.
- Guarda cada transcripción como un archivo `.txt` con el mismo nombre base del audio.

---

### 🚀 Cómo usarlo

1. Ejecuta el script.
2. Ingresa la ruta de la carpeta que contiene los audios `.wav`.
3. El script procesará todos los archivos y generará transcripciones automáticamente.
---

### 📁 Ejemplo de entrada

```
📁 Carpeta: C:\audios_prueba\
├── cliente1.wav
├── cliente2.wav
└── grabacion_voz.wav
```
---

### 📄 Resultado esperado

```
📄 cliente1_transcripcion.txt
📄 cliente2_transcripcion.txt
📄 grabacion_voz_transcripcion.txt
```
---

## 📌 Notas

- Todos los scripts usan el mismo modelo de Vosk. Asegúrate de actualizar la ruta en `MODEL_PATH` según tu ubicación local.
- Si los audios no están en formato `WAV PCM mono 16kHz`, `convaudiotxt.py` se encargará de convertirlos automáticamente usando FFmpeg.

---

## 📄 Créditos

- Motor de reconocimiento: [Vosk API](https://alphacephei.com/vosk/)
- Autor del proyecto: <a href="https://github.com/Shoshan-anjo" target="_blank" style="text-decoration: none;"><strong>Shoshan-anjo</strong>
  </div>
</a>


