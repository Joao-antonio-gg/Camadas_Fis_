#####################################################
# Camada Física da Computação
#Carareto
####################################################

from tracemalloc import stop
from enlace import *
import time
import numpy as np
import sys
import math
from datetime import datetime
from crccheck.crc import Crc16
from crccheck.checksum import Checksum16

#  python -m serial.tools.list_ports

com1 = enlace('COM3')

class Client:

    def __init__(self, file, serialName):
        #self.clientCom = None
        self.serialName = serialName
        self.head = 0
        self.file = file
        self.eop = 0x00000000.to_bytes(4, byteorder="big")
        self.payloads = 0
        self.h0 = 0 # tipo de mensagem
        self.h1 = b'\x00' # livre
        self.h2 = b'\x00' # livre
        self.h3 = 0 # número total de pacotes do arquivo
        self.h4 = 0 # número do pacote sendo enviado
        self.h5 = 0 # se tipo for handshake:id do arquivo; se tipo for dados: tamanho do payload
        self.h6 = b'\x00' # pacote solicitado para recomeço quando há erro no envio.
        self.h7 = 0 # último pacote recebido com sucesso.
        self.h8 = b'\x00' # CRC
        self.h9 = b'\x00' # CRC
        self.logs = ''


    def startClient(self):
        self.clientCom = enlace(self.serialName)
        self.clientCom.enable()


    def closeClient(self):
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        self.clientCom.disable()
        exit()


    # Quebra a imagem nos payloads
    def createPayloads(self):
        self.payloads = [self.file[i:i + 114] for i in range(0, len(self.file), 114)]
        return self.payloads

    # Define o tipo da mensagem
    def defTypeMsg(self, n):
        self.h0 = (n).to_bytes(1, byteorder="big")
        # Mensagem do tipo Handshake
        if n == 1:
            self.h5 = b'\x00' # ? o que é o id do arquivo
        # Mensagem do tipo dados
        elif n == 3:
            self.h5 = len(self.payloads[int.from_bytes(self.h4,"big")-1])
            self.h5 = (self.h5).to_bytes(1, byteorder="big")

    def defNumMsg(self,n):
        self.h4 = (n).to_bytes(1, byteorder="big")
        self.h7 = (n-1).to_bytes(1, byteorder="big")

    def createCRC(self):
        data = self.payloads[int.from_bytes(self.h4,"big") - 1]
        if int.from_bytes(self.h4,"big") - 1 == 2:
            data = self.payloads[1]
        crc1, crc2 = Crc16.calc(data).to_bytes(2,byteorder='big')
        self.h8 = crc1.to_bytes(1,byteorder='big')
        self.h9 = crc2.to_bytes(1,byteorder='big')

    # Define a quantidade de pacotes que serão enviados
    def qtdPacotes(self):
        lenImage = len(self.file)
        h3 = math.ceil(lenImage/114)
        self.h3 = (h3).to_bytes(1, byteorder="big")

    # Cria a composição do head
    def createHead(self):
        self.head = self.h0+self.h1+self.h2+self.h3+self.h4+self.h5+self.h6+self.h7+self.h8+self.h9

    # Cria pacote  
    def createPacote(self):
        return self.head + self.payloads[int.from_bytes(self.h4,"big") - 1] + self.eop
        
    # Checa o tempo máximo para a resposta do servidor
    def SendWait(self, pacote):
        timeMax = time.time()
        while True: 
            self.clientCom.sendData(pacote)
            self.createLog(pacote, 'envio')
            time.sleep(.5)
            confirmacao, lenConfimacao = self.clientCom.getData(15)
            timeF = time.time()
            if timeF - timeMax >= 25:
                print("Servidor não respondeu após quarta tentativa. Cancelando comunicação.")
                break
            elif type(confirmacao) == str:
                print(confirmacao)
            else:
                return confirmacao

    # Realiza o handshake
    def handshake(self):
        payload = b'\x00'
        self.defTypeMsg(1)
        self.h3 = b'\x00'
        self.h4 = b'\x00'
        self.h7 = b'\x00'
        self.createHead()
        pacote = self.head + payload + self.eop
        return self.SendWait(pacote)

    # Checa o tipo de mensagem na confirmação enviada pelo servidor
    def checkTypeMsg(self, confirmacao):
        #typeMsg = int.from_bytes(confirmacao[0], "big")
        if confirmacao[0] == 4:
            self.createLog(confirmacao, 'recebimento')
            print(confirmacao[7])
            print("Tudo certo! O servidor recebeu o pacote corretamente.")
        else:
            self.createLog(confirmacao, 'recebimento')
            numPacoteCorreto = confirmacao[7]
            print(f"Uhmm, algo deu errado no envio :( Precisamos reenviar o pacote {numPacoteCorreto}")
            return numPacoteCorreto
    
    
    # Escreve os logs
    def createLog(self, data, tipo):
        tempo = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        tipoMsg = data[0]
        tamMsg = len(data)
        pacoteEnviado = data[4]
        totalPacotes = data[3]
        self.logs += f"{tempo} / {tipo} / {tipoMsg} / {tamMsg} / {pacoteEnviado} / {totalPacotes}\n"
        
    def writeLog(self):
        with open(f'Projeto 4 - protocolo ponto a ponto/logs/logClient.txt', 'w') as f:
            f.write(self.logs)
                
            
serialName = "COM3"     
path = "Projeto 4 - protocolo ponto a ponto/Imagens/txImage.png"  
file = open(path, 'rb').read()           

def main():
    try:
        
        # * INICIALIZANDO CLIENT
        cliente = Client(file, 'COM3')
        cliente.startClient()

        # * HANDSHAKE
        print("Iniciando HandShake\n")
        if cliente.handshake() is None:
            cliente.closeClient()
        print("Handshake realizado com sucesso! Servidor está pronto para o recebimento da mensagem.\n")

        # * ENVIO DOS PACOTES
        print("Agora vamos realizar o início do envio dos pacotes\n")
        payloads = cliente.createPayloads()
        # h3 = quantidade total de pacotes
        cliente.qtdPacotes()
        # h4 = número do pacote sendo enviado
        h4 = 1
        # último pacote enviado com sucesso
        cont = 0
        while cont < int.from_bytes(cliente.h3, "big"):
            print(f"Enviando informações do pacote {h4}")
            cliente.defNumMsg(h4)
            cliente.createCRC()
            print(cliente.h8, cliente.h9)
            cliente.defTypeMsg(3)
            cliente.createHead()
            pacote = cliente.createPacote()
            confirmacao = cliente.SendWait(pacote)

            if confirmacao is None:
                cliente.closeClient()

            numPacote = cliente.checkTypeMsg(confirmacao)
            if numPacote is None:
                # if h4 == 2:
                #     h4 += 2
                #     cont +=1
            # else:
                h4 += 1
                cont += 1
            else:
                h4 = numPacote
                cont = numPacote - 1

        cliente.writeLog()
        # * FECHANDO CLIENT
        cliente.closeClient()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()


# data = bytearray.fromhex("DEADBEEF")
# crc = Crc16.calc(data).to_bytes(2,byteorder='big')
# crc1, crc2 = Crc16.calc(data).to_bytes(2,byteorder='big')
# h8 = crc1.to_bytes(1,byteorder='big')
# h9 = crc2.to_bytes(1,byteorder='big')
# checksum = Checksum16.calc(data)

# print(crc)
# print(h8, h9)
# print(checksum)