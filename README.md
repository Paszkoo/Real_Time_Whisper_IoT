# Real Time Whisper by Paszko V1.0, 
### Description
It uses Open AI Whisper model and by recording 2 second chunks from default audio input device, prints recognized speech. Works with both CPU and CUDA and has special function for choosing it so it wont crash. Require linux to dockerize it.

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

### instructions
1. cd Real_Time_whisper_IoT
2. sudo docker build -t Real_Time_whisper_IoT .

### Run
docker run --gpus all --device /dev/snd:/dev/snd --rm -it whisper-audio-app


### mic not working
Check python_scripts/recorder.py, run it without docker, and check witch device is actually recording