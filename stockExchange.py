################################################################################
#
# File:         stockExchange.py
# Description:  Razred StockExchange se v casovnih korakih povezuje kot klient 
#               na stock providerja in prevzema trenutne vrednsoti fin. instrumentov.
#               Hkrati pa kot server sprejema uporabniske zahteve in izvaja akcije 
#               (buy, sell, limit buy, limit sell).
#
#               Razred ClientStockNum vsebuje stanje na klientskih racunih - 
#               kolicino posameznega fin. instrumenta glede na uporabnika
# Author:       Igor Rozman
# Created:      
# Modified:     
#               
# Language:     PYTHON (v 3.6.4)
#               
# Package:      
#
################################################################################import socket

import socket
import sys
import json
import threading
import time
from messageStockValue import MessageStockValue
from stockValueSimulator import StockValues
from stockValueSimulator import StockValueSimulator
from messageClientTran import MessageClientTran

# host in port na katerem teče simulacija stock values
HOST_STOCKSIM = 'localhost'    
PORT_STOCKSIM = 50007          
# host in port pod katerim tece stock exchange, nanj se povezujejo uporabniki
HOST_CLIENT = 'localhost'
PORT_CLIENT = 50008
# casovni interval v katerem se nalagajo StockVrednosti in se izvajajo batch opravila
timeWait = 15

# stevilo financnih instrumentov
numFinancial = 3
# stevilo registriranih uporabnikov 
numClients = 4
# multidimenzionalna tabela vsebuje stanje na klientskih racunih
# v prvi vrstici se nahajajo (genericna) imena uporabnikov 
# v prvem stolpcu se nahajajo (genericna) imena fin. instrumentov
w, h = numClients+1, numFinancial+1 
class ClientStockNum:
    def __init__(self):
        self.clientStockNum = [[0 for x in range(w)] for y in range(h)]

    # malo lepsi izpis stanja klientskih racunov
    def izpisiStanjeKR(self):
        for y in range(h):
            print(self.clientStockNum[y]) 


class StockExchange:
    threads = []  # ToDo: daemoni, na koncu jih je potrebno gracefully stopirati

    def __init__(self):
        # Vsebuje limit orderje in druge batch jobe
        self.batchOrders = []

        # Nastavimo privzete vrednosti klientskih racunov (na 0)
        self.csn = ClientStockNum()
        for y in range(h):
            self.csn.clientStockNum[y][0] = "fin" + str(y) 
            for x in range(1,w):
                if y == 0:
                    self.csn.clientStockNum[y][x] = "user" + str(x)
                else:
                    self.csn.clientStockNum[y][x] = 0

        # StockExchange se kot klient poveže na stock providerja
        t = threading.Thread(target=self.runNextCycle)
        t.setDaemon(True) 
        self.threads.append(t)
        t.start()

    # V enem ciklu Stock Exchange prebere nove vrednosti iz Stock providerja,
    # izvede batch akcije (limit buy/sell) in izpise trenutno stanje vrednosti 
    def runNextCycle(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST_STOCKSIM, PORT_STOCKSIM))
            while True:
                s.sendall(bytes('getVal','utf-8'))
                data = s.recv(1024)
                # stock exchange prejme vrednosti od stockSimulator
                ct = json.loads(str(data,'utf-8'))

                # Izpisemo trenutno stanje Stock Exchange                
                print('---Stanje Stock Exchange v trenutnem ciklu-',time.ctime(),'---')
                # 1. Novo stanje placilnih instrumentov
                print('Novo stanje vrednosti placilnih instrumentov')
                currentStockValues = ct['stockVal']
                print(currentStockValues)
                # 2. Izvedba batch oz. limitiranih orderjev
                self.doBatchOrders(currentStockValues)
                # 3. Izpisemo stanje klientskih racunov
                print('Stanje na klientskih racunih')
                self.csn.izpisiStanjeKR()
                time.sleep(timeWait)

    # Zazene se Stock Exchange v obliki serverja, ki sprejema zahteve clientov
    def run(self):
        print('Stock Exchange je zacel sprejemati kliente..')
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST_CLIENT, PORT_CLIENT))
            s.listen(1)
            while True:
                conn, addr = s.accept()
                with conn:        
                    print('***Povezal se je', addr, '***')
                    while True:
                        data = conn.recv(1024)
                        if not data: break
                        msg = json.loads(str(data,'utf-8'))
                        # ToDo: naredi error checking nad prejetimi podatki
                        # izvedi poslovno logiko nad prejetimi podatki
                        self.doBussinesLogic(msg)
                        conn.sendall(bytes('OK','utf-8'))

    # Izvede poslovno logiko glede na klientov message
    def doBussinesLogic(self, msg):
        # izluscimo vrednosti iz sporocila
        clientID = int(msg['clientID'])
        finID = int(msg['finID'])
        akcija = int(msg['akcija'])
        kolicina = int(msg['kolicina'])
        if akcija == 1:   # buy
            self.csn.clientStockNum[finID][clientID] += kolicina 
        elif akcija == 2: # sell
            self.csn.clientStockNum[finID][clientID] -= kolicina 
        elif akcija == 3 or akcija == 4: # limit sell/by dodamo v batch orderje
            self.batchOrders.append(msg)

    # Izvede aktivnosti nad batch orderji. Za vhod dobi trenutne vrednosti placilnih instrumentov.
    def doBatchOrders(self, currentStockValues):
        # pregledamo vse batch orderje
        for msg in self.batchOrders:
            clientID = int(msg['clientID'])
            finID = int(msg['finID'])
            akcija = int(msg['akcija'])
            kolicina = int(msg['kolicina'])
            vrednost = int(msg['vrednost'])
            # limit buy
            if akcija == 3:
                if int(currentStockValues[finID-1][1]) < vrednost:
                    self.csn.clientStockNum[finID][clientID] += kolicina
                    print('### Izvršen limit buy za narocilo ###')
                    print(msg)
                    self.batchOrders.remove(msg)
            # limit sell
            elif akcija == 4: 
                if int(currentStockValues[finID-1][1]) > vrednost:
                    self.csn.clientStockNum[finID][clientID] -= kolicina
                    print('### Izvršen limit sell za narocilo ###')
                    print(msg)
                    self.batchOrders.remove(msg)            
