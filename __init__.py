# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.
#from adapt.intent import IntentBuilder
#from mycroft.skills.core import MycroftSkill
#from mycroft.util.log import getLogger
#from os.path import dirname, abspath
#from .Homey import Homey
#import sys
#import re

from ovos_workshop.skills import OVOSSkill
from ovos_utils.intents import IntentBuilder
from ovos_workshop.decorators import intent_handler
from ovos_utils.log import LOG
from os.path import dirname, abspath
from .Homey import Homey
import sys
import re

__author__ = 'R. de Lange'

"""	This Homey skill is partly ported from the Domoticz Skill by treussart
	Please find on https://github.com/treussart/domoticz_skill """

sys.path.append(abspath(dirname(__file__)))
LOGGER = LOG(__name__)


class HomeySkill(OVOSSkill):

    def __init__(self):
        super(HomeySkill, self).__init__(name="HomeySkill")
        self.lang1 = ''

    def initialize(self):
        self.lang1 = self.config_core.get('lang')

        homey_switch_intent = IntentBuilder("SwitchIntent")\
            .require("TurnKeyword")\
            .require("StateKeyword")\
            .require("WhatKeyword")\
            .optionally("WhereKeyword").build()
        self.register_intent(homey_switch_intent,
                             self.handle_homey_switch_intent)

        homey_infos_intent = IntentBuilder("InfosIntent")\
            .require("InfosKeyword")\
            .require("WhatKeyword")\
            .optionally("WhereKeyword")\
            .optionally("StateKeyword").build()
        self.register_intent(homey_infos_intent,
                             self.handle_homey_infos_intent)
        self.homey = Homey(
            self.settings.get("hostname"),
            self.settings.get("port"),
            self.settings.get("device"),
            self.settings.get("authentication"),
            self.settings.get("username"),
            self.settings.get("password"),
            self.lang1)

    def handle_homey_switch_intent(self, message):
        state = message.data.get("StateKeyword")
        what = message.data.get("WhatKeyword")
        where = message.data.get("WhereKeyword")
        action = message.data.get("TurnKeyword")
        if where ==None: where = "all"
        data = {
            'what': what,
            'where': where
        }
        where = where.replace(" ","")
        print("--init-- switch intent", where, what, state, action)
        LOGGER.debug("message : " + str(message.data))
        response = self.homey.switch(state, what, where, action)
        print("--init--", response)
        edng = re.compile(str(state).title(), re.I)
        ending = "ed"
        if edng.search('aan') or edng.search('uit'):
            ending = ""
        data['stateverb'] = str(state).title()+ending
        data['state'] = str(state).title()
        if response == False: self.speak_dialog("NoConnection",data)
        elif response is None:
            self.speak_dialog("NotFound", data)
        elif response is 2:
            self.speak_dialog("AlreadyTarget", data)
        elif response is 1:
            self.speak_dialog("OpsError", data)
        else:
            self.speak_dialog("OpsSuccess", data)

    def handle_homey_infos_intent(self, message):
        what = message.data.get("WhatKeyword")
        info = message.data.get("InfosKeyword")
        if info == None: info = "stand"  # works only with onoff
        data = {
          'what': what,
          'where': info
        }
        where = info.replace(" ","")
        print("--init-- info intent", where, what)
        response = self.homey.get(what, where)
        sentence = ""
        if response == False: self.speak_dialog("NoConnection",data)
        elif len(response) == 0:
            self.speak_dialog("NotFound", data)
        elif len(response) > 0:
            dd = []
            keywords = ""
            for item in response:
                if not re.search(item[0].replace(" ",""),keywords):
                    d = []
                    d.append(data['where'])
                    d.append(data['what'])
                    d.append(item[0])
                    d.append(item[1])
                    d.append(item[2])
                    dd.append(d)
                    keywords = keywords+item[0].replace(" ","")+" "
            count = 1
            for item_d in dd:
                sentencedata = {}
                sentencedata.clear()
                sentencedata['where'] = item_d[0]
                sentencedata['what'] = item_d[1]
                sentencedata['measurement'] = item_d[2]
                sentencedata['value'] = item_d[3]
                sentencedata['unit'] = item_d[4]
                if self.homey.lang == "nl-nl":
                    if sentencedata['measurement'] == "current temperature" : sentencedata['measurement'] = "huidige temperatuur"
                    if sentencedata['measurement'] == "target temperature": sentencedata['measurement'] = "ingestelde temperatuur"
                    if sentencedata['measurement'] == "current humidity": sentencedata['measurement'] = "huidige luchtvochtigheid"

                if count ==1: self.speak_dialog("SensorRead1",sentencedata)
                elif count == len(dd) and len(dd) > 1:
                    self.speak_dialog("SensorRead2",sentencedata)
                elif count != len(dd) and len(dd) > 1:
                    self.speak_dialog("SensorRead3",sentencedata)

                count =count+1
        #LOGGER.debug("result : " + str(sentence))
        #self.speak(str(sentence))

    def stop(self):
        pass


def create_skill():
    return HomeySkill()
