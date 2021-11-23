from flask import Flask
from flask_restful import Api, Resource, reqparse
from sqlalchemy import create_engine

app = Flask(__name__)
api = Api(app)

class Users(Resource):


    def get(self):
        db_connect = create_engine('sqlite:///sqlite.db')
        conn = db_connect.connect()

        parser = reqparse.RequestParser()
        parser.add_argument('ID_number', required=True)
        parser.add_argument('Surname', required=True)
        parser.add_argument('Name', required=True)
        parser.add_argument('Second_name', required=True)
        args = parser.parse_args()
        
        (n1, n2, n3, n4) = (args[i] for i in args)

        if len(n1) == len(n2) == len(n3) == len(n4) == 0:    
            data = conn.execute('SELECT * FROM employees')

        elif len(n1) > 0 and len(n2) == len(n3) == len(n4) == 0:
            if all(j.isnumeric() for j in n1):
                data = conn.execute(f'SELECT * FROM employees WHERE ID_number = {int(n1)}')
            else:
                return 'Invalid input. Please print single int value into ID field or three string values name fields'

        elif len(n1) == 0 and len(n2) > 0 and len(n3) > 0 and len(n4) > 0:
            data = conn.execute(f'SELECT * FROM employees WHERE Surname=\'{n2}\' AND Name=\'{n3}\' AND Second_name=\'{n4}\'')

        else:
            return 'Invalid input. Please print single int value into ID field or three string values name fields'

        items = []
        for row in data:
            items.append({'Surname': row[0], 'Name': row[1], 'Second_name': row[2], 'Birth_year': row[3],
            'ID_number': row[4], 'Income': row[5], 'Position': row[6], 'Entity': row[7], 'Department': row[8]})
        

        return items, 200



    def post(self):

        db_connect = create_engine('sqlite:///sqlite.db')
        conn = db_connect.connect()

        parser = reqparse.RequestParser()
        parser.add_argument('Surname', required=True)
        parser.add_argument('Name', required=True)
        parser.add_argument('Second_name', required=True)
        parser.add_argument('Birth_year', type=int, required=True)
        parser.add_argument('ID_number', type=int, required=True)
        parser.add_argument('Income', type=float, required=True)
        parser.add_argument('Position', required=True)
        parser.add_argument('Entity', required=True)
        parser.add_argument('Department', required=True)

        args = parser.parse_args()
        (n1, n2, n3, n4, n5, n6, n7, n8, n9) = (args[i] for i in args)
        checkID = conn.execute(f'SELECT * FROM employees WHERE ID_number={n5}')
        counter = 0
        for i in checkID:
            counter += 1

        if counter == 1:
            return f'Employee with ID {n5} already exist. Can\'t use same ID_number twice!', 200

        else:
            query = (f'INSERT INTO employees VALUES (\'{n1}\', \'{n2}\', \'{n3}\', '
            f'{n4}, {n5}, {n6}, \'{n7}\', \'{n8}\', \'{n9}\')')
            conn.execute(query)

            return f'Employee with ID {n5} was succesfully added to table!', 200



    def put(self):

        db_connect = create_engine('sqlite:///sqlite.db')
        conn = db_connect.connect()

        parser = reqparse.RequestParser()
        parser.add_argument('Surname', required=True)
        parser.add_argument('Name', required=True)
        parser.add_argument('Second_name', required=True)
        parser.add_argument('Birth_year', type=int, required=True)
        parser.add_argument('ID_number', type=int, required=True)
        parser.add_argument('Income', type=float, required=True)
        parser.add_argument('Position', required=True)
        parser.add_argument('Entity', required=True)
        parser.add_argument('Department', required=True)

        args = parser.parse_args()
        (n1, n2, n3, n4, n5, n6, n7, n8, n9) = (args[i] for i in args)

        checkID = conn.execute(f'SELECT * FROM employees WHERE ID_number={n5}')
        counter = 0
        for i in checkID:
            counter += 1
        
        if counter == 0:
            return f'Employee with ID {n5} don\'t exist in database, nothing to update!', 200
        else:
            query = (f'UPDATE employees SET Surname = \'{n1}\', Name = \'{n2}\', Second_name = \'{n3}\', '
            f'Birth_year = {n4}, ID_number = {n5}, Income = {n6}, '
            f'Position = \'{n7}\', Entity = \'{n8}\', Department = \'{n9}\' '
            f'WHERE ID_number = {n5}')
            conn.execute(query)

            return f'Employee with ID {n5} was succesfully updated!'
    


    def delete(self):
        db_connect = create_engine('sqlite:///sqlite.db')
        conn = db_connect.connect()

        parser = reqparse.RequestParser()
        parser.add_argument('ID_number', type=int, required=True)

        n = parser.parse_args()['ID_number']

        checkID = conn.execute(f'SELECT * FROM employees WHERE ID_number={n}')
        counter = 0
        for i in checkID:
            counter += 1
        
        if counter == 0:
            return f'There is no employee with ID {n}', 200
        else:
            conn.execute(f'DELETE FROM employees WHERE ID_number={n}')

            return f'Employee with ID {n} was succesfully deleted!', 200

        


api.add_resource(Users, '/employees')

if __name__ == '__main__':
    app.run()
