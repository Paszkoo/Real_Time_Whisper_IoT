import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write

# Ustawienia domyślne
SAMPLE_RATE = 44100  # Próbkowanie 44.1 kHz
CHANNELS = 1         # Kanał mono

def record_audio(duration: int):
    """
    Nagrywa audio przez określoną liczbę sekund i zwraca nagranie.
    
    :param duration: Czas nagrania w sekundach
    :return: Zwraca nagranie audio jako tablicę numpy
    """
    print(f"Nagrywanie przez {duration} sekund...")
    recording = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=CHANNELS, dtype='float32')
    sd.wait()  # Czekaj na zakończenie nagrania
    print("Nagrywanie zakończone.")
    return recording

def normalize_audio(audio_data: np.ndarray, target_amplitude=0.8):
    """
    Normalizuje nagranie audio do określonego poziomu amplitudy.
    
    :param audio_data: Tablica numpy z danymi audio
    :param target_amplitude: Docelowa maksymalna wartość amplitudy (domyślnie 0.9)
    :return: Zwraca znormalizowane dane audio
    """
    max_amplitude = np.max(np.abs(audio_data))
    normalized_audio = (audio_data / max_amplitude) * target_amplitude
    print(f"Audio znormalizowane do poziomu {target_amplitude}")
    return normalized_audio

def save_audio_to_file(audio_data: np.ndarray, filename: str):
    """
    Zapisuje nagranie audio do pliku .wav.
    
    :param audio_data: Tablica numpy z danymi audio
    :param filename: Nazwa pliku do zapisu
    """
    scaled_audio = np.int16(audio_data * 32767)
    write(filename, SAMPLE_RATE, scaled_audio)
    print(f"Nagranie zapisane do pliku {filename}")

def process_audio(audio_data: np.ndarray):
    """
    Przykładowa funkcja przetwarzająca nagranie audio.
    
    :param audio_data: Tablica numpy z danymi audio
    """
    print(f"Długość nagrania: {len(audio_data) / SAMPLE_RATE:.2f} s")
    print(f"Maksymalna amplituda: {np.max(np.abs(audio_data)):.2f}")

# Przykład użycia
if __name__ == "__main__":
    czas_nagrania = 5  # czas nagrania w sekundach
    filename = "nagranie.wav"
    
    audio_data = record_audio(czas_nagrania)
    audio_data = normalize_audio(audio_data)  # Normalizacja nagrania
    process_audio(audio_data)
    save_audio_to_file(audio_data, filename)
