from tracemalloc import stop


from enlace import *
import time
import numpy as np
import random
import time
import sys
import math

serialName = "COM8"                   

def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()

        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("COMUNICAÇÃO ABERTA COM SUCESSO\n")
       
        print("TRANSMISSÃO VAI COMEÇAR\n")

        # * HANDSHAKE
        while True:
            print("Enviando Handshake\n")
            com1.sendData(b'00')
            time.sleep(.05)
            print("Aguardando retorno...\n")
            # rxBuffer, nRx = com1.getData(2)
            tempo1 = time.time()
            while com1.rx.getIsEmpty():
                tempo2 = time.time()

                if tempo2 - tempo1 > 5:
                    a = input('Deseja tentar novamente? (s/n) ')
                    

                    if a == 's':
                        com1.sendData(b'00')
                        tempo1 = time.time()
                        tempo2 = time.time()
                    elif a == 'n':
                        com1.disable()
            else:
                com1.rx.clearBuffer()
                time.sleep(.1)
                print("Handshake recebido!\n")
                break
         
        # Pegando o caminho da imagem a ser transmitida
        pathImageTx = "image/asmolgus.png"
        # Agora vamos abrir o arquivo da imagem e lê-lo com um arquivo binário
        ImageTx = open(pathImageTx, 'rb').read()
        print(ImageTx)
        # Vamos agora saber o tamanho da imagem em número inteiro e em bytes
        lenImage = len(ImageTx)
        lenImageTxBytes = lenImage.to_bytes(2, byteorder="big") 
        # Agora que temos o tamanho da imagem nós podemos saber quantos pacotes serão enviados
        nPacotes = math.ceil(lenImage/50)
        nPacotesBytes = nPacotes.to_bytes(2, byteorder="big")

        # Mandando a quantidade de pacotes que serão enviados para o server
        print(f"A quantidade de pacotes que serão enviados é {nPacotes}\n")
        com1.sendData(nPacotesBytes)
        time.sleep(1)

        # Criando lista de payloads para serem enviados
        payloads = [ImageTx[i:i + 50] for i in range(0, len(ImageTx),50)]

        # ! Vamos criar um LOOP para enviarmos sequencialmente o Head, PayLoad e EOP de cada pacote
        contPacotes = 0 # Somar 1 para dar o erro
        
        while contPacotes < nPacotes:
            print(f"Enviando informações do pacote {contPacotes+1}")

            # * HEAD
            nPacote = (contPacotes+1).to_bytes(5, byteorder="big") # Número do pacote
            tamPayload = (len(payloads[contPacotes])).to_bytes(5, byteorder="big") # Tamanho do pacote
            HEAD = nPacote + tamPayload
            # * PayLoad
            payload = payloads[contPacotes] # Pacote
            # else:
            EOP = b'0'
            #j += 1
            
            tamanhoPacote = (len(HEAD + payload + EOP)).to_bytes(2,byteorder="big")
            com1.sendData(tamanhoPacote)
            time.sleep(1)
            com1.sendData(HEAD + payload + EOP)
            time.sleep(1)

            # Recebendo confirmação se o pacote foi enviado corretamente
            confirmacao, confrimacaoLen = com1.getData(1)

            if confirmacao == b'2':
                pacoteCerto, pacoteCertoLen = com1.getData(2)
                contPacotes = int.from_bytes(pacoteCerto, "big") - 1
                print(f"EOP está errado! Precisamos reenviar o pacote {contPacotes+1}")
                print(contPacotes)

            elif confirmacao == b'1':
                pacoteCerto, pacoteCertoLen = com1.getData(2)
                contPacotes = int.from_bytes(pacoteCerto, "big") - 1
                print(f"Número do pacote está errado! Precisamos reenviar o pacote {contPacotes + 1}")
                print(contPacotes)

            else:
                # if contPacotes == 1:
                #     contPacotes += 2
                # else:
                contPacotes += 1
                

        
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
from tracemalloc import stop



# while com1.rx.getIsEmpty():
#                 tempo2 = time.time()

#                 if tempo2 - tempo1 > 5:
#                     a = input('Deseja tentar novamente? (s/n) ')

#                     if a == 's':
#                         com1.sendData(b'00')
#                     elif a == 'n':
#                         com1.disable()