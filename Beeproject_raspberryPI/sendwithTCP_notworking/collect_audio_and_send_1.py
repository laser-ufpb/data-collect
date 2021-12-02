import socket
import pyaudio
import wave

form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 44100 # 44.1kHz sampling rate
chunk = 4096 # 2^12 samples for buffer
record_secs = 5 # seconds to record
dev_index = 1 # device index found by p.get_device_info_by_index(ii)
wav_output_filename = 'audiofiles/testaudio_tosend.wav' # name of .wav file

audio = pyaudio.PyAudio() # create pyaudio instantiation

#create pyaudio stream
stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                     input_device_index = dev_index,input = True, \
                     frames_per_buffer=chunk)
					
print("recording")
frames = []

# loop through stream and append audio chunks to frame array
for ii in range(0,int((samp_rate/chunk)*record_secs)):
    data = stream.read(chunk, exception_on_overflow = False)
    frames.append(data)

print("finished recording")

# stop the stream, close it, and terminate the pyaudio instantiation
stream.stop_stream()
stream.close()
stream.close()
audio.terminate()

# save the audio frames as .wav file
wavefile = wave.open(wav_output_filename,'wb')
wavefile.setnchannels(chans)
wavefile.setsampwidth(audio.get_sample_size(form_1))
wavefile.setframerate(samp_rate)
wavefile.writeframes(b''.join(frames))
wavefile.close()
print("wavefile created")


import pickle,struct
TCP_IP = '192.168.0.65'
TCP_PORT = 5001
BUFFER_SIZE = 1024

###Tried to send frame step by step or straight the wave datei##
##not woriking
server_socket = socket.socket()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
#s.sendfile(wav_output_filename)

#client_socket,addr = server_socket.accept()
wf = wave.open(wav_output_filename, 'rb')
CHUNK = 1024
data = wf.readframes(CHUNK)
a = pickle.dumps(data)
message = struct.pack("Q",len(a))+a
s.sendall(message)

#s.send(MESSAGE)


#data = s.recv(BUFFER_SIZE)
s.close()
#print("received data:", data)
print("end")


