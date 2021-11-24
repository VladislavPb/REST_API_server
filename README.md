# REST_API_server
Simple Flask REST API server, which can be used to display, add, update and delete data from allocated SQL table.

Sqlite database used for storaging data is named 'sqlite.db', table is named 'employees'. It has 9 columns:
- Surname (string)
- Name (string)
- Second_name (string)
- Birth_year (int)
- ID_number (int) - unique value
- Income (float)
- Position (string)
- Entity (string)
- Department (string)


Interaction with a server is done through API development software such as Postman or VSCode extension Thunder Client. Four basic CRUD functions are done via basic HTTP methods: POST, GET, PUT and DELETE respectively. 
After launch of the server all queries are done via adress bar.
All methods use common first part of address: http://127.0.0.1:5000/employees

1) To display data from table, GET method is used:
- Then you send query like GET 'http://127.0.0.1:5000/employees&ID_number&Surname&Name&Second_name' with all you four input fields empty, full table is displayed via list of vocabularies. Each row represented like this:
  {
    "Surname": "Ivanov",
    "Name": "Ivan",
    "Second_name": "Ivanovich",
    "Birth_year": 1995,
    "ID_number": 222333,
    "Income": 70000.5,
    "Position": "Director",
    "Entity": "Gazprom",
    "Department": "Head"
  }
  If table is empty, you'll get an empty list without contents.
 - Then you send query GET with address like 'http://127.0.0.1:5000/employees=222333&ID_number&Surname&Name&Second_name and so on, you'll be displayed with vocabulary from associated row or empty list if there is no such ID number in table.
 - Also you can send query GET with adress like http://127.0.0.1:5000/employees&ID_number&Surname=Ivanov&Name=Ivan&Second_name=Ivanovich, you'll be displayed with one or multiple vocabularies from associated rows (cause combination Surname, Name and Second_name is not unique) or simply with empty list.
 - If you send query GET with all four field full or only two parts of name or any other make any other not normal activity, this message will be displayed - 'Invalid input. Please print single int value into ID field or three string values name fields'.

2) To add new row to table, POST method is used:
 Then you send query like POST 'http://127.0.0.1:5000/employees&Surname=Ivanov&Name=Ivan&Second_name=Ivanovich&Birth_year=1995&ID_number=222333&Income=50000.0&Position=Lawer&Entiry=Sberbank&Department=Law, data in table will be updated. Firstly server check that all 9 inputs have their respective datatypes. If no, error message is send back; If input is succesfull, server checks whenever ID_number in query already in a table:
 - If exists, message that data cannot be added displayed.
 - If doesn't exist, data is added to table as a new row and message about succesfull adding displayed.
 
 
 3) To update one row of table, PUT method is used:
  Address in query should have exactly same properties and appearance like in previvious, adding method (only difference, that here used a PUT query instead of POST). Server also validated types of data with same messages if unsuccesfull input, then checks if ID_number already exists:
  - If exists, data is updated and message of success is sent back;
  - If doesn't exist, message about nonexistence of row with this ID_number is sent back.
 
 4) To delete one row from table, DELETE method is used:
 Then you send query like DELETE 'http://127.0.0.1:5000/employees&ID_number=222333', data will be deleted if it exists. Firstly server checks whenever input is int, secondly it checks whenever row with this ID_number exists in table:
 - If exists, data is deleted and message of success is sent back;
 - If doesn't exist, message about nonexistence of row with this ID_number is sent back.
 This method is done only with ID_number as single possible argument because it is only unique column in table. Even 8 other fields don't guarantie uniqueness of a table row - but this single field succesfully does.

