import socket 
import os
import sys
import time

def datalist():
    totallist       = []
    filelist        = os.listdir('arquivos_servidor')
    for file in filelist:
        file        = str(file)
        wordspace   = 35-len(file)
        totallist.append(file +(wordspace*' ')+ (str(os.path.getsize(f'arquivos_servidor//{file}')))+' Bytes')
    return totallist


try:
	os.mkdir('arquivos_servidor')
except:
	pass

ipserver            = 'localhost'    
codepage            = 'UTF-8'
portserver          = 2000
buffersize          = 512

while True:
    try:
        socket_server   = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        try:
            socket_server.bind((ipserver, portserver))
        except:
            print("> servidor interrompido!\n> error na porta ou ip escolhido")
            time.sleep(4)
            continue
        print('servidor aberto:')
        data,adress     = socket_server.recvfrom(buffersize)
        data            = data.decode(codepage)
        print(adress,data)
        print(data[:3])
       
        if data =='\\f':
            print(adress,'solicita','Datalist')
            datasfiles  = str(datalist())
            socket_server.sendto(datasfiles.encode(codepage),adress)

        elif data == '\\exit':
            print(adress,'fecha os sistema client e server')
            socket_server.sendto('desligando client e servidor'.encode(codepage),adress)
            socket_server.close()
            quit()
                
        elif data[:3] == '\\f:':
            file        = open(fr'arquivos_servidor/{data[3:]}','rb')   
            socket_server.sendto('arquivo inexistente'.encode(codepage),adress)
            print(adress,'arquivo solicitado inexistente')
            
            filebits    = file.read(buffersize)
            while filebits: 
                print(filebits)
                socket_server.sendto(filebits,adress)
                filebits    = file.read(buffersize)
            file.close()
            socket_server.sendto('f'.encode(codepage),adress)
        else:
            print(adress,'solicita opção inválida')
            socket_server.sendto('opção invalida. Use o comando \help '.encode(),adress)   
   
        
    except:
        socket_server.sendto('data_lixo pass'.encode(codepage),adress)
        socket_server.sendto('f'.encode(codepage),adress)
        print("error")
