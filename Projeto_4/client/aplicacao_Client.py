
from base64 import decode
from calendar import c
from datetime import datetime
from email import message
from http import client, server
from sys import byteorder
from enlace_Client import *
import time
import numpy as np
from random import randint, choice
from crccheck.crc import Crc16
from crccheck.checksum import Checksum16, ChecksumXor16

serialName = "COM2"                  # Windows(variacao de)

def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Communication Successfull!")


        imgR = "client/img/dog.png"
        print("Loading Image: ")
        print(" - {}".format(imgR))
        dog = open(imgR, 'rb').read()


        print(f"a imagem tem  tamanho: {len(dog)}")
        size_of_dog = int(len(dog)/114)
        print(f"a imagem sera dividida em: {size_of_dog} pacotes")


        eop = [0xAA, 0xBB, 0xCC, 0xDD]

        def writeLog(head):

            if head[0] == 4:
                message = str(datetime.now()) + " / recebimento /" + str(head[0]) + " /" +str(head[5])
            
            elif head[0] != 3 and head[0] != 1: #h3 - numero total de pacotes ; h4 - pacote atual; h5 size; 
                message = str(datetime.now()) + " / recebimento /" + str(head[0]) + " /" + str(head[5]) + " /" + str(head[4]) + " /" + str(head[3])

            else: #h3 - numero total de pacotes ; h4 - pacote atual; h5 size; 
                message = str(datetime.now()) + " / envio /" + str(head[0]) + " /" + str(head[5]) + " /" + str(head[4]) + " /" + str(head[3])

            log = "client\log\Client5.txt"
            with open(log, 'a') as f:
                f.write(message)
                f.write('\n')



            # return "lol"
        #eh o handhsake, enviada pelo client para ver se pode comecar a transmissao
        #tipo 2 eh a resposta do handshake, eh recebida pelo client
        def type_1():
            #lista de ints, cada int sera escrito como um byte quando byte(l)
            #lista do head
            l = [1, 0, 0, size_of_dog, 0, 10, 0, 0, 0, 0]       
            #fazemos uma lista de bytes com a lista de ints, cada byte tem tamanho e posicao igual ao do int equivalente na lista
            handshake = bytes(l + eop) 
            pacote = handshake  #temporario     

            #mandando o HandShake:
           # print("mandando o handhshake")
            txBuffer = pacote
            #print(f"enviando: {txBuffer}")
            time.sleep(0.1)
            com1.sendData(np.asarray(txBuffer))
            writeLog(l)
            print("mandando o handhshake")
            print(f"handhsake: {list(pacote)}")

        
        #manda a imagem, monta o pacote baseado no index recebido
        #TODO re-escrever o codigo 
        #tipo 3 eh a mensagem de dados, o client envia os dados e escuta uma resposta
        def type_3(i):
            #print("sending")
            #variando o tamanho da payload quando chegamos no ultimo pacote
            

            if i < 10:
                payload =  dog[114*(i): 114*(i + 1)]

                crc = Crc16().calc(payload)
                crc = int.to_bytes(crc, 2, byteorder='big')
                crc1 = crc[0]
                crc2 = crc[1]
                
                h = [3, 0, 0, size_of_dog, i, 114, 0, 0, crc1, crc2]
                pacote = bytes(h + list(payload) + eop)

            else: 
                print("ultimo pacote!!")
                size = len(list(dog[114*i: ]))
                
                payload =  dog[114*(i):]

                crc = Crc16().calc(payload)
                crc = int.to_bytes(crc, 2, byteorder='big')
                crc1 = crc[0]
                crc2 = crc[1]
                
                h = [3, 0, 0, size_of_dog, i, size, 0, 0, crc1, crc2]
                pacote = bytes(h + list(payload) + eop)
                

            txBuffer = pacote
            print(f"enviando dados: {list(txBuffer)}")
            time.sleep(0.1)
            com1.sendData(np.asarray(txBuffer))
            writeLog(h)
        
        #TODO envia uma mensagem tipo 5, e corta a conecao
        def type_5():
            h = [5, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            pacote = bytes(h + eop)

            txBuffer = pacote
            print(txBuffer)
            time.sleep(0.1)
            com1.sendData(np.asarray(txBuffer))
            writeLog(h)
        
            print("TIME OUT")
            print(":(")
            com1.disable()
            exit()

        def handler(i): #handles o recebimento
            print("ouvindo o recebimento")
            #timers: a == timer 1, b == timer 2
            t_i_1 = time.time()
            t_i_2 = time.time()
            timer_1 = 0
            timer_2 = 0
            l = 0
            while l < 10: #l = len do buffer
                l = com1.rx.getBufferLen()
                timer_1 = time.time() - t_i_1
                timer_2 = time.time() - t_i_2

                if timer_1 >= 5:
                    timer_1 = 0
                    t_i_1 = time.time()
                    print("re-enviando o pacote de dados")
                    if i == 0:
                        type_1()    
                    else:
                        type_3(i - 1) #para ser o pacote correto
                    
                elif timer_2 >= 20:
                    type_5()
                
            #l = 10  
            if l >= 10:
                txLen = 10
                time.sleep(0.1)
                rxBuffer, nRx = com1.getData(txLen) #pegando o HEAD, 1 = timer 1, 5 segundos
                #print(f"recebido: {list(rxBuffer)}")

                rxBuffer = list(rxBuffer)
                codigo = rxBuffer[0]
                pacote_correto = rxBuffer[6]
                print(f"codigo: {codigo}")
                print(f"pacote correto: {pacote_correto}")
                writeLog(rxBuffer)

            txLen = 4
            time.sleep(0.1)
            rxBuffer, nRx = com1.getData(txLen)

            print(f"eop: {list(rxBuffer)}")
            print(f"codigo: {codigo}")

            if codigo == 2:
            
                return (True, pacote_correto)

            elif codigo == 4:
                return (True, pacote_correto)

            elif codigo == 5:
                type_5()
                
            else:
                print(f"pacote correto: {pacote_correto}")
                return (False, pacote_correto )

        #comecando a transmissao:
        start = False
        while(start is False):
            type_1()
            time.sleep(5) 
            start = handler(0)
            if not start[0]:
                print("HandShake ERROR, retrying")

        if start:
            acabou = False
            i = 1
            error = False
            
            while not acabou:
                
                if i <= size_of_dog:

                    if i > 1:
                        
                        next_pkg, ultimo_pacote = handler(i)
                        

                    else: 
                        next_pkg = True
                        ultimo_pacote = 1
                    
                    if not next_pkg:
                        
                        i = ultimo_pacote
                        type_3(i)
                        i+=1

                    if next_pkg: 
                        type_3(i)
                        i += 1

                else: 
                    acabou = True
                    print("Terminou! :)")
                    com1.disable()
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()


        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()

    # answer = int(input("Client(0.1) or Server(0)?"))

    # if answer is 1:
    #     print("client")

    # if answer is not 1:
    #     print("server")

    # ready = input("Press ENTER when ready")
    # main(answer)
    