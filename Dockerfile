# Bazowy obraz CUDA z Ubuntu 22.04
FROM nvidia/cuda:12.6.2-cudnn-runtime-ubuntu22.04

# Ustawienie zmiennej, aby zapobiec interaktywnym pytaniom
ENV DEBIAN_FRONTEND=noninteractive

# Instalacja podstawowych pakietów
RUN apt-get update && apt-get install -y --no-install-recommends \
    software-properties-common \
    portaudio19-dev \
    python3.11 \
    python3.11-venv \
    python3.11-dev \
    curl \
    libasound2-dev \
    libpulse-dev \
    ffmpeg \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Instalacja pip dla Pythona 3.11
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11

# Ustawienie Pythona 3.11 jako domyślnego
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 \
    && update-alternatives --install /usr/bin/pip3 pip3 /usr/local/bin/pip3.11 1

# Skopiowanie projektu
WORKDIR /app
COPY ./python_scripts /app/python_scripts

# Instalacja zależności z requirements.txt
RUN pip3 install --upgrade pip && pip3 install -r /app/python_scripts/requirements.txt

# Domyślne polecenie uruchamiające aplikację
CMD ["python3", "/app/python_scripts/main.py"]
