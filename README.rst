Homey_skill
==============

This skill is for controlling Homey with the source voice assistant OVOS.
Keep in mind this is a very early prototype only used to show and test the connections between OVOS and Homey.
Tested connections switching on/off and status request on/off of multiple devices.
Only working with limited set of commands -see uasage-.


CONFIGURATION HOMEY
---------------------------------

Apps
The homey requires multiple apps each with their own configuration. 
    -Install the right app for your devices. How to configure these apps is not part of the description here.
    -Install the MQTT client app. Tested is the "Musqitto MQTT client" from Menno van Grinsven. Set the IP address equal to the homey address and use port 1884. If wanted you can secure the connection with the broker.
    -Install the MQTT broker. Tested is the "MQTT broker" from Menno van Grinsven. Give the port 1884 and enable unsecure connections
    -Install the "MQTT Hub". This is an app to discover all devices and it status and broadcast this information according the homie convention to the MQTT broker. Set Hub "on", publish state by broadcast, protocol "Homie convention v3.0.1". Topic "homie/homey" and Birth and lastwill "on" with standard parameters.
    -Check if devices are found by the "MQTT hub" and broadcast them on the topic.

Devices
    -You can use the Hue app to discover on/off devices. You can also use on/off devices from klikaanklikuit. Others on/off devices should work but they are not tested.
    -Name your devices in Homey uniquely by using the location and description in the device name. : "Kantoor Lamp". OVOS can look in the Homey for the device named by a location and description, in the code called "where" and "what". Devices can also be referenced by "What" alone but Mycroft will only fall back to that if it can't find the device using "Where What" or "What Where".


CONFIGURATION OVOS
-----------------------------------

The solution is tested on the OVOS docker version. Installing OVOS is not part of the description.
After installing OVOS install the path to the github repository and set the configuration of the homey skill.

~/ovos/config/skills/skill-homey.mennebos/settings.json
    "hostname": "192.168.1.192",
    "device": "homie/homey",
    "label1": "null",
    "__mycroft_skill_firstrun": false,
    "password": "",
    "port": "1884",
    "authorization": false,
    "username": "",
    "label2": "null"

~/ovos/config/skills.list
git+https://github.com/MenneBos/skill-homey

USAGE
---------------------------------------

There are only two options available tested on a on/off light. More options possible but the code needs adjustments.

Switch Light named "kantoor lamp"
    -Hey Mycroft zet lamp in kantoor aan    # this will switch the light on with name "kantoor lamp"
    -Hey Mycroft zet lamp uit               # this will switch the light of which has the name "lamp"
Ask Status named "kantoor lamp"
    -Hey Mycroft stand van kantoor lamp     # this will give you the status of the "kantoor lamp"
    -Hey Mycroft stand van lamp             # this will give you the status of the light with "lamp" in tis name

#NOTE on Status request: "Hey Mycroft stand ......", is the only option to request data in Dutch. Using all other options in the vocab file will raise conflicts in OVOS and will not be recognized by OVOS. Using another request words can also lead to errors. This need still to be fixed.
