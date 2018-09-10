'''
Created on Sep 6, 2018

@author: Moatasim Magdy
'''
import datetime

def get_mytime(startDate, endDate):
    startDate = startDate.split(' ')
    startdates = startDate[0].split('-')
    startyear = int(startdates[0])
    startmonth = int(startdates[1])
    startday = int(startdates[2])
    starthours = startDate[1].split(':')
    starthour = int(starthours[0])
    startminute = int(starthours[1])
    startseconds = starthours[2].split('.')
    startsecond = int(startseconds[0])
    startmillisecond = int(startseconds[1])

    endDate = endDate.split(' ')
    enddates = endDate[0].split('-')
    endyear = int(enddates[0])
    endmonth = int(enddates[1])
    endday = int(enddates[2])
    endhours = endDate[1].split(':')
    endhour = int(endhours[0])
    endminute = int(endhours[1])
    endseconds = endhours[2].split('.')
    endsecond = int(endseconds[0])
    endmillisecond = int(endseconds[1])

    start = datetime.datetime(startyear, startmonth, startday, starthour, startminute, startsecond, startmillisecond)
    end = datetime.datetime(endyear, endmonth, endday, endhour, endminute, endsecond, endmillisecond)

    duration = end - start

    return duration