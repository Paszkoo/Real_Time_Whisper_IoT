# Real Time Whisper by Paszko V1.3, 
### Description
It uses Locally Open AI Whisper model and by recording 2 second chunks from default audio input device, prints recognized speech. And RTWI* uses Yolov8 model to predict what he can see from laptop camera. Works with both CPU and CUDA. Required linux to dockerize it. I know there are tokens and ssl certs in code but its just for testing okay..

### Linux required for easier installation, making docker can read microphone from windows is quite complicated

## installation on linux Debian12
### Requirements:
- Python 3.11.8 !! important
- make venv and 
- install requirements.txt
- SSL cert for MQTT connection in /python_scripts/MQTTcert.crt
### CUDA Requirements
- CUDA 12.6, V12.6.77
- nvhpc_2024_2411_Linux_x86_64_cuda_12.6.tar.gz
- cudnn/9.5.1/local_installers/cudnn-local-repo-debian12-9.5.1_1.0-1_amd64.deb
### Run
1. set correct values main.py
2. using >Real_Time_whisper_IoT/python_scripts/.venv/bin/Python3.11 main.py

## DOCKER install
### Requirements
1. docker
2. NVIDIA Container Toolkit for docker so it can read GPU
3. SSL cert for MQTT connection in /python_scripts/MQTTcert.crt

### instructions whisper_RealTime 
1. cd whisper_realTime
2. sudo docker build -t whisper_realTime .

### whisper_RealTime run:
sudo docker run --gpus all --device /dev/snd:/dev/snd --rm -it whisper-audio-app

### instructions YOLOv8 
1. cd YOLOv8
2. sudo docker build -t yolo-app .

### YOLOv8 run:
sudo docker run --rm --device=/dev/video0:/dev/video0 yolo-app

## Grafana 'n influx stats server setup and run
1. cd grafana_influx_stats
2. sudo docker compose up --build

## NodeMCU v3 setup
### I2C LCD wireing
VCC -> VV
GND -> G
SCL -> D1
SDA -> D2

### DallasTemperature sensor wireing
Middle Pin (data) -> D3
GND -> GND
VCC -> 3V with resistor



### mic not working
Check python_scripts/recorder.py, run it without docker, and check witch device is actually recording
