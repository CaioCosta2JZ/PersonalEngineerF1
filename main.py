import pyaudio
import json
import subprocess
from vosk import Model, KaldiRecognizer
import os
import re

# Caminho absoluto para o modelo Vosk (ajuste conforme o local real)
model_path = r"C:\vosk-model-en-us-0.22"

# Verifica se o modelo existe
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Modelo Vosk não encontrado em: {model_path}")

# Carrega o modelo Vosk
model = Model(model_path)
rec = KaldiRecognizer(model, 16000)

# Inicializa PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=8000)
stream.start_stream()

print("[🎤] Fale um comando...")

# Função para executar comandos com base no texto reconhecido
def executar_comando(texto):
    texto = texto.lower()
    
    # Detecção de comando usando expressões regulares para mais variações de frases
    if re.search(r"weather report|wheater report|weather forecast|weather update", texto):
        subprocess.run([r"C:\Program Files\AutoHotkey\v2\AutoHotkey64.exe", r"scripts_ahk\weatherReport.ahk"])
    elif re.search(r"tyre wear|how's my tyre wear|how is my tyre wear|tyre condition", texto):
        subprocess.run([r"C:\Program Files\AutoHotkey\v2\AutoHotkey64.exe", r"scripts_ahk\tyreWear.ahk"])
    elif re.search(r"fuel information|fuel status|fuel level", texto):
        subprocess.run([r"C:\Program Files\AutoHotkey\v2\AutoHotkey64.exe", r"scripts_ahk\fuelInformation.ahk"])
    elif re.search(r"full race update|race update|race status", texto):
        subprocess.run([r"C:\Program Files\AutoHotkey\v2\AutoHotkey64.exe", r"scripts_ahk\fullRaceUpdate.ahk"])
    else:
        print("[❓] Comando não reconhecido.")

# Loop principal de escuta
while True:
    data = stream.read(4000, exception_on_overflow=False)
    if rec.AcceptWaveform(data):
        result = json.loads(rec.Result())
        texto = result.get("text", "").strip()
        if texto:
            print(f"[🗣️] Você disse: {texto}")
            executar_comando(texto)
