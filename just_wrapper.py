
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
import pymongo

errors = 0

class Just(object):

    name = "cs"
    allowed_domains = ["scj.ro"]
    start_urls = ["http://www.scj.ro/dosare.asp?"]
    connection = None
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

    def browse_records(self, full_name):

        array_dosar = self.client.service.CautareDosare(numeParte = full_name)
        records = []
        i = 0

        self.write_to_file('test2', array_dosar)
        if array_dosar == None:
            return []
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
                dp_entry = {}
                dp_entry[self.normalize(rol_text).replace('.','-')] = self.normalize(name_text)

                #dp_entry = (self.normalize(rol_text), self.normalize(name_text))
                record['parti'].append(dp_entry)
            found = False
            for parte in record['parti']:
                p = parte[parte.keys()[0]]
                if p.lower() == full_name.lower():
                    if parte.keys()[0].lower().find('inculpat') > -1  or  parte.keys()[0].lower().find('acuzat') > -1 :
                        found = True
                        break
            if found:
                records.append(record)

        return records

    def write_to_file(self, file, text):

        file = './logs/' + file
        with open(file,'a+') as f:
          #  text2 = text.encode('utf8')
            f.write(str(text))

    def save_info(self, info):
     mep_db = self.get_db("meps")
     mep_db.cases.insert(info)

    def save_info_in_mep(self, mep_name, info):
        mep_db = self.get_db("meps")
        mep = mep_db.meps.find_one({'Name.full':mep_name})
        #print post
 #       print info
        mep["cases"] = []
        mep["cases"] = info
        #print post
#        print mep
        mep_db.meps.update({'Name.full':mep_name}, mep, upsert = False)

    def get_db(self, db):
        if self.connection is None:
             connection_string = "mongodb://ubuntuaa.cloudapp.net"
             self.connection = pymongo.MongoClient(connection_string)
        return self.connection[db]

    def get_meps(self):
        mep_db = self.get_db("meps")
        meps = mep_db.meps.find({}, {"_id":1, "Name.full" :1})
        return meps

if __name__ == "__main__":
    url = 'http://portalquery.just.ro/query.asmx?WSDL'
    just = Just(url)
    name = 'george becali'
    meps = just.get_meps()

    for mep in meps:
        #print mep
        info = just.browse_records(mep["Name"]["full"])
        just.save_info_in_mep(mep["Name"]["full"], info)
    meps2 = just.get_meps()

    for mep in meps:
        print mep
        just.write_to_file(mep.Name.full, mep)
