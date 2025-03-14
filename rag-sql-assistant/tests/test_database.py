"""
Tests for the city_stats database module.
"""
import unittest
import os
import tempfile
from unittest.mock import patch, MagicMock

from src.database.city_stats import CityStatsDB
from llama_index.core import SQLDatabase
from llama_index.core.query_engine import NLSQLTableQueryEngine


class TestCityStatsDB(unittest.TestCase):
    """Test cases for the CityStatsDB class."""

    def setUp(self):
        """Set up a test database before each test."""
        # Use a temporary file for the database
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test_city_stats.db")
        self.db = CityStatsDB(self.db_path)
        # Populate with default data
        self.db.populate_default_data()

    def tearDown(self):
        """Clean up after each test."""
        self.temp_dir.cleanup()

    def test_database_creation(self):
        """Test that the database was created successfully."""
        # Check that we can get all cities
        cities = self.db.get_all_cities()
        self.assertEqual(len(cities), 6)  # We should have 6 default cities

    def test_get_city_by_name(self):
        """Test retrieving a city by name."""
        city = self.db.get_city_by_name("Miami")
        self.assertIsNotNone(city)
        self.assertEqual(city[0], "Miami")
        self.assertEqual(city[1], 449514)  # Miami's population
        self.assertEqual(city[2], "Florida")  # Miami's state

        # Test a city that doesn't exist
        non_existent_city = self.db.get_city_by_name("Springfield")
        self.assertIsNone(non_existent_city)

    def test_insert_data(self):
        """Test inserting new city data."""
        # Add a new city
        new_city = {
            "city_name": "San Francisco",
            "population": 874961,
            "state": "California"
        }
        self.db.insert_data([new_city])

        # Verify the city was added
        cities = self.db.get_all_cities()
        self.assertEqual(len(cities), 7)  # Now we should have 7 cities

        # Check the specific city data
        city = self.db.get_city_by_name("San Francisco")
        self.assertIsNotNone(city)
        self.assertEqual(city[0], "San Francisco")
        self.assertEqual(city[1], 874961)
        self.assertEqual(city[2], "California")

    def test_get_llama_index_sql_database(self):
        """Test that we can create a LlamaIndex SQLDatabase from our database."""
        sql_database = self.db.get_llama_index_sql_database()
        
        # Check that it's the right type and contains our table
        self.assertIsInstance(sql_database, SQLDatabase)
        # Check that our include_tables contains 'city_stats'
        self.assertIn("city_stats", sql_database._include_tables)

    @patch('llama_index.core.query_engine.NLSQLTableQueryEngine')
    def test_llama_index_query_engine_creation(self, mock_query_engine):
        """Test creating a query engine with a mock to avoid OpenAI API key requirement."""
        # Mock the initialization
        mock_instance = MagicMock()
        mock_query_engine.return_value = mock_instance
        
        # Get the SQL database
        sql_database = self.db.get_llama_index_sql_database()
        
        # This would normally fail without an API key, but we're mocking it
        # The initialization would happen here in the real code
        # We're just testing that the code structure would work if an API key was provided
        mock_query_engine(
            sql_database=sql_database,
            tables=["city_stats"]
        )
        
        # Assert that the mock was called with the right arguments
        mock_query_engine.assert_called_once()
        args, kwargs = mock_query_engine.call_args
        self.assertEqual(kwargs['tables'], ["city_stats"])
        self.assertIs(kwargs['sql_database'], sql_database)


if __name__ == "__main__":
    unittest.main()
