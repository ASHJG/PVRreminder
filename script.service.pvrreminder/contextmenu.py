# -*- coding: utf-8 -*-
#import sys
#import os
import xbmc
#import xbmcaddon
#import xml.etree.ElementTree as ET
import reminders 

#addon = xbmcaddon.Addon(id='script.service.PVRReminder')
#cwd = addon.getAddonInfo('path').decode("utf-8")
#resource = xbmc.translatePath(os.path.join(cwd, 'resources').encode("utf-8")).decode("utf-8")
#lib = xbmc.translatePath(os.path.join(resource, 'lib').encode("utf-8")).decode("utf-8")
#data = xbmc.translatePath(os.path.join(resource, 'reminder_data.xml').encode("utf-8")).decode("utf-8")


#sys.path.append(resource)
#sys.path.append(lib)

#tree = ET.parse(data)
#root = tree.getroot()

#from cronjobs import CronTab, Job
#from datetime import datetime

videostarttime = xbmc.getInfoLabel("ListItem.StartTime")
#videoStartTime = "15:30"
videoname = xbmc.getInfoLabel("ListItem.Title")
videodate = xbmc.getInfoLabel("ListItem.StartDate")



setreminderdata = reminders.Reminderstuff()
setreminderdata.setreminder(videoname, videostarttime, videodate)

#setreminderdate.setreminder(videoName, videoStartTime, VideoDate)
#setreminderalert = Reminderstuff.setalert(videoName, videoStartTime, VideoDate)


#alarmClock = setalarms.AlarmClock()
#monitor = setalarms.AlarmClockMonitor(alarmClock)

#xbmc.log("PVR: Starting alarm clock.. from conextmenu", xbmc.LOGDEBUG)
#alarmClock.start()


