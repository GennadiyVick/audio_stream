#!/usr/bin/python3
"""
audio stream receiver using lib pyaudio
only for one socket client
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


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 53))
    ip = s.getsockname()[0]
    s.close()
    return ip


port = 5000
 
chunk = 512
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=True, frames_per_buffer=chunk)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create the socket
server_socket.bind(('', port)) # listen on port 5000
server_socket.listen(5) # queue max 5 connections
running = True

print('server started ', get_local_ip(), port)

while running:
    print('listening...')
    try:
        client_socket, address = server_socket.accept()
    except KeyboardInterrupt:
        print(' Exit with CTRL+C')
        break

    data_size = 0    
    print('client connected', address)
    print('')
    while running:
        try:
            data = client_socket.recv(2048)
            l = len(data)
            if l > 100:
                #data_size += l
                stream.write(data, chunk)
                #print("sending bytes: %s" % (data_size), end="\r")
            else:
                print('client disconnected')
                break
        except KeyboardInterrupt:
            running = False
            print(' Exit with CTRL+C')
            break
        except:
            print('client disconnected')
            break
       
server_socket.close()
stream.close()
