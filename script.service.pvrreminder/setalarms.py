# # -*- coding: utf-8 -*-
import sys
import os
import xbmc
import xbmcaddon
import xbmcgui
import xml.etree.ElementTree as ET
import datetime

addon = xbmcaddon.Addon(id='script.service.PVRReminder')
cwd = addon.getAddonInfo('path').decode("utf-8")
resource = xbmc.translatePath(os.path.join(cwd, 'resources').encode("utf-8")).decode("utf-8")
lib = xbmc.translatePath(os.path.join(resource, 'lib').encode("utf-8")).decode("utf-8")
data = xbmc.translatePath(os.path.join(resource, 'reminder_data.xml').encode("utf-8")).decode("utf-8")

sys.path.append(resource)
sys.path.append(lib)

trees = ET.parse(data)
roots = trees.getroot()

from cronjobs import CronTab, Job

# from datetime import datetime

def remindme():
    alerttitle = "Reminder "
    line1 = "A program that was added to the reminder is about to start."
    xbmcgui.Dialog().ok(alerttitle, line1)

class AlarmClock:
    """Main alarm clock application class."""
    #
    def __init__(self):
        self.addon = xbmcaddon.Addon()
        self.crontab = CronTab(xbmc)

    def validtime(self, programestarttime):
        """make sure its in the future, if Start time is in the future then set to true"""
        now = datetime.datetime.now()
        hr, mins = programestarttime.split(":")
        starttime = now.replace(hour=int(hr), minute=int(mins), second=1, microsecond=0)
        return starttime > now


    def applysettings(self, contextenabled, new_programmename, new_programmetime, new_programmedate):
        """Gets the current configuration and updates the scheduler."""
        xbmc.log("PVRReminder: Getting settings", xbmc.LOGDEBUG)
        self.addon = xbmcaddon.Addon()
        self.crontab.jobs = self._getalarms(contextenabled, new_programmename, new_programmetime, new_programmedate)
        # xbmc.log("PVRReminder: Job:" + str(self), xbmc.LOGDEBUG)
        self.crontab.start()

    def start(self):
        """Starts the alarm clock, ie. activates the defined alarms."""
        xbmc.log("PVRReminder: Starting current alarm...", xbmc.LOGDEBUG)
        self.crontab.start()

    def stop(self):
        """Stops the alarm clock."""
        xbmc.log("PVRReminder: Stopping current alarm...", xbmc.LOGDEBUG)
        self.crontab.stop()

    def _getalarms(self, contextenabled, new_programmename, new_programmetime, new_programmedate):
        """Get a list of the cron jobs for the enabled alarms."""
        jobs = []
        if contextenabled == "true":
            jobs.extend(self._getjobs(1, contextenabled,  new_programmename, new_programmetime, new_programmedate))
            return jobs
        else:
            for reminder in roots.findall('reminder'):
                enabled = reminder.find('enabled').text
                xbmc.log("PVRReminder: alarm is: %s" % str(enabled), xbmc.LOGDEBUG)
            if enabled == "true":
                jobs.extend(self._getjobs(1, contextenabled, new_programmename, new_programmetime, new_programmedate))
                return jobs
            else:
                xbmc.log("PVRReminder: Going to have to stop alarm as there is nothing to remind", xbmc.LOGDEBUG)
                AlarmClock.stop(self)

    def _getjobs(self, number, contextenabled,  new_programmename, new_programmetime, new_programmedate):

        if contextenabled == "true":
            starttime = new_programmetime
            programmename = new_programmename
#           programmedate = new_programmedate
            xbmc.log("PVRReminder: Getting info from user input from EPG", xbmc.LOGDEBUG)
        else:
            for reminder in roots.findall('reminder'):
                starttime = reminder.find('starttime').text
                programmename = reminder.find('programmename').text
#               programmedate = reminder.find('sdate').text
                xbmc.log("PVRReminder: Getting info from file", xbmc.LOGDEBUG)
                """If start time is in the future (true) then set times"""
        if AlarmClock.validtime(self, starttime):
            hr, mins = starttime.split(":")
            filetoplay = programmename
            jobs = [Job(self._play, int(mins), int(hr), args=[filetoplay, 30])]
            xbmc.log("PVRReminder: Time is valid, setting jobs: %s" % str(jobs), xbmc.LOGDEBUG)
            return jobs
        else:
            xbmc.log("PVRReminder: Setting old reminder to false as its in the past ", xbmc.LOGDEBUG)
            for enabled in roots.iter('enabled'):
                enabled.text = "false"
                trees.write(data)
            xbmc.log("PVRReminder: Stopping Alarm because enabled reminder is in the past", xbmc.LOGDEBUG)
            AlarmClock.stop(self)
            jobs = []
            return jobs



    def _play(self, item, volume):

        remindme()

        for enabled in roots.iter('enabled'):
            enabled.text = "false"
            trees.write(data)
            xbmc.log("PVRReminder: Reminder sent, going set enabled to:" + str(enabled), xbmc.LOGDEBUG)
            self.crontab.stop()


class AlarmClockMonitor(xbmc.Monitor):
    """Monitor subclass listening on configuration changes and termination requests."""

    def __init__(self, alarmclock, contextenabled, new_programmename, new_programmetime, new_programmedate):
        xbmc.Monitor.__init__(self)
        xbmc.log("PVRReminder: Starting AlarmClockMonitor", xbmc.LOGDEBUG)
        self.alarmClock = alarmclock
        self.alarmClock.applysettings(contextenabled, new_programmename, new_programmetime, new_programmedate)

    def onSettingsChanged(self):
        self.alarmClock.applysettings()

    def onAbortRequested(self):
        self.alarmClock.stop()


contextenabled = "false"
new_programmename = "false"
new_programmetime = "false"
new_programmedate = "false"
alarmClock = AlarmClock()
monitor = AlarmClockMonitor(alarmClock, contextenabled, new_programmename, new_programmetime, new_programmedate)

#xbmc.log("PVRReminder: Start Up: Starting alarm clock..", xbmc.LOGDEBUG)
#alarmClock.start()
