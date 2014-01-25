
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys
sys.path.append('../')
import xmltodict, json
import logging
import traceback as tb
import suds.metrics as metrics
from suds import WebFault
from suds.client import Client

errors = 0

class Just(object):

    def __init__(self, url):
        self.client = Client(url)

    def normalize(self, text):
        text_clean = ""
        mapping = {
            226: "a",
            351: "s",
            258: "A",
            259: "a",
            211 : "O",
            194: "A",
            350: "S",
            354: "T",
            225: "a",
            243: "o",
            201: "E",
            225: "a",
            336: "O"
        }
        for c in text:
            ordinal = ord(c)
            if ordinal > 0 and ordinal < 127:
                text_clean = text_clean + c
            else:
                if ordinal in mapping.keys():
                    text_clean = text_clean + mapping[ordinal]
        return text_clean

    def browse_files(self, name):

        array_dosar = self.client.service.CautareDosare(numeParte = name)
        records = []
        i = 0

        self.write_to_file('test2', array_dosar)

        for dosar in array_dosar[0]:
            i += 1
            record = { 'numar' : str(dosar.numar),
                        'obiect' : self.normalize(dosar.obiect),
                        'data' : str(dosar.data),
                        'parti': []}


            dosare_parte = dosar[0][0]
            for dp in dosare_parte:
                (name, rol) = dp
                (name_annotation, name_text) = name
                (rol_annotation, rol_text) = rol
              #  write_to_file('test' + str(dosar.numar).replace('/','-'), name_annotation)
                dp_entry = (self.normalize(rol_text), self.normalize(name_text))
                record['parti'].append(dp_entry)
            records.append(record)

        return records

    def write_to_file(self, file, text):

        file = './logs/' + file
        with open(file,'a+') as f:
          #  text2 = text.encode('utf8')
            f.write(str(text))

if __name__ == "__main__":
    url = 'http://portalquery.just.ro/query.asmx?WSDL'
    just = Just(url)
    name = 'george becali'
    just.write_to_file('test3', just.browse_files(name))
