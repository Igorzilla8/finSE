################################################################################
#
# File:         messageClientTran.py
# Description:  Razred MessageStockValue je namenjen posiljanju vrednosti
#               fin. instrumentov med Stock Providerjem in Stock Exchangeom.
#               Message vsebuje:
#               clientID - ID klienta
#               tranTyp - tip transakcije
#               value - vrednosti fin. instrumentov
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

class MessageStockValue:
    def __init__(self, stockID, msgTyp, stockValue):
        self.stockID = stockID
        self.msgTyp = msgTyp
        self.stockVal = stockValue
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)