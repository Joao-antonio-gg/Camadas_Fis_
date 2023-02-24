from tracemalloc import stop

from enlace import *
import time
import numpy as np
import random
import time
import sys

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

# Definindo os comandos a serem enviados


serialName = "COM5"                    

def main():
    try:    
        com1 = enlace(serialName)
        c1 = b'\x00\x00\x00\x00'
        c2 = b'\x00\x00\xAA\x00'
        c3 = b'\xAA\x00\x00'
        c4 = b'\x00\xAA\x00'
        c5 = b'\x00\x00\xAA'
        c6 = b'\x00\xAA'
        c7 = b'\xAA\x00'
        c8 = b'\x00'
        c9 = b'\xFF'

        # Guardando comandos em uma lista
        comandos = [c1,c2,c3,c4,c5,c6,c7,c8,c9]
        cmdTr = []

        nCmd = random.randint(10, 30)

        while len(cmdTr) < nCmd:
            cmdTr.append(random.choice(comandos))

        
        
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        print("enviando byte de sacrifício")
        com1.sendData(b'00')

        # Enviando a quantidade de comandos que será enviado
        print(f"Serão enviados {nCmd} pacotes de comandos\n")
        nPacotes = nCmd.to_bytes(2, byteorder="big")
        com1.sendData(nPacotes)
        time.sleep(.05)

        for i in cmdTr:
            # Tamanho do pacote a ser enviado
            txBufferLen = len(i)

            # Pacote a ser enviado 
            txBuffer = i        

            # Transformando o tamanho do pacote a ser enviado em bytes
            txBufferHeader = txBufferLen.to_bytes(2, byteorder="big") 

            # Enviando o tamanho do pacote em bytes
            com1.sendData(txBufferHeader)

            # Enviando o pacote
            com1.sendData(txBuffer)

            time.sleep(.05)
            
        print("Pacotes enviados!\n")  

        print("Esperando confirmação da quantidade de pacotes recebidos pelo server...\n")
        try:
            nCmdConfirmacao, t = com1.getData(2)
            nCmdConfirmacaoInt = int.from_bytes(nCmdConfirmacao, "big") 

            if nCmdConfirmacaoInt == nCmd:
                print("Quantidade de pacotes recebidos é IGUAL")
            else:
                print("Servidor não confirmou que recebeu a mensagem") 
        except:
            print("Time Out: mensagem de confirmação não recebida!")     

        
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()