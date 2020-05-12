from scapy.all import *
import psycopg2
from threading import Thread


def close_db():
    global conn
    global cursor
    cursor.close()
    conn.close()


def connect_db():
    global conn
    global cursor
    conn = psycopg2.connect(dbname='tftyiqbk', user='tftyiqbk', password='ioia30LFy_tPe-xsKDEfSalK-jlBC7j_',host='kandula.db.elephantsql.com')
    cursor = conn.cursor()


def http_header(packet):
    http_packet=str(packet)
    if http_packet.find('POST /result HTTP/1.1 \n Host: segevharpaz1.pythonanywhere.com') and http_packet.find('name') and http_packet.find('PP')and http_packet.find('id') :
            return GET_print(packet)


def GET_print(packet1):
    global conn
    global cursor
    ret = "\n".join(packet1.sprintf("{Raw:%Raw.load%}\n").split(r"\r\n"))
    stack = ret.split('\n')
    try:
        checker = False
        data = stack[15].split('&')
        data = data[0].split('=')
        connect_db()
        table_data = get_data()
        print(data[1])
        print(table_data)
        for row in table_data:
            if(row[0] == data[1]):
                print(packet1[0][Ether].dst)
                cursor.execute(('UPDATE project_database SET mac = %s WHERE name = %s'), (packet1[0][Ether].dst, row[0]))
                conn.commit()
                close_db()
        return True
    except:
        print('ffuck')


def get_data():
    global cursor
    cursor.execute("SELECT * FROM project_database")
    return cursor.fetchall()


def sniff1():
    global cursor
    global conn
    while True:
        connect_db()
        table_data = get_data()
        packets = sniff(count=1, filter='udp and (port 67 or 68) and ether src b8:27:eb:8a:0a:c9', iface='wlan0')
        for row in table_data:
            if row[3] == packets[0][Ether].dst:
                data_times = str(row[7])
                data_times = data_times.split(',')
                date = datetime.now()
                day = date.strftime("%A")
                time = str(int(date.strftime("%H%M")) + 300)
                checker = False
                late = False
                for i in range(0, len(data_times), 3):
                    if day.lower() == data_times[i + 2] and int(data_times[i]) - 500 < int(time) and data_times[i + 1] > time:
                        checker = True
                        if data_times[i] < time and data_times[i + 1] > time:
                            late = True
                            break
                        else:
                            break
                cursor.execute('UPDATE project_the_one SET connected_wifi = True, connected_time = %s, on_time = %s WHERE %s' ,(packets[0][Ether].dst, checker, late))
        close_db()


def sniff2():
    while True:
        print(1)
        sniff(count=1, lfilter=http_header, filter="tcp port 80", iface="wlan0")


def main():
    t = Thread(target = sniff1)
    t.start()
    s = Thread(target = sniff2)
    s.start()
            

if __name__ == '__main__':
    main()
