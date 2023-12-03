FROM python:3.8.10-slim

WORKDIR /

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

RUN apt-get install -y ffmpeg 
COPY /requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY / .

EXPOSE 5000

CMD [ "python3" , "wsgi.py" ]