#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Camada de Enlace
####################################################

# Importa pacote de tempo
import time

# Threads
import threading

# Class
class RX(object):
  
    def __init__(self, fisica):
        self.fisica      = fisica
        self.buffer      = bytes(bytearray())
        self.threadStop  = False
        self.threadMutex = True
        self.READLEN     = 1024

    def thread(self): 
        while not self.threadStop:
            if(self.threadMutex == True):
                rxTemp, nRx = self.fisica.read(self.READLEN)
                if (nRx > 0):
                    self.buffer += rxTemp  
                time.sleep(0.01)

    def threadStart(self):       
        self.thread = threading.Thread(target=self.thread, args=())
        self.thread.start()

    def threadKill(self):
        self.threadStop = True

    def threadPause(self):
        self.threadMutex = False

    def threadResume(self):
        self.threadMutex = True

    def getIsEmpty(self):
        if(self.getBufferLen() == 0):
            return(True)
        else:
            return(False)

    def getBufferLen(self):
        return(len(self.buffer))

    def getAllBuffer(self, len):
        self.threadPause()
        b = self.buffer[:]
        self.clearBuffer()
        self.threadResume()
        return(b)

    def getBuffer(self, nData):
        self.threadPause()
        b           = self.buffer[0:nData]
        self.buffer = self.buffer[nData:]
        self.threadResume()
        return(b)

    def getNData(self, size):
        tempoI = time.time()
        while(self.getBufferLen() < size):
            time.sleep(0.05)
            tempoF = time.time()
            if (tempoF - tempoI) >= 5:
                return "Servidor inativo! Vamos tentar reenviar o pacote.\n"

        return(self.getBuffer(size))

    def getNDataServer(self, size):
        tempoI = time.time()
        while(self.getBufferLen() < size):
            time.sleep(0.05)
            tempoF = time.time()
            if (tempoF - tempoI) >= 2:
                print("Pacote não recebido pós 2 segundos! Por favor envie o pacote.\n")
                tempoI = time.time()
        return(self.getBuffer(size))


    def clearBuffer(self):
        self.buffer = b""


