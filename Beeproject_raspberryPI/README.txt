1. Connect PI with SSH 
- https://www.youtube.com/watch?v=JGXZZoHc1zA 
- micro usb into your PC for config Wifi
- chage Wifi iide and passwort in wpa_supplicate.conf 
- start raspberry with new config 
- i used Advanced IP Scanner to search for the raspberry IP-Adress
- Connect to ssh, default values of name and passwort (name=pi, psw=raspberry)

2. Test script audiotest.py 
- https://makersportal.com/blog/2018/8/23/recording-audio-on-the-raspberry-pi-with-python-and-a-usb-microphone
- importan is the channel, i used the 4. USB slot (right bottom) this is channel1

3. Test safe_audio_wave_and_sac_png.py 
- after start, programm needs a time vaulue for recording in secounds
- enter a value and see results in folder (audiofiles and plotfiles)
- to see, i used filezilla for transfer data from PI to my PC

4. NOT WORKING send wavefile or png from PI to PC with TCP 
- there are some messy files
- i tried to send the frames of recording with a tcp socket to a server to anaylse it there, without succes yet


# Raspberry Pi is not connected with our Github