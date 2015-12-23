# -*- coding: utf-8 -*-
import sys
import os
import xbmc
import xbmcaddon
import xbmcgui
import xml.etree.ElementTree as et
import setalarms
import datetime

addon = xbmcaddon.Addon(id='script.service.PVRReminder')
cwd = addon.getAddonInfo('path').decode("utf-8")
resource = xbmc.translatePath(os.path.join(cwd, 'resources').encode("utf-8")).decode("utf-8")
lib = xbmc.translatePath(os.path.join(resource, 'lib').encode("utf-8")).decode("utf-8")
xmlfile = xbmc.translatePath(os.path.join(resource, 'reminder_data.xml').encode("utf-8")).decode("utf-8")


sys.path.append(resource)
sys.path.append(lib)
alarmclock = setalarms.AlarmClock()

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
           elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


class Reminderstuff:
    """Main alarm clock application class."""

    def __init__(self):
        self.addon = xbmcaddon.Addon()

    def validtime(self, programestarttime):
        """make sure its in the future"""
        now = datetime.datetime.now()
        hr, mins = programestarttime.split(":")
        system_time = xbmc.getInfoLabel('System.Time(hh:mm)')
        hour = system_time.split(':')[0]
        minute = system_time.split(':')[1]

        system_time = now.replace(hour=int(hour), minute=int(minute), second=1, microsecond=0)
        starttime = now.replace(hour=int(hr), minute=int(mins), second=1, microsecond=0)
        return system_time < starttime

    def setalert(self, alerttitle, line1txt, line2txt):
        xbmcgui.Dialog().ok(alerttitle, line1txt, line2txt)

    def invalidtime(self, new_programmetime):
        Reminderstuff.setalert(self, "Cant set time!", "A reminder can not be set for a time in the past", "")
        xbmc.log("PVRReminder: Valid program time:" + str
        (Reminderstuff.validtime(self, new_programmetime)), xbmc.LOGDEBUG)

    def setreminder(self, new_programmename, new_programmetime, new_programmedate, new_channelname):

        titletxt = "Reminder: " + str(new_programmename)
        line1txt = "A reminder has been set for: " + str(new_programmename)
        line2txt = "that starts at: " + str(new_programmetime) + " on " + str(new_programmedate)

        if Reminderstuff.validtime(self, new_programmetime):

            xbmc.log("PVRReminder: setting reminder [from context menu], valid program time:" + str \
            (Reminderstuff.validtime(self, new_programmetime)), xbmc.LOGDEBUG)
            data = et.Element("data")
            reminder = et.SubElement(data, "reminder")
            reminder.set("id", "0")
            enabled = et.SubElement(reminder, "enabled")
            enabled.text = "true"
            programmename = et.SubElement(reminder, "programmename")
            programmename.text = new_programmename
            starttime = et.SubElement(reminder, "starttime")
            starttime.text = new_programmetime
            sdate = et.SubElement(reminder, "sdate")
            sdate.text = new_programmedate
            channel = et.SubElement(reminder, "channel")
            channel.text = new_channelname
            indent(data, level=0)
            tree = et.ElementTree(data)
            tree.write(xmlfile, xml_declaration=True, encoding='utf-8', method="xml")
            Reminderstuff.setalert(self, titletxt, line1txt, line2txt)
            context_enabled = 'true'
            xbmc.log("PVRReminder: Contextmenu selection.", xbmc.LOGDEBUG)
            setalarms.AlarmClockMonitor(alarmclock, context_enabled, new_programmename, new_programmetime, new_programmedate, new_channelname)
        else:
            Reminderstuff.invalidtime(self, new_programmetime)
