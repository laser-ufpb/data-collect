import socket

import matplotlib.pyplot as plt
import numpy as np
from numpy.lib.function_base import append
from scipy.signal import find_peaks

import wave
import sys

wave_name="hallo.wav"
######
#That data should be started from the PC (Server)
#####

def sac_dm(data, N):
	M = len(data)
	
	size = int(M/N)
	sacdm=[0.0] * size

	start = 0
	end = N
	for k in range(size):
		peaks, _ = find_peaks(data[start:end])
		v = np.array(peaks)
		sacdm[k] = (1.0*len(v)/N)
		start = end
		end += N

	return sacdm

TCP_IP = '192.168.0.65'
TCP_PORT = 5001
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
 
conn, addr = s.accept()
print ('Connection address:', addr)

from scipy.io.wavfile import write
a = np.array


import socket,os
import threading, wave, pickle,struct

payload_size = struct.calcsize("Q")
CHUNK = 1024
stream = open(wave_name)

while True:
    # Wait for a connection
    print (sys.stderr, 'waiting for a connection')
    connection, client_address = s.accept()
    
    try:
        print (sys.stderr, 'connection from', client_address)
        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            print(data)
        
        print (sys.stderr, 'received "%s"' % data)
        if data:
            print (sys.stderr, 'sending data back to the client')
            connection.sendall(data)
        else:
            print (sys.stderr, 'no more data from', client_address)
        break
            
    finally:
        # Clean up the connection
        connection.close()
wavefile = wave.open("test123.wav")
wavefile.writeframesraw(b''.join(a))
conn.close()
print("ende")
# import socket
# import sys

# # Create a TCP/IP socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # Bind the socket to the port
# server_address = ('192.168.0.65', 5001)
# print (sys.stderr, 'starting up on %s port %s' % server_address)
# sock.bind(server_address)

# # Listen for incoming connections
# sock.listen(1)

# while True:
#     # Wait for a connection
#     print (sys.stderr, 'waiting for a connection')
#     connection, client_address = sock.accept()
    
#     try:
#         print (sys.stderr, 'connection from', client_address)

#         # Receive the data in small chunks and retransmit it
#         while True:
#             data = connection.recv(16)
#         print (sys.stderr, 'received "%s"' % data)
#         if data:
#             print (sys.stderr, 'sending data back to the client')
#             connection.sendall(data)
#         else:
#             print (sys.stderr, 'no more data from', client_address)
#         break
            
#     finally:
#         # Clean up the connection
#         connection.close()

##############
spf = wave.open(wave_name, "r")

# Extract Raw Audio from Wav File
signal = spf.readframes(-1)

signal = np.frombuffer(signal, np.int16)
fs = spf.getframerate()

# If Stereo
if spf.getnchannels() == 2:
    print("Just mono files")
    sys.exit(0)


Time = np.linspace(0, len(signal) / fs, num=len(signal))

N=500
sac = sac_dm(signal, N)


fig = plt.figure()

ax1 = fig.add_subplot(211)  
ax1.plot(Time, signal, color='r', label='audio_orginal')

ax2 = fig.add_subplot(212)
ax2.plot(sac, color='g', label='sac from audio')


fig.savefig("test_sac_audio.png")
plt.show()
print("Cabou!")    
