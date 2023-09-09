import unittest
import FlaskMariaDB

class TestDictToSQLFunctions(unittest.TestCase):
    def test_dict_to_sql_insert(self):
        data = {
            "Id": 1,
            "Name": "Test",
            "Type1": "TypeA",
            "Type2": "TypeB"
        }
        tableName = "TestTable"
        columns = ["Id", "Name", "Type1", "Type2"]
        result = FlaskMariaDB.dictToSQLInsert(data, tableName, columns)

        expected_query = "INSERT INTO TestTable (`Id`, `Name`, `Type1`, `Type2`) VALUES (%s, %s, %s, %s)"
        expected_values = [1, "Test", "TypeA", "TypeB"]

        self.assertEqual(result["insertQuery"], expected_query)
        self.assertEqual(result["values"], expected_values)

    def test_dict_to_sql_update(self):
        tableName = "TestTable"
        id = 1
        data = {
            "Name": "UpdatedName",
            "Type1": "UpdatedType"
        }
        result = FlaskMariaDB.dictToSQLUpdate(tableName, id, data)

        expected_query = "UPDATE TestTable SET Name = %s, Type1 = %s WHERE PokemonId = (SELECT Id FROM pokemons WHERE PokemonId = 1 LIMIT 1);"
        expected_values = ["UpdatedName", "UpdatedType"]

        self.assertEqual(result[0], expected_query)
        self.assertEqual(result[1], expected_values)

if __name__ == '__main__':
    unittest.main()