# required_packages = [pip install mysql-connector-python,
#                      pip install flask]

from flask import Flask, jsonify, request
from mysql.connector import connection
import json

app = Flask(__name__)


@app.route('/StudentInfo', methods=['GET'])
def display_student_info():
    conn = connection.MySQLConnection(user='nikhilmanvesh',
                                      password='Nikhil123@',
                                      host='localhost',
                                      database='Models')

    cursor = conn.cursor()
    cursor.execute('select * from StudentInfo')
    res = list(cursor)

    cursor.close()
    conn.close()

    if res:
        return jsonify({'message': 'records found',
                        'data': res})
    else:
        return jsonify({'message': 'no data found'})


@app.route('/StudentAcademics', methods=['GET'])
def display_student_academics():
    conn = connection.MySQLConnection(user='nikhilmanvesh',
                                      password='Nikhil123@',
                                      host='localhost',
                                      database='Models')

    cursor = conn.cursor()
    query = 'SELECT si.Roll_no, si.Name, sa.Maths, sa.Physics, sa.Chemistry, sa.Biology, sa.English\
             FROM StudentInfo AS si\
             INNER JOIN StudentAcademics AS sa\
             ON si.Roll_no = sa.Roll_no'
    cursor.execute(query)
    res = list(cursor)

    cursor.close()
    conn.close()

    if res:
        return jsonify({'message': 'record found',
                        'data': res})
    else:
        return jsonify({'message': 'no record found'})


@app.route('/StudentInfo/StudentAcademics/<int:roll_no>', methods=['GET'])
def display_student_whole_record(roll_no):
    conn = connection.MySQLConnection(user='nikhilmanvesh',
                                      password='Nikhil123@',
                                      host='localhost',
                                      database='Models')
    cursor = conn.cursor()

    query = 'SELECT si.*, sa.Maths, sa.Physics, sa.Chemistry, sa.Biology, sa.English\
             FROM StudentInfo AS si\
             INNER JOIN StudentAcademics AS sa\
             ON si.Roll_no = sa.Roll_no'
    cursor.execute(query)
    list_of_rec = list(cursor)

    for rec in list_of_rec:
        if rec[0] == roll_no:
            cursor.close()
            conn.close()

            return jsonify({'message': 'record found',
                            'data': rec})
    else:
        cursor.close()
        conn.close()

        return jsonify({'message': 'no record found'})


@app.route('/update/StudentInfo/StudentAcademics', methods=['POST'])
def update_record():

    po_man_rec = json.loads(request.data)
    conn = connection.MySQLConnection(user='nikhilmanvesh',
                                      password='Nikhil123@',
                                      host='localhost',
                                      database='Models')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM StudentInfo')
    list_of_rec = list(cursor)

    flag = False
    index = False
    for ind, rec in enumerate(list_of_rec):
        if rec[0] == po_man_rec['Roll_no']:
            flag = True
            index = rec[0]
            break

    if flag:
        query_list = ['UPDATE StudentInfo set Name = ' + '(' + '"' + po_man_rec['Name'] + '"' + ')' + ', ' +
                      'Class = ' + '(' + '"' + po_man_rec['Class'] + '"' + ')' + ', ' +
                      'Mobile = ' + '(' + '"' + po_man_rec['Mobile'] + '"' + ')' + ', ' +
                      'Address = ' + '(' + '"' + po_man_rec['Address'] + '"' + ')' + ' WHERE Roll_no = ' + str(index),

                      'UPDATE StudentAcademics set Maths = ' + str(po_man_rec['Maths']) + ', ' +
                      'Physics = ' + str(po_man_rec['Physics']) + ', ' +
                      'Chemistry = ' + str(po_man_rec['Chemistry']) + ', ' +
                      'Biology = ' + str(po_man_rec['Biology']) + ', ' +
                      'English = ' + str(po_man_rec['English']) + ' WHERE Roll_no = ' + str(index)]

        for query in query_list:
            cursor.execute(query)
            conn.commit()

        cursor.close()
        conn.close()

        return jsonify({'message': 'record updated'})
    else:
        cursor.close()
        conn.close()

        return jsonify({'message': 'no record found to be updated'})


@app.route('/delete/StudentInfo/StudentAcademics/<int:roll_no>', methods=['DELETE'])
def delete_record(roll_no):
    conn = connection.MySQLConnection(user='nikhilmanvesh',
                                      password='Nikhil123@',
                                      host='localhost',
                                      database='Models')
    cursor = conn.cursor()
    cursor.execute('SELECT * from StudentInfo')
    list_of_rec1 = list(cursor)

    index = False
    flag = False

    for ind, rec in enumerate(list_of_rec1):
        if rec[0] == roll_no:
            flag = True
            index = rec[0]
            break

    if flag:
        query_list = ['DELETE FROM StudentAcademics where Roll_no = ' + str(index),
                      'DELETE from StudentInfo where Roll_no = ' + str(index)]

        for query in query_list:
            cursor.execute(query)
            conn.commit()

        cursor.close()
        conn.close()

        return jsonify({'message': 'record deleted successfully'})
    else:
        cursor.close()
        conn.close()

        return jsonify({'message': 'no record found to be deleted'})


if __name__ == "__main__":
    app.run()
