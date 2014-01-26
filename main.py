
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



import pymongo
import bottle
import cgi
import re
import mepsDAO

# Displays a particular mep
@bottle.get("/meps/id")
def get_mep(id):

    mep = meps.get_meps(id)

    # return bottle.template("single_mep", dict(mep=mep))


@bottle.get("/meps")
def list_meps():

    meps_list = meps.list()
    return bottle.template('meps', dict(meps=meps_list))

connection_string = "mongodb://localhost"
connection = pymongo.MongoClient(connection_string)
database = connection.blog

meps = mepsDAO.mepsDAO(database)


bottle.debug(True)
bottle.run(host='localhost', port=8082)         # Start the webserver running and wait for requests

