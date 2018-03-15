################################################################################
#
# File:         clientSimple.py
# Description:  Razred ClientSimple prebere uporabnikovo zahtevo in jo 
#               poslje na Stock Exchange server. Izvede samo en klic in konca
#               izvajanje. Namenjen je osnovnemu testiranju in debugiranju.
#
# Author:       Igor Rozman
# Created:      
# Modified:     
#               
# Language:     PYTHON (v 3.6.4)
#               
# Package:      
#
################################################################################import socket
import sys
import json
import socket
from messageClientTran import MessageClientTran

HOST = 'localhost'    # Server na katerem tece Stock Exchange
PORT = 50008          # Port pod katerim tece Stock Exchange


class ClientSimple:

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            # ToDo: Preberi fin. vrednosti s serverja in jih predstavi uporabniku.

            # izbire uporabnika - zelo poenostavljen klientski model 
            print('-Vnos vrednosti klientskega zahtevka---------------------------')
            clientID = input('Izberite ID klienta (1,2,3 ali 4): ')
            finID = input('Izberite financi instrument (1,2 ali 3): ')
            akcija = input("Izberite akcijo (buy=1,sell=2,limitbuy=3,limitsell=4): ") 
            kolicina = input("Izberite kolicino nakupa/prodaje: ") 
            vrednost = input("Izberite ceno pri limit buy/sell akciji: ") 
            # ToDo: Izvedi error checking.

            # uporabnikova zahteva se pošlje Stock Exchange-u
            tran = MessageClientTran(clientID, finID, akcija, kolicina, vrednost)
            message = tran.toJSON()
            print('Sending', message)
            s.sendall(bytes(message,'utf-8'))
            data = s.recv(1024)
            # ToDo: Razvij logiko, ki uposteva serverjev odgovor 
            print('Received', repr(data))