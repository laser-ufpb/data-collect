#!/usr/bin/env python

# Importa pacotes para criação do servidor e manipulação dos dados
import socket
import time
import pandas as pd

# Importa pacotes responsáveis por cuidar da interrupção quando o programa for fechado com 'Ctrl + C'
import signal
import sys
import threading

# Nome do arquivo que armazenará a coleta do SAC-DM
nomeArquivo = 'm5Stick_TR_drone_grande_02_12_2021_com_vento_1'

localIP     = "192.168.1.101"

localPort   = 20001

bufferSize  = 1024

# Create a datagram socket



UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)


# Bind to address and ip

UDPServerSocket.bind((localIP, localPort))


x=[]
y=[]
z=[]
timestamp = []

print("UDP server up and listening")
# Cria thread que monitora o fechamento do programa com 'Ctrl + C'
# Quando programa for fechado, executa essa função:
def signal_handler(signal, frame):
    print('\n\nSalvando coleta de dados em {}.csv'.format(nomeArquivo))
    """ for j in range(len(timestamp)):
        df.loc[len(df)] = [str(timestamp[j]), x[j], y[j], z[j]] # Adiciona os novos valores em uma nova linha do DataFrame """
    df.to_csv('{}.csv'.format(nomeArquivo))
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
forever = threading.Event()

# Cria DataFrame com as colunas referentes aos dados da coleta
df = pd.DataFrame(columns=['Timestamp','Eixo X', 'Eixo Y', 'Eixo Z'])



# Cria rota que a ESP8266 realizará o http.POST com os resultados do SAC-DM
temp_ini = time.time()
while(True):
    
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    print("true")
    message = bytesAddressPair[0]
    tempo_fim = time.time() - temp_ini
    #timestamp.append(time.time() - temp_ini)
    
    address = bytesAddressPair[1]

    eixos = format(message)
    eixos = eixos.split("'")

    print("MSG: {}".format(message))
    print("EIXOS: {}".format(eixos[1]))

    #LOW M5 BATTERY
    if(eixos[1] == "LOW_BATTERY"):
        print("|M5| > LOW_BATTERY {}".format(tempo_fim))
        
        print('\n\nSalvando coleta de dados em {}.csv'.format(nomeArquivo))        
        df.to_csv('{}.csv'.format(nomeArquivo))
        sys.exit(0)

    else:
        eixos = eixos[1].split(',') 
        #print(eixos)
        #print(eixos)

        if (len(df)==0):
            #print("entrei IF")
            df.loc[len(df)] = [str(tempo_fim), eixos[0], eixos[1], eixos[2]]

        else:
            #print("entrei no else")
            if(eixos[0] != df.loc[len(df)-1, 'Eixo X'] or eixos[1] != df.loc[len(df)-1, 'Eixo Y'] or eixos[2] != df.loc[len(df)-1, 'Eixo Z']):
                #print("entrei no else if")
                df.loc[len(df)] = [str(tempo_fim), eixos[0], eixos[1], eixos[2]]