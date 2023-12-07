# Video_transcription

A Video Transcription Project to transcribe text from the given video on the browser using whisper AI model.

## Setup

Clone the project

```bash
  git clone https://github.com/mukunthan007/video_transcription.git
```

Go to the project directory

```bash
  cd video_transcription
```

Choose one of the following options to set up the project locally or using Docker.

### 1. Docker

Install Docker - https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04

Build & Run the container
```bash
  docker build -t dockerfile .
  docker run -d -p 8080:5000 dockerfile:latest
```

vist - [http://127.0.0.1:8080/](http://127.0.0.1:8080/ )

### 2. Run Locally

Install dependencies

```bash
  # on Ubuntu or Debian
  sudo apt update && sudo apt install ffmpeg

  # install python
  sudo apt-get install python3.8

  # install pip for python
  sudo apt-get install python3-pip python-dev

  # create virtual envionment for python
  python3 -m venv .venv

  # activate env
  source .venv/bin/activate

  # install dependencies
  pip install -r requirements.txt
```

Start the server

```bash
  python3 wsgi.py
```

*Note: Currently, the model is configured to run on the CPU, even if a GPU is available.*

## Demo

https://github.com/mukunthan007/video_transcription/assets/50894477/d64948cd-5e18-44be-966a-fe389a509352

## Performance Comparison

Ran an inference on a 1:20 minute video for both CPU and GPU.

|Video	                                         | CPU        |	GPU        |
|----------------------------------------------- |:----------:|:----------:|
|https://youtu.be/yYF2Vf1Gc14?si=5dcdV0YGYygOhXi5|49.80139961s|27.72750911s|

*Note: The times represent the duration of inference, and lower values indicate better performance. GPU time is significantly faster compared to CPU time, showcasing the benefits of GPU acceleration.*

## Future Enhancements

### 1. PyTorch to TensorFlow Lite Conversion

- **Objective:** Convert the PyTorch model to a TensorFlow Lite model for improved memory efficiency and faster inference times.
- **Advantages:**
  - **Memory Usage:** Significant reduction in memory consumption.
  - **Inference Time:** Faster predictions.
- **Considerations:**
  - **Timestamps:** Loss of timestamp information for each word in the extracted text (currently supported only in PyTorch).

### 2. Model Quantization

- **Objective:** Implement quantization for a medium-sized model to optimize memory usage and enhance Word Error Rate (WER).
- **Advantages:**
  - **Memory Efficiency:** Reduced RAM usage.
  - **WER Improvement:** Enhanced recognition accuracy.
- **Considerations:**
  - **Resource Usage:** Requires approximately 6 GB of RAM.
  - **Inference Time:** Potential increase.

### 3. Server-Sent Events for Inference Status

- **Objective:** Replace long polling with server-sent events for checking the status of inference, enhancing client and server performance.
- **Advantages:**
  - **Performance:** Improved responsiveness between client and server.

### 4. Multi-Language Subtitles Support

- **Objective:** Add support for multi-language subtitles in upcoming releases.
- **Advantages:**
  - **Versatility:** Enables users to process audio in different languages.
- **Timeline:** Expected to be supported in the near future.

## How to Contribute

If you're interested in contributing to these enhancements or have additional ideas, follow these guidelines:

- Fork the repository and create a new branch for your feature.
- Adhere to the project's coding standards.
- Submit a pull request with a clear description of your changes.
