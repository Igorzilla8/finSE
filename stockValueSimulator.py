################################################################################
#
# File:         stockValueSimulator.py
# Description:  Razred StockValueSimulator predstavlja server storitev,
#               ki sprejema klice in vraca trenutno vrednost fin. instrumentov.
#
#               Razred StockValueGenerator kreira nove vrednosti za fin. 
#               instrumente na dolocen casovni interval. Vrednosti so shranjene
#               v dvodimenzionalni tabeli.
#
# Author:       Igor Rozman
# Created:      
# Modified:     
#               
# Language:     PYTHON (v 3.6.4)
#               
# Package:      
#
################################################################################
import socket
import sys
import json
import time
import threading
import random
from messageStockValue import MessageStockValue

HOST_STOCKSIM = 'localhost'       # Streznik pod katerim se zazene storitev
PORT_STOCKSIM = 50007             # Port
# stevilo fin. instrumentov
numFinancial = 3
# dvodimenzionalna tabela vsebuje imena in vrednosti fin. instrumentov
w, h = 2, numFinancial
# zacetne vrednosti fin. instrumentov so na intervalu (a,b)
a = 100
b = 200
# casovni interval pri katerem se spreminjajo vrednosti v sekundah
timeWaitChangeFin = 30
# vrednost random intervala v katerem se lahko spreminja vrenost 
# fin. instrumenta; primer (x - rand(5), x + rand(5))
sizeOfChange = 5


# Vrednosti financnih instrumentov hranimo v dvodimenzionalni tabeli, prvi element je
# ime instrumenta, drugi element je njegova vrednost. 
class StockValues:
    def __init__(self):
        self.finInstruments = [[0 for x in range(w)] for y in range(h)]


# Razred generira "neke" nakljucne vrednosti za financne instrumente. Vsak instrument
# je sestavljen iz njegovega imena in vrednosti. Generator v metodi  changeValuesOfFinInstruments
# periodicno spreminja vrednosti intrumenta.
class StockValueGenerator:

    # inicializacija financnih instrumentov z nakljucnimi vrednostmi
    def __init__(self):
        self.sv = StockValues()
        print('-Initialized-----------------------------------------------------------')
        for y in range(h):
            # prvi stolpec vsebuje (genericna) imena fin. instrumentov
            self.sv.finInstruments[y][0] = "fin" + str(y+1) 
            # drugi stolpec vsebuje vrednosti fin. instrumentov
            self.sv.finInstruments[y][1] = random.randint(a, b+1)
        print(self.sv.finInstruments)

    # spreminjanje vrednosti financih instrumentov po enem intervalu
    def changeValuesOfFinInstruments(self):
        while True:
            print('---Sprememba vrednosti placilnih instrumentov--',time.ctime(),'---')
            for y in range(h):
                self.sv.finInstruments[y][1] = self.sv.finInstruments[y][1] + random.randint(-sizeOfChange, sizeOfChange)
            print(self.sv.finInstruments)
            time.sleep(timeWaitChangeFin)


# StockValueSimulator se zazene kot server, ki vraca klientom trenutne
# vrednosti fin instrumentov
class StockValueSimulator:
    threads = [] # ToDo: daemoni, na koncu jih je potrebno se gracefully stopirati

    def __init__(self):
        # Zazene se generator stock vrednosti kot daemon thread
        self.sg = StockValueGenerator()
        t = threading.Thread(target=self.sg.changeValuesOfFinInstruments)
        t.setDaemon(True) 
        self.threads.append(t)
        t.start()

    def run(self):
        # Zazene se Stock Value Simulator v obliki serverja, ki clientom sporoča trenutne vrednosti instrumentov
        # Sprocila, ki jih Stock Value Simulator so JSON nizi v katerih je serializiran objekt MessageStockValue
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST_STOCKSIM, PORT_STOCKSIM))
            s.listen(1)
            conn, addr = s.accept()
            with conn:        
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data: break
                    # ToDo: preveri kaj si pravzaprav dobil v 'data' in razvij
                    # ustrezno logiko
                    msv = MessageStockValue(1,1,self.sg.sv.finInstruments) 
                    conn.sendall(bytes(msv.toJSON(),'utf-8'))
