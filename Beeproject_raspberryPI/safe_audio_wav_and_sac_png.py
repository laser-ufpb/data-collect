import pyaudio
import wave

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks


def sac_dm(data, N, menorTam):
	M = menorTam
	
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

def plot_x (sec_value): 
	x1 = np.array(range(0, len(sec_value)))
	x1 = x1 * N
	return x1

form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 44100 # 44.1kHz sampling rate
chunk = 4096 # 2^12 samples for buffer
record_secs = int(input('Enter recording time (sec.) '))
#record_secs = 5 # seconds to record
dev_index = 1 # device index found by p.get_device_info_by_index(ii)
wav_output_filename = 'audiofiles/test_sac_audio.wav' # name of .wav file
fig_filename = 'plotfiles/plot_figure.png' 

audio = pyaudio.PyAudio() # create pyaudio instantiation

N = 500 #N-Value for Sac-dm

# create pyaudio stream
stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                     input_device_index = dev_index,input = True, \
                     frames_per_buffer=chunk)

print("recording now for", record_secs, "seconds")
frames = []

# loop through stream and append audio chunks to frame array
for ii in range(0,int((samp_rate/chunk)*record_secs)):
    data = stream.read(chunk, exception_on_overflow = False)
    frames.append(data)
    
print("finished recording")

# stop the stream, close it, and terminate the pyaudio instantiation
stream.stop_stream()
stream.close()
audio.terminate()

# save the audio frames as .wav file
wavefile = wave.open(wav_output_filename,'wb')
wavefile.setnchannels(chans)
wavefile.setsampwidth(audio.get_sample_size(form_1))
wavefile.setframerate(samp_rate)
wavefile.writeframes(b''.join(frames))
wavefile.close()
print(wav_output_filename, "is created")

raw = wave.open(wav_output_filename)

# reads all the frames
# # -1 indicates all or max frames
signal = raw.readframes(-1)
signal = np.frombuffer(signal, dtype ="int16")

# gets the frame rate
f_rate = raw.getframerate()

# to Plot the x-axis in seconds
# you need get the frame rate
# # and divide by size of your signal
# to create a Time Vector
# spaced linearly with the size
# of the audio file
time = np.linspace(0, len(signal) / f_rate, num = len(signal))

# unsing sac_dm
sac = sac_dm(signal, N, len(signal))

# using matlplotlib to plot
# creates a new figure
fig = plt.figure()
fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.4, hspace=1.0)

# unsing subplots
ax1 = fig.add_subplot(211)  
plt.title("Plot from Wavefile")
ax1.plot(time, signal, color='r', label='audio_orginal')
# label of x-axis
plt.xlabel("Time")

ax2 = fig.add_subplot(212)
plt.title("Plot SAC-DM from Wavefile")
ax2.plot( sac, color='g', label='sac from audio')

# shows the plot
#plt.show()

plt.savefig(fig_filename)
print(fig_filename, "is created")
print("end")
