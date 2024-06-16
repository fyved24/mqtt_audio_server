import paho.mqtt.client as mqtt
import time
import pyaudio
import wave
import struct

# 设置音频参数
sample_rate = 16000  # 设置采样率
channels = 1  # 设置通道数
sample_width = 2  # 设置样本宽度（以字节为单位）

p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(sample_width), channels=channels, rate=sample_rate, output=True)
HOST = "127.0.0.1"
PORT = 1883

AUDIO_MQTT_TOPIC = "data/audio"


def client_loop():
    client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,client_id,)  # ClientId不能重复，所以使用当前时间
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(HOST, PORT, 15)
    client.loop_forever()

def on_connect(client, userdata, flags, reason_code, properties):
    if flags.session_present:
        print('session_present')
    if reason_code == 0:
        print("Connected with result code " + str(reason_code))
        client.subscribe(AUDIO_MQTT_TOPIC)
    if reason_code > 0:
        print('连接失败')


def on_message(client, userdata, msg):
    # 将字节流转换为32位整数样本
    data = msg.payload
    print(data)

    # 播放音频
    stream.write(msg.payload)
    rotate_audio_file(msg.payload, 10)


start = 0
is_start = False
audio_file = None
file_name = None

buffer = b''  # 用于缓存音频数据的字节流


def rotate_audio_file(frame, seconds):
    global start
    global is_start
    global audio_file
    global buffer
    global file_name
    if is_start:
        buffer += frame
        if time.time() - start > seconds:
            is_start = False
            audio_file.writeframes(buffer)
            audio_file.close()
            buffer = b''
            print(f"saved {file_name}")
    else:
        start = time.time()
        file_name = f"{time.strftime('%Y.%m.%d.%H.%M.%S')}.wav"
        audio_file = wave.open(file_name, "wb")
        audio_file.setnchannels(channels)
        audio_file.setsampwidth(sample_width)
        audio_file.setframerate(sample_rate)
        is_start = True


if __name__ == '__main__':
    client_loop()
