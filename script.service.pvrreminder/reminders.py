# -*- coding: utf-8 -*-
import sys
import os
import xbmc
import xbmcaddon
import xbmcgui
import xml.etree.ElementTree as ET
import setalarms
import datetime

addon = xbmcaddon.Addon(id='script.service.PVRReminder')
cwd = addon.getAddonInfo('path').decode("utf-8")
resource = xbmc.translatePath(os.path.join(cwd, 'resources').encode("utf-8")).decode("utf-8")
lib = xbmc.translatePath(os.path.join(resource, 'lib').encode("utf-8")).decode("utf-8")
data = xbmc.translatePath(os.path.join(resource, 'reminder_data.xml').encode("utf-8")).decode("utf-8")

sys.path.append(resource)
sys.path.append(lib)

tree = ET.parse(data)
root = tree.getroot()
alarmclock = setalarms.AlarmClock()


class Reminderstuff:
    """Main alarm clock application class."""

    def __init__(self):
        self.addon = xbmcaddon.Addon()

    def validtime(self, programestarttime):
        """make sure its in the future"""
        now = datetime.datetime.now()
        hr, mins = programestarttime.split(":")
        starttime = now.replace(hour=int(hr), minute=int(mins), second=1, microsecond=0)
        return now < starttime

    def setalert(self, alerttitle, line1txt, line2txt):
        xbmcgui.Dialog().ok(alerttitle, line1txt, line2txt)

    def invalidtime(self, new_programmetime):
        Reminderstuff.setalert(self, "Cant set time!", "A reminder can not be set for a time in the past", "")
        xbmc.log("PVRReminder: Valid program time:" + str
        (alarmclock.validtime(new_programmetime)), xbmc.LOGDEBUG)

    def setreminder(self, new_programmename, new_programmetime, new_programmedate):

        titletxt = "Reminder:" + str(new_programmename)
        line1txt = "A reminder has been set for :" + str(new_programmename)
        line2txt = "at :" + str(new_programmetime) + " on " + str(new_programmedate)

        if alarmclock.validtime(new_programmetime):
            xbmc.log("PVRReminder: setting reminder [from context menu], valid program time:" + str \
            (alarmclock.validtime(new_programmetime)), xbmc.LOGDEBUG)

            for programmename in root.iter('programmename'):
                programmename.text = str(new_programmename)
                tree.write(data)
            for starttime in root.iter('starttime'):
                starttime.text = str(new_programmetime)
                tree.write(data)
            for sdate in root.iter('sdate'):
                sdate.text = str(new_programmedate)
                tree.write(data)
            for enabled in root.iter('enabled'):
                enabled.text = 'true'
                enabled = 'true'
                tree.write(data)
            Reminderstuff.setalert(self, titletxt, line1txt, line2txt)

            #setalarms.AlarmClock.stop(alarmclock)
            setalarms.AlarmClockMonitor(alarmclock, enabled, new_programmename, new_programmetime, new_programmedate)
            setalarms.AlarmClock.start(alarmclock)
        else:
            Reminderstuff.invalidtime(self, new_programmetime)
