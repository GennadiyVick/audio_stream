#!/usr/bin/python3
"""
Audio stream sender using lib pyaudio.
Works on Linux OS, if there is no sound, look at your settings alsa, pulse, etc.,
for example for pulse I used the pavucontrol utility to direct the output.
For Windows, it is possible to correct the code.
Author Roganov G.V. roganovg@mail.ru

LICENSE
This is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.
This soft is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU Lesser General Public License for more details.
"""
import pyaudio
import socket


port = 5000
ip = input('type server IP-address (default is 192.168.1.101): ')
if len(ip) == 0:
    ip = "192.168.1.101"
chunk = 512
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
 
p = pyaudio.PyAudio()
SPEAKERS = p.get_default_output_device_info()["hostApi"]

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=chunk,
                input_host_api_specific_stream_info=SPEAKERS)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(f'try connect to {ip} {port}')
client_socket.connect((ip, port))
print('connected')


while True:
    try:
        ch = stream.read(chunk)
        client_socket.sendall(ch)
    except KeyboardInterrupt:
        print(' Exit with CTRL+C')
        break
    except Exception as e:
        print(e)
        break
stream.close()
client_socket.close()    
