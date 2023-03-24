from crccheck.crc import Crc16

from enlace import *
import time
import numpy as np
from random import randint, choice
from datetime import datetime


serialName = "COM8"                  # Windows(variacao de)


def main():
    try:
       
        com1 = enlace(serialName)
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Communication Successfull!")


        def log_recebe(tipo,tamanho, n_atual, n_total, local):
            agora = str(datetime.now())
            string_log = agora + '/recebe/' + str(tipo) + '/' + str(tamanho) + '/' + str(n_atual) + '/' +str(n_total)
            with open(local, 'a') as f:
                f.write(string_log)
                f.write('\n')

        def log_envio(tipo,local):
            agora = str(datetime.now())
            string_log = agora + '/envio/' + str(tipo) + '/14'
            with open(local, 'a') as f:
                f.write(string_log)
                f.write('\n')


        def tipo2():

            head = [2, 0, 0, 0, 0, 0, 0, 0 ,0 ,0] #numero total a ser visto
            eop = [0xAA, 0xBB, 0xCC, 0xDD]

            pacote = head + eop
            txBuffer = pacote

            log_envio(2,"log/Server5.txt")
            time.sleep(0.1)
            com1.sendData(np.asarray(bytes(txBuffer)))

        def tipo4(ultimo_pacote):

            head = [4, 0, 0, 0, 0, 0, 0, ultimo_pacote ,0 ,0]
            eop = [0xAA, 0xBB, 0xCC, 0xDD]

            pacote = head + eop
            txBuffer = pacote

            log_envio(4,"log/Server5.txt")
            time.sleep(0.1)
            com1.sendData(np.asarray(bytes(txBuffer)))

        def tipo5():

            head = [5, 0, 0, 0, 0, 0, 0, 0 ,0 ,0] #numero total a ser visto
            eop = [0xAA, 0xBB, 0xCC, 0xDD]

            pacote = head + eop
            txBuffer = pacote

            log_envio(5,"log/Server5.txt")
            time.sleep(0.1)
            com1.sendData(np.asarray(bytes(txBuffer)))
        
        def tipo6(numero_pacote):

            head = [6, 0, 0, 0, 0, 0, numero_pacote, 0 ,0 ,0] #numero total a ser visto
            eop = [0xAA, 0xBB, 0xCC, 0xDD]

            pacote = head + eop
            txBuffer = pacote

            log_envio(6,"log/Server5.txt")
            time.sleep(0.1)
            com1.sendData(np.asarray(bytes(txBuffer)))

        
        identificador = 10
        pkg = 1
        lista_imagem = []
        ocioso = True

        while ocioso:

            print("ouvindo handshake:")

            txLen = 10
            rxBuffer, nRx = com1.getData(txLen)

            rxBuffer = list(rxBuffer)
            print(rxBuffer)

            tipo_mensagem = rxBuffer[0]
            numero_de_pacotes = rxBuffer[3]

            if tipo_mensagem == 1: # ver se é handshake

                id_mensagem = rxBuffer[5]

                if id_mensagem == identificador: #ver se é para o server

                    ocioso = False
                    time.sleep(1)

                else:
                    time.sleep(1)
            else:
                time.sleep(1)
            
            #eop do handshake
            txLen = 4
            rxBuffer, nRx = com1.getData(txLen)
        
        #envia a mensagem de tipo 2
        tipo2()

        time.sleep(5)

        cont = 1
        eop = [170, 187, 204, 221]


        img = b''

        while cont < numero_de_pacotes:

            l = 0

            ti_1 = time.time() 
            ti_2 = time.time()
            timer_1 = 0
            timer_2 = 0

            print("ouvindo mensagem:")


            while l < 10:
                l = com1.rx.getBufferLen()

                timer_1 = time.time()-ti_1
                timer_2 = time.time()-ti_2

                # print(timer_2)

                if timer_2 >= 20:
                    ocioso == True
                    tipo5()
                    print(':-(')
                    print('encerrando a comunição por tempo')
                    com1.disable()
                    exit()

                if timer_1 >= 2:
                    tipo4(pkg)
                    timer_1 = 0
                    ti_1 = time.time()
                    print('pedindo a imagem novamente')

            if l >= 10:
                txLen = 10
                rxBuffer, nRx = com1.getData(txLen)
                head = rxBuffer
                print('peguei head')
            

            head_n = list(head)

            last_pkg = head[7]
            print(head_n)
            
            tipo_mensagem = rxBuffer[0]
            numero_do_pacote = rxBuffer[4]
            numero_total = rxBuffer[3]
            tamanho_payload = rxBuffer[5]

            crc1_check = rxBuffer[8]
            crc2_check = rxBuffer[9]

            print('analisando o head')

            time.sleep(1)

            if tipo_mensagem == 3: #tipo de mensagem certa
                    
                if pkg == numero_do_pacote: #verifica o numero de pkg junto com o numero do pacote da mensagem
                    
                    #payload
                    log_recebe(tipo_mensagem,tamanho_payload, numero_do_pacote, numero_total, "log/Server5.txt")

                    txLen = tamanho_payload
                    time.sleep(0.1)
                    rxBuffer, nRx = com1.getData(txLen)
                    print('peguei payload')
                    # lista_imagem.append(rxBuffer)

                    pct_imagem = rxBuffer

                    crc = Crc16().calc(rxBuffer)
                    crc = int.to_bytes(crc, 2, byteorder='big')

                    crc1_check = int.to_bytes(crc1_check, 1, byteorder='big')
                    crc2_check = int.to_bytes(crc2_check, 1, byteorder='big')
                    crc_check = crc1_check+crc2_check

                    #eop
                    print('escutando eop')
                    txLen = 4
                    time.sleep(0.1)
                    rxBuffer, nRx = com1.getData(txLen)

                    print('peguei eop')

                    eop_mensagem = rxBuffer # pegar os 4 ultimos elementos para matar o eop

                    print(list(eop_mensagem))
                    print(eop)

                    if eop == list(eop_mensagem) and crc == crc_check:

                        print('mais um')

                        img+=pct_imagem
                        
                        pkg+=1
                        print('pkg: ', pkg)
                        
                        tipo4(last_pkg)
                        
                        cont+=1
                    

                    else:
                        tipo6(pkg)
                        tamanho_payload = rxBuffer[5]
                        log_recebe(tipo_mensagem,tamanho_payload, numero_do_pacote, numero_total, "log/Server5.txt")

                        txLen = tamanho_payload
                        time.sleep(0.1)
                        rxBuffer, nRx = com1.getData(txLen)

                        txLen = 4
                        time.sleep(0.1)
                        rxBuffer, nRx = com1.getData(txLen)

                        print('o eop nao bateu')
                        print('tirando do buffer')
                else:
                    tipo6(pkg)
                    tamanho_payload = rxBuffer[5]
                    log_recebe(tipo_mensagem,tamanho_payload, numero_do_pacote, numero_total, "log/Server5.txt")

                    txLen = tamanho_payload
                    time.sleep(0.1)
                    rxBuffer, nRx = com1.getData(txLen)

                    txLen = 4
                    time.sleep(0.1)
                    rxBuffer, nRx = com1.getData(txLen)

                    print('o numero do pacote nao bateu com o esperado')
                    print('tirando do buffer')
            else:
                log_recebe(tipo_mensagem,tamanho_payload, numero_do_pacote, numero_total, "log/Server5.txt")
                time.sleep(1)

        print('SUCESSO DE ENVIO')

        imgW = "img/copyDog.png"
        f = open(imgW, 'wb')
        f.write(img)
        f.close()
        print("acabou de fazer a imagem!")


        print("SUCESSO NA CONSTRUÇÃO DA IMAGEM")
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
        




        