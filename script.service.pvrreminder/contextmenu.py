# -*- coding: utf-8 -*-
#import sys
#import os
import xbmc
#import xbmcaddon
#import xml.etree.ElementTree as ET
import reminders
import setalarms

#addon = xbmcaddon.Addon(id='script.service.PVRReminder')
#cwd = addon.getAddonInfo('path').decode("utf-8")
#resource = xbmc.translatePath(os.path.join(cwd, 'resources').encode("utf-8")).decode("utf-8")
#lib = xbmc.translatePath(os.path.join(resource, 'lib').encode("utf-8")).decode("utf-8")
#data = xbmc.translatePath(os.path.join(resource, 'reminder_data.xml').encode("utf-8")).decode("utf-8")
#alarmclock = setalarms.AlarmClock()

#sys.path.append(resource)
#sys.path.append(lib)

#tree = ET.parse(data)
#root = tree.getroot()

#from cronjobs import CronTab, Job
#from datetime import datetime

videostarttime = xbmc.getInfoLabel("ListItem.StartTime")
#videostarttime = "23:55"
videoname = xbmc.getInfoLabel("ListItem.Title")
videodate = xbmc.getInfoLabel("ListItem.StartDate")



setreminderdata = reminders.Reminderstuff()
setreminderdata.setreminder(videoname, videostarttime, videodate)



