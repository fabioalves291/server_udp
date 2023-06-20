import socket   
import sys
import os
import time

def menu():
    print('''
\\f         para listar arquivos
\\f:        para baixar arquivo(mais o nome do arquivo)
\\help      para ver o menu novamente
\\exit      para fechar o client'''
    )

def sair():
    if input_menu in '2°':
        socket_client.close()
        quit

try:
	os.mkdir('arquivos_cliente')
except:
	pass


ipserver    = 'localhost'
portserver  = 2000
codepage    = 'UTF-8'
buffersize  = 512
menu()
while True:
    try:
        input_menu = input(': ')
        if input_menu == '\\help':
            print(menu())
            continue
        socket_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_client.sendto(input_menu.encode(codepage),(ipserver,portserver))
        msg,adress = socket_client.recvfrom(buffersize)
        try:
            msgdecode = msg.decode(codepage)
        except UnicodeDecodeError:
            pass
        if input_menu =='\\f':
            msgdecode = msgdecode.replace('[',' ')
            msgdecode = msgdecode.replace(']',' ')
            listmsg = msgdecode.split(',')

            for dados in listmsg:
                print(dados.replace("'",' '))
        
        elif input_menu[:3] == '\\f:':
            file = open(fr'arquivos_cliente/{input_menu[3:]}','wb') 
            inicio = True
            
            while inicio:
                msg = socket_client.recv(buffersize)
                print(msg)
                try:
                    if msg.decode(codepage) =='f':
                        inicio = False
                except UnicodeDecodeError:
                    pass
                file.write(msg)
            file.close()
            print('arquivo recebido')
        elif input_menu == '\\exit':
            socket_client.close()
            input('Enter para continuar')
            quit()
        else:
            print(msgdecode)
        sair()
    except:
        continue
        print("err")
        time.sleep(2)
