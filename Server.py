from tracemalloc import stop


from enlace import *
import time
import numpy as np

import time


serialName = "COM8"                    # Windows(variacao de)

def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()

        print("esperando 1 byte de sacrifício")        
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        time.sleep(.1)
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("COMUNICAÇÃO ABERTA COM SUCESSO\n")
       
        print("RECEPÇÃO VAI COMEÇAR\n")

        # Recebendo a quantidade de comandos que será enviado
        nCmd, t = com1.getData(2)
        nCmdInt = int.from_bytes(nCmd, "big")
        print(f"Serão recebidos {nCmdInt} pacotes de comandos\n")
        
        x = 0
        while x < nCmdInt:
            # Recebendo o tamanho do pacote
            rxBufferHeader, rxHeaderLen = com1.getData(2)

            # Transformando o tamanho do pacote em um inteiro
            rxBufferResponse = int.from_bytes(rxBufferHeader, "big")

            # Recebendo o pacote
            rxBuffer, rxBufferLen = com1.getData(rxBufferResponse)

            x += 1

        print("Pacotes recebidos!\n")

        # Retornando quantidade de pacotes recebidos para o client
        print("Enviando a quantidade de pacotes recebidos ao client para confirmação\n")
        com1.sendData(nCmd)



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