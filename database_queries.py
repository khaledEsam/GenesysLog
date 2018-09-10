'''
Created on Sep 5, 2018

@author: Moatasim Magdy
'''

import cx_Oracle
from Genesys import duration_count


def start_connection():
    con = cx_Oracle.connect('Genesys','1234')
    return con

def search_database(con, my_value):
    cur = con.cursor()
    cur.execute("select * from call where call_id = '"+my_value+"'")
    row_count = cur.fetchone()
    con.commit()

    if row_count == None:
        return 0
    else:
        return 1
    
def update_object_end_date(con, my_object ):
    cur = con.cursor()
    statement = "UPDATE call SET end_date = :v WHERE call_id = :n"
    cur.execute(statement, {'v': my_object.endDate, 'n': my_object.call_id})
    con.commit()

def update_object_start_date(con, my_object ):
    cur = con.cursor()
    cur.execute("select start_date from call where call_id = '"+my_object.call_id+"'")
    x= cur.fetchone()
    con.commit()
    x = str(x)[2:-3]
    if x == '0':
        # print('OK')
        statement = "UPDATE call SET start_date = :v WHERE call_id = :n"
        cur.execute(statement, {'v': my_object.startDate, 'n': my_object.call_id})
        con.commit()
    
    
def update_object_duration(con, my_object ):
    
    cur = con.cursor()
    cur.execute("select duration from call where call_id = '"+my_object.call_id+"'")
    x= cur.fetchone()
    con.commit()
    x = str(x)[2:-3]
    if x == '0':
        cur.execute("select start_date from call where call_id = '"+my_object.call_id+"'")
        y= cur.fetchone()
        y = str(y)[2:-3]
        if y == '0':
            return
        else:
            cur.execute("select end_date from call where call_id = '"+my_object.call_id+"'")
            z= cur.fetchone()
            z = str(z)[2:-3]
            if z == '0':
                return
            else:
                duration = duration_count.get_mytime(y, z)
                duration = str(duration)
                
                statement = "UPDATE call SET duration = :v WHERE call_id = :n"                  
                cur.execute(statement, {'v': duration, 'n': my_object.call_id})
                con.commit()
                 
    else:
        return
            
        

def update_object_signal(con, my_object ):
    cur = con.cursor()
    cur.execute("select signal from call where call_id = '"+my_object.call_id+"'")
    x= cur.fetchone()
    con.commit()

    if x == (None,):
        cur = con.cursor()
        statement = "UPDATE call SET signal = :v WHERE call_id = :n"
        cur.execute(statement, {'v': my_object.signal_string(), 'n': my_object.call_id})
        con.commit()
    else:
        my_signal = my_object.signal_string()
        y = str(x)[2:-3] + ' -> ' + str(my_signal)
        cur = con.cursor()
        statement = "UPDATE call SET signal = :v WHERE call_id = :n"
        cur.execute(statement, {'v': y, 'n': my_object.call_id})
        con.commit()
    
    

def end_connection(con):
    con.close()


def insert_object(con, my_object):
    cur = con.cursor()
    insert_statment =  "insert into call values ( :1, :2, :3, :4, :5, :6 )"
    cur.execute(insert_statment, {'1' : my_object.call_id, '2' : my_object.phone, '3' : my_object.signal_string(), '4' : str(my_object.startDate), '5' :  str(my_object.endDate), '6' : str(my_object.duration) })
    con.commit()

