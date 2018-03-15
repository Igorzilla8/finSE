################################################################################
#
# File:         messageClientTran.py
# Description:  Razred MessageClientTran je namenjen posiljanju uporabnikove
#               zahteve (buy, sell, limit buy, limit sell) na Stock Exchange.
#               Message vsebuje:
#               clientID - ID uporabnika 
#               finID - ID fin. instrumenta
#               akcija - uporabnikovo narocilo (buy, sell, limit buy, limit sell)
#               kolicina - kolicina fin. instrumenta, ki ga uporabnik kupuje/prodaja
#               vrednost - vrednost pri kateri se sprozi limitirani buy/sell
# Author:       Igor Rozman
# Created:      
# Modified:     
#               
# Language:     PYTHON (v 3.6.4)
#               
# Package:      
#
################################################################################
import json


class MessageClientTran:
    def __init__(self, clientID, finID, akcija, kolicina, vrednost):
        self.clientID = clientID
        self.finID = finID
        self.akcija = akcija
        self.kolicina = kolicina
        self.vrednost = vrednost
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)