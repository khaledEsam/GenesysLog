'''
Created on Sep 5, 2018

@author: Moatasim Magdy
'''

import datetime

class Call:
    call_id = ''
    phone = ''
    signal = []
    startDate = datetime.datetime
    endDate = datetime.datetime
    duration = datetime.datetime

    def __init__(self, call_id, phone, signal, startDate, endDate, duration):
        self.call_id = call_id
        self.phone = phone
        self.signal = signal
        self.startDate = startDate
        self.endDate = endDate
        self.duration = duration

    def full_call(self):
        return '{} {} {} {} {} {}'.format(self.call_id, self.phone, self.signal, self.startDate, self.endDate, self.duration)

    def signal_string(self):
        full_signal = ''
        count = 0
        for i in self.signal:
            count += 1
            if count == self.signal.__len__():
                full_signal += i
                break

            full_signal += i + ' -> '

        return full_signal
    
    


