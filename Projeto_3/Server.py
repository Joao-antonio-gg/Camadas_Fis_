
from enlace import *
import time
import numpy as np

import time

serialName = "COM2"     

def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()

        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("COMUNICAÇÃO ABERTA COM SUCESSO\n")
       
        print("RECEPÇÃO VAI COMEÇAR\n")

        # * HANDSHAKE
        print("Esperando Handshake...\n")
        handShake, lenHS = com1.getData(2)
        print("Enviando retorno...\n")
        com1.sendData(handShake)
        time.sleep(.05)
        print("Handshake enviado!\n")
        

        # Recebendo a quantidade de pacotes que serão enviados pelo client
        nPacotesBytes, nPacotesBytes_len = com1.getData(2)
        nPacotes = int.from_bytes(nPacotesBytes, "big") 
        print(f"Serão enviados {nPacotes} pacotes\n")

        #Cria LOOP para recebermos sequencialmente o Head, PayLoad e EOP de cada pacote
        contPacotes = 0 # Somar 1 para o erro 4 
        ImageRx = b'00'
        while contPacotes < nPacotes:
            print(f"Recebendo informações do pacote {contPacotes+1}")

            # * Recebendo Tamanho do pacote
            pacoteBytes, pacoteLenBytes = com1.getData(2)
            tamanhoPacote = int.from_bytes(pacoteBytes, "big")

            # * Recebendo pacote
            pacote, lenPacote = com1.getData(tamanhoPacote)
            # HEAD
            nPacote = int.from_bytes(pacote[0:5], "big")
            tamPayload = int.from_bytes(pacote[5:10], "big")
            # PayLoad
            payload = pacote[10:tamPayload + 10]
            # EOP
            EOP = pacote[tamPayload + 10:len(pacote)]            

            # Sem erros = b'0'
            semErro = b'0'
            # Erro de número do pacote = b'1'
            numErro = b'1'
            # Erro de EOP = b'2'
            eopErro = b'2'
            

            if EOP != b'0':
                print(f"EOP está diferente do esperado! Por favor reenvie o pacote {contPacotes+1}\n")
                # Enviando código de erro
                com1.sendData(eopErro)
                time.sleep(1)
                # Enviando mensagem pedindo o reenvio do pacote correto
                pacoteCerto = (contPacotes+1).to_bytes(2, byteorder="big")
                com1.sendData(pacoteCerto)
                time.sleep(1)

            elif nPacote != contPacotes+1:
                print(f"A ordem do pacote está errada! Por favor envie o pacote {contPacotes+1}\n")
                # Enviando código de erro
                com1.sendData(numErro)
                time.sleep(1)
                # Enviando mensagem pedindo o reenvio do pacote correto
                pacoteCerto = (contPacotes+1).to_bytes(2, byteorder="big")
                com1.sendData(pacoteCerto)
                time.sleep(1)
                
            else:
                # * Recebendo PayLoad
                ImageRx += payload
                # Enviando confirmação de que está tudo certo com o pacote
                com1.sendData(b'0')
                time.sleep(1)
                contPacotes +=1


        pathImageRx = "image/rxImage.png"
        print(ImageRx[2:len(ImageRx)])
        f = open(pathImageRx, 'wb')
        f.write(ImageRx[2:len(ImageRx)+1])
        f.close()

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