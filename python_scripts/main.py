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
chunk_duration = 5  # Czas trwania chunków w sekundach
total_duration = 120  # Całkowity czas działania programu w sekundach
broker_address = "a9aa313a.ala.eu-central-1.emqxsl.com"  # Adres brokera MQTT (zmień na odpowiedni adres)
topic = "whisper"  # Temat MQTT
username = "testowy"  # Użytkownik do logowania
password = "test"  # Hasło użytkownika
ca_certs = "./EMQXcert.crt"  # Ścieżka do certyfikatu SSL
start_time = time.time()  # Start odliczania czasu

chunk_number = 1

def remove_polish_characters(text):
    # Sprawdzenie, czy tekst zawiera tylko łacińskie znaki (podstawowy zakres Unicode)
    if not all(' ' <= c <= 'z' or 'A' <= c <= 'Z' for c in text):
        return "sprobuj ponownie"

    # Zamiana polskich znaków na ich łacińskie odpowiedniki
    replacements = {
        'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n',
        'ó': 'o', 'ś': 's', 'ż': 'z', 'ź': 'z',
        'Ą': 'A', 'Ć': 'C', 'Ę': 'E', 'Ł': 'L', 'Ń': 'N',
        'Ó': 'O', 'Ś': 'S', 'Ż': 'Z', 'Ź': 'Z'
    }
    return ''.join(replacements.get(c, c) for c in text)

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
    segments, info = model.transcribe(filename, word_timestamps=True)

    # Wyświetlanie wykrytego języka i pewności
    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

    # Wysyłanie segmentów transkrypcji jako wiadomości MQTT
    for segment in segments:
        for word in segment.words:
            #message = "[%.2fs -> %.2fs] %s" % (word.start, word.end, word.word)
            message = word.word
            print("#################################################")
            print(message)
                # usuwanie polskich znakow
            message = remove_polish_characters(message)
                # Wysyłanie wiadomości MQTT z SSL i uwierzytelnianiem
            send_mqtt_message(broker_address, topic, message, username, password, ca_certs)

    chunk_number += 1

print("Program zakończył nagrywanie i transkrypcję.")
