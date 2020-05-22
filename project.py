from scapy.all import *
import psycopg2
from threading import Thread, Timer
from datetime import timedelta, date


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
        yoel = []
        for i in range(1,6,2):
            yoel.append(data[i])
        days = ''
        for i in range(7,18,2):
            if(data[i] != 'none'):
                days += str(data[i-1])+','+str(data[i]).replace('%3A', '').replace('-',',')
        yoel.append(days)
        connect_db()
        table_data = get_data()
        checker = True
        for row in table_data:
            if(row[0] == yoel[0]):
                checker = False
        if checker:
            sql = "INSERT INTO project_database (name, password, id, mac, connected_signin, " \
                  "connected_wifi, connected_time, times, on_time) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (data[0], data[1], data[2], packet1[0][Ether].dst, True, True, True, data[3], True)
            cursor.execute(sql, val)
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


def dudu(q):
    if not q:
        return create_q()
    global cursor
    connect_db()
    cursor.execute('UPDATE project_database SET connected_wifi=%s, connected_signin = %s, connected_time = %s',
                   (False, False, False))
    data = q.pop(0)
    Timer(data, dudu, args=q).start()


def arrive_late(q):
    if not q:
        return create_q()
    global cursor
    global conn
    table_data = get_data()
    today = date.today()
    for row in table_data:
        if (bool(row[6] and bool(row[5]) and bool(row[4]))):
            if (row[8]):
                print(0)
                cursor.execute("UPDATE admin SET " + 'a' + str(today)[6:].replace('-', '') + "=%s WHERE name=%s",(0, row[0]))
                conn.commit()
            else:
                print(1)
                cursor.execute("UPDATE admin SET " + 'a' + str(today)[6:].replace('-', '') + "=%s WHERE name=%s",(3, row[0]))
                conn.commit()
        else:
            print(2)
            cursor.execute("UPDATE admin SET " + 'a' + str(today)[6:].replace('-', '') + "=%s WHERE name=%s",(4, row[0]))
            conn.commit()
    close_db()
    x = q.pop(0)
    Timer(x, arrive_late, [q]).start()


def create_q():
    q = [timedelta(hours=2).total_seconds(), timedelta(hours=2).total_seconds(),
         timedelta(hours=1.75).total_seconds()]
    now = datetime.now().strftime('%H:%M:%S')
    now = datetime.strptime(now, '%H:%M:%S')
    reset_connection = datetime.strptime('8:20:00', "%H:%M:%S")
    late_check = datetime.strptime('8:16:00', "%H:%M:%S")
    delay = (reset_connection - now).total_seconds()
    delay1 = (late_check - now).total_seconds()
    if delay < 0:
        delay += timedelta(hours=24).total_seconds()
    if delay1 < 0:
        delay1 += timedelta(hours=24).total_seconds()
    Timer(delay, dudu, [q]).start()
    Timer(delay1, arrive_late, [q]).start()


def main():
    t = Thread(target = sniff1)
    t.start()
    s = Thread(target = sniff2)
    s.start()
    create_q()
            

if __name__ == '__main__':
    main()
