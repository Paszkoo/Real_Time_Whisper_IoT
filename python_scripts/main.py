from faster_whisper import WhisperModel
from recorder import record_audio, normalize_audio, save_audio_to_file, process_audio
import numpy as np
import time

# Inicjalizacja modelu Whisper
print("Ładowanie modelu Whisper...")
model_size = "large-v3"
model = WhisperModel(model_size, device="cpu", compute_type="int8")
print("Model załadowany.")

# Parametry nagrania
chunk_duration = 10  # Czas trwania chunków w sekundach
total_duration = 120  # Całkowity czas działania programu w sekundach
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
    #print(f"Chunk {chunk_number} zapisany do pliku {filename}.")

    # Transkrypcja nagranego chunku
    #print(f"Rozpoczynam transkrypcję chunka {chunk_number}...")
    segments, info = model.transcribe(filename, beam_size=1)

    # Wyświetlanie wykrytego języka i pewności
    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

    # Wyświetlanie segmentów transkrypcji
    for segment in segments:
        print("#################################################")
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))


    #print(f"Transkrypcja chunka {chunk_number} zakończona.\n")
    
    chunk_number += 1

print("Program zakończył nagrywanie i transkrypcję.")
