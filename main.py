
#
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#


import bson
import pymongo
import bottle
import cgi
import re
import mepsDAO
#import just_wrapper

def get_db(db):
    connection_string = "mongodb://ubuntuaa.cloudapp.net"
    connection = pymongo.MongoClient(connection_string)
    return connection[db]

def get_meps():
    mep_db = get_db("meps")
    meps = mep_db.meps.find({}, {"_id":1, "Name.full" :1, "cases":1, "iccsj":1})
    # for mp in meps:
    #     print mp
    return meps

def get_mep_by_id(id):
    mep_db = get_db("meps")
    mep = mep_db.meps.find_one({'_id':bson.ObjectId(oid=str(id))}, {"_id":1, "Name.full" :1, "cases":1,'iccsj':1})
    return mep

@bottle.route('/')
def main():

   # meps_list = meps.list()
    meps_list = get_meps()
    #for mp in meps_list:
        #print mp
    return bottle.template('meps', dict(meps=meps_list))



# Displays a particular mep
@bottle.get("/mep/<id>")
def get_mep(id):

    mep = get_mep_by_id(id)
    print mep
    return bottle.template("mep", dict(mep=mep))

@bottle.get("/meps")
def list_meps():

    meps_list = meps.list()
    return bottle.template('meps', dict(meps=meps_list))

connection_string = "mongodb://ubuntuaa.cloudapp.net"
connection = pymongo.MongoClient(connection_string)
database = connection.meps

meps = mepsDAO.mepsDAO(database)


bottle.debug(True)
bottle.run(host='localhost', port=8082)         # Start the webserver running and wait for requests

