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
        c_init = b'\x05'  # sendo que o \x05 vai representar o inicio de uma serie de comandos novos.
        # comando de começo de transmissão, comando de começo de comando, comando de fim de comando, comando de fim de transmissão.
        # como verificar se nada foi perdido?

        num_com = random.randint(10, 30) # define um numero aleatorio de comandos a serem executados 
        com1
        for i in range (1, num_com):
            
            # com1.sendData(np.asarray(txBuffer))  #as array apenas como boa pratica para casos de ter uma outra forma de dados
            com1.sendData(np.asarray(comandos[random.randint(0,8)]))
            


    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()

if __name__ == "__main__":
    main()