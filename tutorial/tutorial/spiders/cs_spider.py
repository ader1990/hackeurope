# -*- coding: utf-8 -*-

from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.http import FormRequest
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from tutorial.items import JusticeCaseItem
import pymongo

class CsSpider(BaseSpider):
    log_file = "C:\Users\\adrian\desktop\logger.txt";
    name = "cs"
    allowed_domains = ["scj.ro"]
    start_urls = ["http://www.scj.ro/dosare.asp?"]
    connection = None
    
    def parse(self, response):
        full_names = []
        for mep in self.get_meps():
            full_name = mep["Name"]["full"]
            full_name_stripped = ""
            mapping = {
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
            name_changed = False
            for c in full_name:
                ordinal = ord(c)
                if ordinal > 0 and ordinal < 127:                    
                    full_name_stripped = full_name_stripped + c
                else:
                    if ordinal in mapping.keys():
                        name_changed = True
                        full_name_stripped = full_name_stripped + mapping[ordinal]  
            if name_changed:
                yield FormRequest.from_response(response,
                                        formname='caut_dosar',
                                        formdata={'caut_numar': '',
                                                  'caut_obiect': '',
                                                  'caut_nume': full_name_stripped,
                                                  'caut_sectie': '',
                                                  'view': 'cauta_dosar'},
                                        callback=lambda x : self.afterParse(x))
            else:
                yield FormRequest.from_response(response,
                                        formname='caut_dosar',
                                        formdata={'caut_numar': '',
                                                  'caut_obiect': '',
                                                  'caut_nume': full_name,
                                                  'caut_sectie': '',
                                                  'view': 'cauta_dosar'},
                                        callback=lambda x : self.afterParse(x))

            
    
    def afterParse(self, response):
        mep_name = ""
        td_mapping = {
              1 : "Number",
              2 : "Date",
              3 : "Object",
              4 : "Stage",
              5 : "Section",
              6 : "Implied",
              7 : "Link"
        }
        cases = {
            "MepId" : mep_name,
            "MepName" : mep_name,
            "Number" : "",
            "Date" : "",
            "Object" : "",
            "Stage" : "",
            "Section" : "",
            "Implied" : "",
            "Link" : ""
        }
        sel = Selector(response)
        table = sel.xpath("//*[@cellspacing=1]/tr")
        for index, tr in enumerate(table):
            if index != 0 and index != len(table) - 1:
                tds = tr.xpath("td")
                for index, td in enumerate(tds):
                  if index > 0: 
                      full_mapping = td_mapping[index]
                      if index == 1:          
                          mapping = td_mapping[7]     
                          cases[mapping] = td.xpath("a/@href").extract()
                          cases[full_mapping] = td.xpath("a/text()").extract()
                      else:
                          cases[full_mapping] = td.xpath("text()").extract()
        if cases["Number"] is not "":
            self.save_info(cases)


    def save_info(self, info):
         mep_db = self.get_db("meps")
         mep_db.cases.insert(info)
    
    def get_db(self, db):        
        if self.connection is None:
             connection_string = "mongodb://localhost"
             self.connection = pymongo.MongoClient(connection_string)
        return self.connection[db]

    def get_meps(self):
        mep_db = self.get_db("meps")
        meps = mep_db.meps.find({}, {"_id":1, "Name.full" :1})
        return meps


