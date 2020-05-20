from flask import Flask, render_template, request
import psycopg2
from datetime import datetime


def connect_db():
    global conn
    global cursor
    try:
        conn = psycopg2.connect(dbname='tftyiqbk', user='tftyiqbk', password='ioia30LFy_tPe-xsKDEfSalK-jlBC7j_',
                                host='kandula.db.elephantsql.com')
    finally:
        print('please leave segevharpaz1.pythonanywhere.com and try again')
    cursor = conn.cursor()


def close_db():
    global conn
    global cursor
    conn.close()
    cursor.close()


def get_data():
    connect_db()
    global cursor
    cursor.execute("SELECT * FROM project_database")
    table_data = cursor.fetchall()
    return table_data


def do():
    connect_db()
    table_data = get_data()
    global tablee
    tablee = ['name', 'password', 'id', 'connected']
    counter = 1
    for row in table_data:
        num = []
        if row[0] != 'admin':
            num.append(row[0])
            num.append(row[1])
            num.append(row[2])
            num.append(str(bool(row[4]) and bool(row[5]) and bool(row[6])))
            num.append(row[8])
            tablee.append(num)
        counter += 1
    close_db()
    return tablee


app = Flask(__name__)


@app.route('/')
def student():
    return render_template('projectHTML.html')


@app.route('/result', methods=['POST', 'GET'])
def result():
    connect_db()
    table_data = get_data()
    global cursor
    global conn
    if request.method == 'POST':
        days = ['sunday', 'monday', 'tuesday', 'wensday', 'thursday', 'friday']
        option_data = ''
        for day in days:
            if str(request.form.get(day)) != 'none':
                option_data += (str(request.form.get(day)).replace('-', ',').replace(':', '')) + ',' + day + ','
        option_data = option_data[:-1]
        result = request.form
        result1 = str(result)[:-2]
        num = result1.split(',')
        data = []
        for i in range(1, 6, 2):
            data.append(str(num[i][2:-2]))
        isit = False
        for row in table_data:
            for i in range(3):
                if data[i] == row[i]:
                    isit = True
        if isit:
            try:
                close_db()
                return render_template("projectHTML.html", result="change the name, password or id")
            finally:
                close_db()
                print('please leave segevharpaz1.pythonanywhere.com and try again')
        else:
            sql = "INSERT INTO project_database (name, password, id, mac, connected_signin, " \
                  "connected_wifi, connected_time, times, on_time) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (data[0], data[1], data[2], 'miss_mac', True, True, True, option_data, True)
            cursor.execute(sql, val)
            conn.commit()
            close_db()
            return render_template('pass.html')


@app.route('/sign_in', methods=['POST', 'GET'])
def sign_in():
    if request.method == 'POST':
        return render_template('signin.html')


@app.route('/sign_in2', methods=['POST', 'GET'])
def sign_in2():
    connect_db()
    table_data = get_data()
    global tablee
    if request.method == 'POST':
        result = request.form
        result1 = str(result)[:-2]
        num = result1.split(',')
        data = []
        for i in range(1, 4, 2):
            data.append(num[i][2:-2])
        isit = False
        counter = 0
        for i in table_data:
            if i[0] == data[0] and i[1] == data[1]:
                isit = True
                break
            counter += 1
        if data[0] == 'admin' and data[1] == 'admin123':
            do()
            return render_template('admin.html', tablee=tablee)
        elif isit:
            data_times = str(table_data[counter][7])
            data_times = data_times.split(',')
            date = datetime.now()
            day = date.strftime("%A")
            time = str(int(date.strftime("%H%M")) + 300)
            checker = False
            for i in range(0, len(data_times), 3):
                if day.lower() == data_times[i+2] and int(data_times[i]) - 500 < int(time) and data_times[i+1] > time:
                    checker = True
                    break
            if checker:
                close_db()
                return render_template('pass.html')
            else:
                close_db()
                return render_template("signin.html", result=time)
        else:
            close_db()
            return render_template("signin.html", result="the password or name is incorrect")


@app.route('/sign_in2/delete', methods=['POST', 'GET'])
def delete():
    connect_db()
    table_data = get_data()
    global cursor
    global tablee
    global conn
    if request.method == 'POST':
        result = request.form
        result = str(result)[:-2]
        result = result.split(',')
        result = result[1][2:-2]
        checker = False
        for row in table_data:
            if row[0] == result:
                checker = True
        if checker:
            delete_sql = 'DELETE FROM project_database WHERE name = %s'
            cursor.execute(delete_sql, (result,))
            conn.commit()
            do()
            close_db()
            return render_template('admin.html', tablee=tablee)
        else:
            close_db()
            return render_template('admin.html', pro='this user is not exist in the database', tablee=tablee)


@app.route('/sign_in2/create_class', methods=['POST', 'GET'])
def createe():
    connect_db()
    global cursor
    table_data = get_data()
    if request.method == 'POST':
        result = request.form
        result1 = str(result)[:-2]
        num = result1.split(',')
        data = []
        for i in range(1, len(result), 2):
            data.append(num[i][2:-2])
        sql = 'CREATE TABLE admin (name varchar(20)'
        day = 22
        month = ['May', 'june']
        x = month[0]
        for i in range(30):
            sql += ', ' + x + str(day) + ' varchar(1)'
            day += 1
            if day > 31:
                day = 1
                x = month[1]
        sql += ')'
        cursor.execute(sql)
        conn.commit()
        for i in data:
            cursor.execute('INSERT INTO admin(name) VALUES(%s)', i)
            conn.commit()


if __name__ == '__main__':
    app.run(debug=True)
