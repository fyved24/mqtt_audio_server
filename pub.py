import time

import paho.mqtt.client as mqtt
import wave
from pydub import AudioSegment

# MQTT broker配置
BROKER = "127.0.0.1"
PORT = 1883
AUDIO_RECEIVE_MQTT_TOPIC = "data/audio"


def publish_frame(frame):
    client = mqtt.Client()
    client.connect(BROKER, PORT)
    client.publish(AUDIO_RECEIVE_MQTT_TOPIC, frame)
    client.disconnect()


def read_audio_file(filename):
    with wave.open(filename, 'rb') as audio_file:
        sample_rate = audio_file.getframerate()
        channels = audio_file.getnchannels()
        sample_width = audio_file.getsampwidth()
        frame_size = sample_width * channels
        print(f"sample_rate: {sample_rate}, channels: {channels}, sample_width: {sample_width}, frame_size: {frame_size}")

        frame_count = audio_file.getnframes()
        print(f"frame_count: {frame_count}")
        for i in range(0, frame_count, sample_rate):
            frames = audio_file.readframes(sample_rate)
            publish_frame(frames)
            time.sleep(1)


if __name__ == '__main__':
    # 读取音频文件并发布每一帧
    audio_filename = "cantonese.wav"
    read_audio_file(audio_filename)
