import unittest
import FlaskMariaDB

class FlaskMariaDBTest(unittest.TestCase):
		
    response = None
    
    def setUp(self):
        data = {
        "Id": "001",
        "Name": "Bulbasaur",
        "Type 1": "Grass",
        "Type 2": "Poison",
        "Category": "Seed Pok\u00e9mon",
        "Height (ft)": "2'04\"",
        "Height (m)": "0.7",
        "Weight (lbs)": "15.2",
        "Weight (kg)": "6.9",
        "Capture Rate": "45",
        "Egg Steps": "5120",
        "Exp Group": "Medium Slow",
        "Total": "318",
        "HP": "45",
        "Attack": "49",
        "Defense": "49",
        "Sp. Attack": "65",
        "Sp. Defense": "65",
        "Speed": "45"
        }
        columns= [
        "Id",
        "Name",
        "Type 1",
        "Type 2",
        "Category",
        "Height (ft)",
        "Height (m)",
        "Weight (lbs)",
        "Weight (kg)",
        "Capture Rate",
        "Egg Steps",
        "Exp Group",
        "Total",
        "HP",
        "Attack",
        "Defense",
        "Sp. Attack",
        "Sp. Defense",
        "Speed"
        ]
        response = FlaskMariaDB.jsonToSQL(data, "pokemons", columns )
      
    def testNoneResponse(self):
        self.assertIsNone(self.response, )

    def tearDown(self):
        response = None

if __name__ == '__main__':
    data = {
        "Id": "001",
        "Name": "Bulbasaur",
        "Type 1": "Grass",
        "Type 2": "Poison",
        "Category": "Seed Pok\u00e9mon",
        "Height (ft)": "2'04\"",
        "Height (m)": "0.7",
        "Weight (lbs)": "15.2",
        "Weight (kg)": "6.9",
        "Capture Rate": "45",
        "Egg Steps": "5120",
        "Exp Group": "Medium Slow",
        "Total": "318",
        "HP": "45",
        "Attack": "49",
        "Defense": "49",
        "Sp. Attack": "65",
        "Sp. Defense": "65",
        "Speed": "45"
        }
    columns= [
        "Id",
        "Name",
        "Type 1",
        "Type 2",
        "Category",
        "Height (ft)",
        "Height (m)",
        "Weight (lbs)",
        "Weight (kg)",
        "Capture Rate",
        "Egg Steps",
        "Exp Group",
        "Total",
        "HP",
        "Attack",
        "Defense",
        "Sp. Attack",
        "Sp. Defense",
        "Speed"
        ]
    response = FlaskMariaDB.jsonToSQL(data, "pokemons", columns )
    print(response)
    unittest.main()