
from tracemalloc import stop
from enlace import *
import time
import numpy as np
import time

serialName = "COM8"           

def main():
    try:
        com1 = enlace(serialName)
        com1.enable()

        print("esperando 1 byte de sacrifício")        
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("COMUNICAÇÃO ABERTA COM SUCESSO\n")
       
        print("RECEPÇÃO VAI COMEÇAR\n")

        # Recebendo a quantidade de comandos que será enviado
        nCmd, t = com1.getData(2)
        nCmdInt = int.from_bytes(nCmd, "big")
        print(f"Serão recebidos {nCmdInt} pacotes de comandos\n")
        
        lista = []
        x = 0
        while x < nCmdInt:
            # Recebendo o tamanho do pacote
            rxBufferHeader, rxHeaderLen = com1.getData(2)

            # Transformando o tamanho do pacote em um inteiro
            rxBufferResponse = int.from_bytes(rxBufferHeader, "big")

            # Recebendo o pacote
            rxBuffer, rxBufferLen = com1.getData(rxBufferResponse)
            lista.append(rxBuffer)
            x += 1

        print("Pacotes recebidos!\n")

        # Retornando quantidade de pacotes recebidos para o client
        print("Enviando a quantidade de pacotes recebidos ao client para confirmação\n")
        com1.sendData(x.to_bytes(2, byteorder="big"))
   

        print("Comunicação encerrada")
      
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()

if __name__ == "__main__":
    main()