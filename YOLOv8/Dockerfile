# Wybieramy obraz bazowy z Pythonem i PyTorchem (z CUDA, jeśli masz GPU)
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

# Ustawiamy zmienną środowiskową, aby Python nie buforował wyjścia
ENV PYTHONUNBUFFERED=1

# Ustawienie zmiennej, aby zapobiec interaktywnym pytaniom
ENV DEBIAN_FRONTEND=noninteractive

# Instalujemy zależności systemowe
RUN apt-get update && apt-get install -y \
    python3-opencv \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*


# Tworzymy katalog roboczy
WORKDIR /app
# Kopiujemy kod programu do kontenera
COPY . /app

# Instalujemy YOLOv8 i inne wymagane pakiety
RUN pip install --no-cache-dir -r /app/requirements.txt

# Ustawiamy domyślny punkt wejścia
CMD ["python", "main.py"]
