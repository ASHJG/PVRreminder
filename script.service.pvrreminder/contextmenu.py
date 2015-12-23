# -*- coding: utf-8 -*-
import xbmc
import reminders

def cleantime(videostarttime):
    # strip ot PM and add 12hrs
    strtime = videostarttime
    if videostarttime.find("pm") <>-1:
        xbmc.log("PVRReminder: Removing PM and formatting to 24hr : ", xbmc.LOGDEBUG)
        strtime.replace("pm", "")
        hr, mins = strtime.split(":")
        hrs = int(hr)+12
        strtime = str(hrs)+":"+str(mins)

    elif videostarttime.find("am")<>-1:
        xbmc.log("PVRReminder: Removing AM and formatting to 24hr : ", xbmc.LOGDEBUG)
        strtime.replace("am", "")

    return strtime

videostarttime = cleantime(xbmc.getInfoLabel("ListItem.StartTime"))
videoname = xbmc.getInfoLabel("ListItem.Title")
videodate = xbmc.getInfoLabel("ListItem.StartDate")
channelname= xbmc.getInfoLabel("ListItem.ChannelName")
setreminderdata = reminders.Reminderstuff()
setreminderdata.setreminder(videoname, videostarttime, videodate, channelname)
