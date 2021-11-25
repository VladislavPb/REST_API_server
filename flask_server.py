from flask import Flask
from flask_restful import Api, Resource, reqparse
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker


app = Flask(__name__)
api = Api(app)


class Users(Resource):


    def get(self):
        engine = create_engine('sqlite:///sqlite.db')
        table1meta = MetaData(engine)
        table1 = Table('employees', table1meta, autoload=True)
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        parser = reqparse.RequestParser()
        parser.add_argument('ID_number', required=True)
        parser.add_argument('Surname', required=True)
        parser.add_argument('Name', required=True)
        parser.add_argument('Second_name', required=True)
        args = parser.parse_args()

        if all([not args[i] for i in args]):
            results = session.query(table1)
        elif args['ID_number'] and all(not x for x in [args['Surname'], args['Name'], args['Second_name']]):
            if all([j.isnumeric() for j in args['ID_number']]):
                results = session.query(table1).filter(table1.columns.ID_number==args['ID_number'])
            else:
                return 'Please use valid input: one int for ID_number or three strings for name columns', 200
        elif not args['ID_number'] and all(x for x in [args['Surname'], args['Name'], args['Second_name']]):
            results = session.query(table1).filter(table1.columns.Surname==args['Surname'], 
            table1.columns.Name==args['Name'], table1.columns.Second_name==args['Second_name'])
        else:
            return 'Please use valid input: one int for ID_number or three strings for name columns', 200

        items = []
        for row in results:
            items.append({'Surname': row[0], 'Name': row[1], 'Second_name': row[2], 'Birth_year': row[3],
            'ID_number': row[4], 'Income': row[5], 'Position': row[6], 'Entity': row[7], 'Department': row[8]})
        
        return items, 200


    def post(self):

        engine = create_engine('sqlite:///sqlite.db')
        table1meta = MetaData(engine)
        table1 = Table('employees', table1meta, autoload=True)
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

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

        employee = session.query(table1).filter(table1.columns.ID_number==args['ID_number']).first()
        if not employee:
            d = table1.insert().values((args['Surname'], args['Name'], args['Second_name'],
            args['Birth_year'], args['ID_number'], args['Income'], args['Position'], 
            args['Entity'], args['Department']))
            d.execute()
            return 'New user with ID_number ' + str(args['ID_number']) + ' was sucessfull added', 200
        else:
            return 'User with this ID already exists', 200


    def put(self):

        engine = create_engine('sqlite:///sqlite.db')
        table1meta = MetaData(engine)
        table1 = Table('employees', table1meta, autoload=True)
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

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

        employee = session.query(table1).filter(table1.columns.ID_number==args['ID_number']).first()
        if employee:
            d = table1.update().where(table1.columns.ID_number==args['ID_number']).values((args['Surname'], args['Name'], 
            args['Second_name'], args['Birth_year'], args['ID_number'], args['Income'], 
            args['Position'], args['Entity'], args['Department']))
            d.execute()
            return 'User with ID_number ' + str(args['ID_number']) + ' was sucessfull updated', 200
        else:
            return 'User with this ID doesn\'t exist', 200
    

    def delete(self):
        engine = create_engine('sqlite:///sqlite.db')
        table1meta = MetaData(engine)
        table1 = Table('employees', table1meta, autoload=True)
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        parser = reqparse.RequestParser()
        parser.add_argument('ID_number', type=int, required=True)
        arg = parser.parse_args()['ID_number']

        employee = session.query(table1).filter(table1.columns.ID_number==arg).first()
        
        if employee:
            d = table1.delete().where(table1.columns.ID_number==arg)
            d.execute()
            return f'Employee with ID_number {arg} was succesfully deleted', 200
        else:
            return f'Employee with ID_number {arg} was not found, nothing to delete', 200


api.add_resource(Users, '/employees')

if __name__ == '__main__':
    app.run()
