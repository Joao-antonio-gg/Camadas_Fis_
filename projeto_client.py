from enlace import *
import time
import numpy as np
import random 

# Definindo a porta de entrada
serialName = "COM5"

def main():
    try:
        print("Iniciou o main")
        com1 = enlance(serialName)

        # Definindo comandos (Byte array)
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


        # Criando os comandos de instrucao
        # byte inicial
        m_init = b'\x05'  # \x05 representa o inicio da sequencia de comandos
        # Vai ter um byte entre cada comando que diz o tamanho do próximo comando
        m_end = b'\x06'   # \x06 representa o fim da sequencia de comandos 

        # comando de começo de transmissão, comando de começo de comando, comando de fim de comando, comando de fim de transmissão.
        # como verificar se nada foi perdido?

        # Definindo o reebidor rxBuffer
                
        com1.enable()
        txLen = len(txBuffer)
        rxBuffer, nRx = com1.getData(txLen)

        num_com = random.randint(10, 30) # define um numero aleatorio de comandos a serem executados 
        
        com1.sendData(np.asarray(m_init))
        for i in range (1, num_com):
            # # com1.sendData(np.asarray(txBuffer))  #as array apenas como boa pratica para casos de ter uma outra forma de dados
            # com1.sendData(np.asarray(c_init))
            # com1.sendData(np.asarray(comandos[random.randint(0,8)])) 
            com_env = comandos[random.randint(0,8)]
            str_com = str(com_env)
            size = 0 # prone to bugs
            for char in str_com:
                if char == "x":
                    size += 1
            
            if size == 1:
                com1.sendData(np.asarray(b'\x01')) # o próximo comando tem tamanho 1
            if size == 2:
                com1.sendData(np.asarray(b'\x02')) # o próximo comando tem tamanho 2
            if size == 3:
                com1.sendData(np.asarray(b'\x03')) # o próximo comando tem tamanho 3
            if size == 4:
                com1.sendData(np.asarray(b'\x04')) # o próximo comando tem tamanho 4
            else:
                print ("Deu erro no loop de size")
                break

            com1.sendData(np.asarray(com_env)) # comando sendo enviado
            # Após o c_end, o proximo loop só pode iniciar se o servidor confirmar que a mensagem foi recebida. 

            if com1.getData(txLen) != 1: # o servidor não confirmou que recebeu uma mensagem:
                print("Servidor não confirmou que recebeu a mensagem")
                break            

        com1.sendData(np.asarray(m_end))
 
        for i in range(5,0,-1): 
            com1.getData(txLen)
            if rxBuffer == '\x1B':
                print("Sucesso!")
                break
            else:
                time.sleep(1)


    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()

if __name__ == "__main__":
    main()