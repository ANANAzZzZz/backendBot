from flask import Flask
from flask import render_template
from flask import jsonify
import sqlite3
import json
from flask import request
from flask_cors import CORS, cross_origin

app = Flask(__name__)

cors = CORS(app, supports_credentials=True, resources={r"/boardGames": {"origins": "http://localhost:5000"}})

@app.route('/')
def hello_world():
    return "Hello, World!"

def find_all_boardgames():
    # db
    connection = sqlite3.connect("db.db")
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Boardgame')
    allBoardgames = cursor.fetchall()
    connection.close()

    allBoardgames_list = []

    for boardgame in allBoardgames:
        print(boardgame)
        allBoardgames_dict = {
            'ID': boardgame[0],
            'Status': boardgame[1],
            'Name': boardgame[2],
            'Description': boardgame[3],
            'Middle_game_time': boardgame[4],
            'Min_players': boardgame[5],
            'Max_players': boardgame[6],
            'Age': boardgame[7],
            'Rools': boardgame[8],
            'Image': boardgame[9],
            'Rating': boardgame[10],
            'Price_per_day': boardgame[11],
            'Base_cost': boardgame[12],
            'Complexity': boardgame[13],
            'Category': boardgame[14],
        }
        allBoardgames_list.append(allBoardgames_dict)

    return allBoardgames_list

@app.route('/boardGames')
@cross_origin(supports_credentials=True, origin='http://localhost:5000', headers=['Content- Type', 'Authorization'])
def loadMenu():
    response = jsonify(find_all_boardgames())
    print(response.headers)
    return response

# args - name; des; url; complexity; category; price
# /addBoardGame?username=321&password=123
# /addBoardGame?Name=penis&Description=228&Image=http&Complexity=hard&Category=adult&Price=20
@app.route('/addBoardGame', methods=['GET', 'POST'])
def getData():
    connection = sqlite3.connect("db.db")
    cursor = connection.cursor()

    cursor.execute('SELECT Count(*) FROM Boardgame')
    data = cursor.fetchall()
    connection.close()
    # get ID for new board using database

    ID = data[0][0]
    print(ID)
    Name = request.args.get('Name')
    Description = request.args.get('Description')
    Image = request.args.get('Image')
    Complexity = request.args.get('Complexity')
    Category = request.args.get('Category')
    Price = request.args.get('Price')

    # save to db
    connection = sqlite3.connect("db.db")
    cursor = connection.cursor()

    try:
        cursor.execute('INSERT INTO BoardGame (ID, Name, Status, Description, Middle_game_time, Min_players, Max_players, Age, Rools, Image, Rating, Price_per_day, Base_cost, Complexity, Category) VALUES (?, ?, "0", ?, "0", "0", "0", "0", "0", ?, "0", ?, "0", ?, ?)' , (ID, Name, Description, Image, Price, Complexity, Category))
    except:
        connection.close()
        return "not ok"

    connection.commit()
    connection.close()

    print(Name, Description, Image, Complexity, Category, Price)

    return "ok"
@app.route('/createOwner', methods=['GET', 'POST'])
def createOwner():
    connection = sqlite3.connect("db.db")
    cursor = connection.cursor()

    cursor.execute('SELECT Count(*) FROM Owner')
    data = cursor.fetchall()
    connection.close()

    ID = data[0][0]
    print(ID)

    Name = request.args.get('Name')

    connection = sqlite3.connect("db.db")
    cursor = connection.cursor()
    try:
        cursor.execute('INSERT INTO Owner (FIO, ID, Rating) VALUES (?, ?, "0")', (Name, ID))
    except:
        connection.close()
        return "not ok"

    connection.commit()
    connection.close()

    return "ok"

@app.route('/createRenter', methods=['GET', 'POST'])
def createRenter():
    connection = sqlite3.connect("db.db")
    cursor = connection.cursor()

    cursor.execute('SELECT Count(*) FROM Renter')
    data = cursor.fetchall()
    connection.close()

    ID = data[0][0]
    print(ID)

    Name = request.args.get('Name')

    connection = sqlite3.connect("db.db")
    cursor = connection.cursor()
    try:
        cursor.execute('INSERT INTO Renter (FIO, ID, Rating) VALUES (?, ?, "0")', (Name, ID))
    except:
        connection.close()
        return "not ok"

    connection.commit()
    connection.close()

    return "ok"


if __name__ == "__main__":
    app.run()

