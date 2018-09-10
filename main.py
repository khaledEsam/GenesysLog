'''
Created on Sep 5, 2018

@author: Moatasim Magdy
'''
import datetime
import xlsxwriter
import cx_Oracle
from Genesys import database_queries
from Genesys import Call
from Genesys import duration_count






def find_call_id(file_name):
    file = open(file_name, "r")
    count = 0
    i = -1
    temps = []
    call_ids = []
    calls = []

    lines = file.readlines()
    for line in lines:
        x = 0
        i += 1
        count += 1
        if line.find('Call-ID') != -1:

            line_indexes = line.split(' ')
            if line_indexes[0].find('Call-ID') != -1:
                block = []
                while True:
                    if x == 2:
                        break
                    block.append(str(x) + ' ' + lines[i + x])
                    x += 1
                if block[1].find('Contact:') != -1:
                    temps.append(block)
                    count += 1

            for temp in temps:
                call = Call.Call('', '', [], 0, 0, 0)
                call.call_id = temp[0]
                call.call_id = call.call_id[11: -1].split('@')
                call.call_id = call.call_id[0]
                if call.call_id in call_ids:
                    continue
                else:
                    if lines[i - 7].startswith('20'):
                        start = lines[i - 7]
                        start = start.split(' ')
                        if start[0].find('T') != -1:
                            start = start[0].split('T')
                            start = start[0]+' '+start[1]

                            call.startDate = start
                        else:
                            start = start[0] + ' ' + start[1]

                            call.startDate = start
                    else:
                        call.startDate = 0
                    call_ids.append(call.call_id)
                    full_contact = temp[1].split('@')
                    call.phone = full_contact[0]
                    call.phone = call.phone[16:]
                    if call.phone.find('GVP') != -1:
                        continue
                    else:
                        call.signal = []
                        call.duration = 0
                        # call.startDate = 0
                        call.endDate = 0
                        calls.append(call)
    
                    

    file.close()
    return calls


def get_signal(calls,file_name):
    file = open(file_name, "r")
    lines = file.readlines()
    x = 0
    i = -1
    temps = []
    count = 0


    for line in lines:
        x = 0
        i += 1
        if line.find('Call-ID') != -1:

            line_indexes = line.split(' ')
            if line_indexes[0].find('Call-ID') != -1:
                block = []
                while True:
                    if x == 11:
                        break
                    block.append(str(x)+' '+lines[i+x])
                    x += 1
                if block[1].find('Contact:') != -1 and block[5].find('Signal') != -1:
                    temps.append(block)
                    count += 1


    for temp in temps:
        call = Call.Call('', '', [], 0, 0, 0)
        call.call_id = temp[0]
        call.call_id = call.call_id[11: -1].split('@')
        call.call_id = call.call_id[0]
        full_contact = temp[1].split('@')
        call.phone = full_contact[0]
        call.phone = call.phone[16:]
        full_signal = temp[5].split('=')
        signal = full_signal[1]
        signal = signal[0:1]
        call.signal.append(signal)
        call.duration = 0
#         my_call_times = temp[10].split(' ')
#         my_call_time = my_call_times[1]
#         if my_call_time.startswith('20', 0):
#             my_call_time = my_call_times[1] + ' ' + my_call_times[2]
#             call.startDate = my_call_time

        for my_call in calls:
            q=0
            if my_call.call_id.find(call.call_id) != -1:
                q = 1
                my_call.signal.append(signal)
#                 if my_call.startDate == 0:
#                     my_call.startDate = call.startDate
                break
            else:
                continue
        if q == 0:
            # print(call.call_id+' '+str(call.startDate))
            calls.append(call)

    return calls


def get_duration(calls, file_name):
    file = open(file_name, "r")
    x = 0
    i = 0
    lines = file.readlines()

    for line in lines:
        x = 0
        # q = 0
        i += 1
        if line.find('CSeq') != -1:
            temp = line.split(' ')
            if temp[2].find('BYE') != -1:
                block = []
                while True:
                    if x == 10:
                        break
                    block.append(str(x) + ' ' + lines[i + x])
                    x += 1
                if block[0].find('Call-ID') != -1:
                    my_call_id = block[0]
                    my_call_id = my_call_id[11: -1].split('@')
                    my_call_id = my_call_id[0]
                    time = block[9].split(' ')
                    # print(my_call_id+' '+str(time[1]))
                    if time[1].startswith('20', 0):
                        if time[1].find('T')!= -1:
                            time = time[1].split('T')
                            time = time[0] + ' ' + time[1]
                        else:
                            time = time[1] + ' ' + time[2]
                        
                        for my_call in calls:
                            q = 0
                            if my_call.call_id.find(my_call_id) != -1:
                                if my_call.endDate == 0:
                                    my_call.endDate = time
                        
                                
                                # print(my_call.call_id+' '+my_call.endDate)
                                q = 1
                                if my_call.startDate != 0:
                                    my_call.duration = duration_count.get_mytime(my_call.startDate, my_call.endDate)
                                break
                            else:
                                continue
                        # print(q)
                        if q == 0:
                            # print(my_call_id+' '+time)
                            call = Call.Call('', '', [], 0, 0, 0)
                            call.call_id = my_call_id
                            call.endDate = time
                            calls.append(call)
                            
                    else:
                        continue
                else:
                    continue
            else:
                continue
        else:
            continue

    return calls






def export_xls_file(calls):
    # https://xlsxwriter.readthedocs.io/
    # Create a workbook and add a worksheet.

    workbook = xlsxwriter.Workbook('Genesyslogfile.xlsx')
    worksheet = workbook.get_worksheet_by_name('Genesys')
    if worksheet is None:
        worksheet = workbook.add_worksheet('Genesys')

    # Start from the first cell. Rows and columns are zero indexed.
    row = 1

    worksheet.write(0, 0, 'Call IDs')
    worksheet.write(0, 1, 'Contact number')
    worksheet.write(0, 2, 'Signal Path')
    worksheet.write(0, 3, 'Start Date')
    worksheet.write(0, 4, 'End  Date')

    # Iterate over the data and write it out row by row.
    for i in (calls):
        worksheet.write(row, 0, i.call_id)
        worksheet.write(row, 1, i.phone)
        worksheet.write(row, 2, i.signal_string())
        worksheet.write(row, 3, i.startDate)
        worksheet.write(row, 4, i.endDate)
        row += 1

    workbook.close()





files = ['MCP/MCP01.20180906_133218_874.log', 'MCP/MCP01.20180906_133550_655.log', 'MCP/MCP01.20180906_133847_432.log',
        'MCP/MCP01.20180906_134114_927.log', 'MCP/MCP01.20180906_134425_564.log', 'MCP/MCP01.20180906_134730_326.log']
con = database_queries.start_connection()       
for file in files:
    all_call_ids = find_call_id(file)
    calls = get_signal(all_call_ids, file)
    temps = get_duration(calls, file)
 
    for temp in temps:
        x = database_queries.search_database(con, temp.call_id)
        if x == 0:
            database_queries.insert_object(con, temp)
        else:
            database_queries.update_object_signal(con, temp)
            database_queries.update_object_end_date(con, temp)
            database_queries.update_object_start_date(con,temp)
            database_queries.update_object_duration(con, temp)
        
    


database_queries.end_connection(con)

 

# signal = ['1','2','3']
# call = Call.Call('008DEFAA-541D-1B6A-82D5-A3E8390AAA77-43333', 'sssss', signal, '2018-07-31 11:53:20.924', '2018-08-31 11:53:20.924', '11:53:20.924')
# database_queries.update_object_start_date(con, call)

# export_xls_file(temps)

