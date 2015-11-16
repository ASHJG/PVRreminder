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
        xbmc.log("PVRReminder: Getting settings, contextenabled:"+str(contextenabled), xbmc.LOGDEBUG)
        self.addon = xbmcaddon.Addon()
        self.crontab.jobs = self._getalarms(contextenabled, new_programmename, new_programmetime, new_programmedate)
        self.stop()
        self.crontab.switch()
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
            xbmc.log("PVRReminder: setting New alarm from user input: %s" % str(new_programmename), xbmc.LOGDEBUG)
            return jobs
        else:
            for reminder in roots.findall('reminder'):
                enabled = reminder.find('enabled').text
                if enabled == "true":
                    ReminderID = reminder.get('id')
                    new_programmetime = reminder.find('starttime').text
                    new_programmename = reminder.find('programmename').text
                    jobs.extend(self._getjobs(ReminderID, contextenabled, new_programmename, new_programmetime, new_programmedate))
                    xbmc.log("PVRReminder: setting old alarm from file", xbmc.LOGDEBUG)
                else:
                    xbmc.log("PVRReminder: Going to have to stop alarm as there is nothing to remind", xbmc.LOGDEBUG)
                    AlarmClock.stop(self)
            return jobs

    def _getjobs(self, ReminderID, contextenabled,  new_programmename, new_programmetime, new_programmedate):

        xbmc.log("PVRReminder: Getting info from file, programme Name: " + str(new_programmename), xbmc.LOGDEBUG)

        if AlarmClock.validtime(self, new_programmetime):
            hr, mins = new_programmetime.split(":")
            filetoplay = new_programmename
            jobs = [Job(self._play, int(mins), int(hr), args=[filetoplay, ReminderID])]
            xbmc.log("PVRReminder: Time is valid, setting jobs: %s" % str(jobs), xbmc.LOGDEBUG)

        else:
            xbmc.log("PVRReminder: Setting old reminder to false as its in the past ", xbmc.LOGDEBUG)
            for reminder in roots.findall('reminder'):
                ID = int(reminder.get('id'))
                if ID == int(ReminderID):
                    for enabled in roots.iter('enabled'):
                        enabled.text = "false"
                        trees.write(data)

                    #roots.remove(reminder)
                    #trees.write(data)
            xbmc.log("PVRReminder: Reminder set in the past, going to purge reminder", xbmc.LOGDEBUG)

            jobs = []
        return jobs

    def _play(self, item, ReminderID):

        remindme()
        for reminder in roots.findall('reminder'):
            ID = int(reminder.get('id'))
            if ID == int(ReminderID):
                for enabled in roots.iter('enabled'):
                    enabled.text = "false"
                    trees.write(data)
                #roots.remove(reminder)
                #trees.write(data)
        xbmc.log("PVRReminder: Reminder sent, going to purge reminder", xbmc.LOGDEBUG)


class AlarmClockMonitor(xbmc.Monitor):
    """Monitor subclass listening on configuration changes and termination requests."""

    def __init__(self, alarmclock, contextenabled, new_programmename, new_programmetime, new_programmedate):
        xbmc.Monitor.__init__(self)
        xbmc.log("PVRReminder: Starting AlarmClockMonitor"+ str(contextenabled), xbmc.LOGDEBUG)
        self.alarmClock = alarmclock
        self.alarmClock.applysettings(contextenabled, new_programmename, new_programmetime, new_programmedate)

    def onSettingsChanged(self):
        self.alarmClock.applysettings()

    def onAbortRequested(self):
        self.alarmClock.stop()

if __name__ == '__main__':

    contextenabled = "false"
    new_programmename = "false"
    new_programmetime = "false"
    new_programmedate = "false"
    alarmClock = AlarmClock()
    monitor = AlarmClockMonitor(alarmClock, contextenabled, new_programmename, new_programmetime, new_programmedate)

#xbmc.log("PVRReminder: Start Up: Starting alarm clock..", xbmc.LOGDEBUG)
#alarmClock.start()
