from faster_whisper import WhisperModel
from recorder import record_audio, normalize_audio, save_audio_to_file, process_audio
from mqtt_client import send_mqtt_message  # Import funkcji MQTT
import numpy as np
import time

# Inicjalizacja modelu Whisper
print("Ładowanie modelu Whisper...")
model_size = "large-v3"
model = WhisperModel(model_size, device="cpu", compute_type="int8")
print("Model załadowany.")

# Parametry nagrania i MQTT
chunk_duration = 10  # Czas trwania chunków w sekundach
total_duration = 120  # Całkowity czas działania programu w sekundach
broker_address = "a9aa313a.ala.eu-central-1.emqxsl.com"  # Adres brokera MQTT (zmień na odpowiedni adres)
topic = "transcription_topic"  # Temat MQTT
username = "testowy"  # Użytkownik do logowania
password = "test"  # Hasło użytkownika
ca_certs = "./emqxsl-ca.crt"  # Ścieżka do certyfikatu SSL
start_time = time.time()  # Start odliczania czasu

chunk_number = 1

while (time.time() - start_time) < total_duration:
    print(f"Rozpoczynam nagrywanie chunka {chunk_number}...")

    # Nagrywanie i przetwarzanie audio
    audio_data = record_audio(chunk_duration)
    audio_data = normalize_audio(audio_data)
    process_audio(audio_data)
    
    # Zapis do pliku tymczasowego
    filename = f"chunk_{chunk_number}.wav"
    save_audio_to_file(audio_data, filename)

    # Transkrypcja nagranego chunku
    segments, info = model.transcribe(filename, beam_size=1)

    # Wyświetlanie wykrytego języka i pewności
    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

    # Wysyłanie segmentów transkrypcji jako wiadomości MQTT
    for segment in segments:
        message = "[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text)
        print("#################################################")
        print(message)
        
        # Wysyłanie wiadomości MQTT z SSL i uwierzytelnianiem
        send_mqtt_message(broker_address, topic, message, username, password, ca_certs)

    chunk_number += 1

print("Program zakończył nagrywanie i transkrypcję.")
