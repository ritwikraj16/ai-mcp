"""
Tests for the LlamaCloud RAG module.
"""
import unittest
from unittest.mock import patch, MagicMock, Mock
from typing import Dict, Any

from src.rag.llama_cloud import LlamaCloudRAG


class TestLlamaCloudRAG(unittest.TestCase):
    """Test cases for the LlamaCloudRAG class."""

    def setUp(self):
        """Set up test fixtures."""
        # Mock config with required parameters
        self.mock_config = {
            "api_key": "mock_api_key",
            "org_id": "mock_org_id",
            "project": "mock_project",
            "index": "mock_index"
        }

    @patch('src.rag.llama_cloud.LlamaCloudIndex')
    def test_initialization(self, mock_llama_cloud_index):
        """Test that the LlamaCloudRAG class initializes correctly."""
        # Setup mock
        mock_index_instance = MagicMock()
        mock_query_engine = MagicMock()
        mock_index_instance.as_query_engine.return_value = mock_query_engine
        mock_llama_cloud_index.return_value = mock_index_instance
        
        # Initialize with mock config and disable LLM initialization for testing
        rag = LlamaCloudRAG(config=self.mock_config, init_llm=False)
        
        # Check that the index was created with the right parameters
        mock_llama_cloud_index.assert_called_once_with(
            name=self.mock_config["index"],
            project_name=self.mock_config["project"],
            organization_id=self.mock_config["org_id"],
            api_key=self.mock_config["api_key"]
        )
        
        # Check that the query engine was created
        mock_index_instance.as_query_engine.assert_called_once()
        
        # Verify that the query engine is accessible
        self.assertEqual(rag._query_engine, mock_query_engine)

    @patch('src.rag.llama_cloud.get_llama_cloud_config')
    @patch('src.rag.llama_cloud.LlamaCloudIndex')
    def test_initialization_with_env_config(self, mock_llama_cloud_index, mock_get_config):
        """Test initialization with configuration from environment variables."""
        # Setup mocks
        mock_get_config.return_value = self.mock_config
        mock_index_instance = MagicMock()
        mock_query_engine = MagicMock()
        mock_index_instance.as_query_engine.return_value = mock_query_engine
        mock_llama_cloud_index.return_value = mock_index_instance
        
        # Initialize without explicit config (should use env vars)
        rag = LlamaCloudRAG(init_llm=False)
        
        # Check that get_llama_cloud_config was called
        mock_get_config.assert_called_once()
        
        # Check that the index was created with the right parameters
        mock_llama_cloud_index.assert_called_once_with(
            name=self.mock_config["index"],
            project_name=self.mock_config["project"],
            organization_id=self.mock_config["org_id"],
            api_key=self.mock_config["api_key"]
        )

    def test_initialization_with_missing_params(self):
        """Test that initialization fails with missing parameters."""
        # Missing API key
        config_missing_api_key = {
            "org_id": "mock_org_id",
            "project": "mock_project",
            "index": "mock_index"
        }
        
        with self.assertRaises(ValueError) as context:
            LlamaCloudRAG(config=config_missing_api_key, init_llm=False)
        
        self.assertIn("Missing required LlamaCloud configuration parameters", str(context.exception))
        self.assertIn("api_key", str(context.exception))

    @patch('src.rag.llama_cloud.LlamaCloudIndex')
    def test_query(self, mock_llama_cloud_index):
        """Test querying the LlamaCloud index."""
        # Setup mocks
        mock_index_instance = MagicMock()
        mock_query_engine = MagicMock()
        mock_response = MagicMock()
        mock_query_engine.query.return_value = mock_response
        mock_index_instance.as_query_engine.return_value = mock_query_engine
        mock_llama_cloud_index.return_value = mock_index_instance
        
        # Initialize with mock config
        rag = LlamaCloudRAG(config=self.mock_config, init_llm=False)
        
        # Test querying
        query_text = "Where is the Space Needle located?"
        response = rag.query(query_text)
        
        # Check that query was called with the right parameters
        mock_query_engine.query.assert_called_once_with(query_text)
        
        # Check that the response is as expected
        self.assertEqual(response, mock_response)

    @patch('src.rag.llama_cloud.LlamaCloudIndex')
    def test_get_query_engine(self, mock_llama_cloud_index):
        """Test getting the query engine."""
        # Setup mocks
        mock_index_instance = MagicMock()
        mock_query_engine = MagicMock()
        mock_index_instance.as_query_engine.return_value = mock_query_engine
        mock_llama_cloud_index.return_value = mock_index_instance
        
        # Initialize with mock config
        rag = LlamaCloudRAG(config=self.mock_config, init_llm=False)
        
        # Get the query engine
        query_engine = rag.get_query_engine()
        
        # Check that it's the right object
        self.assertEqual(query_engine, mock_query_engine)

    def test_get_available_cities(self):
        """Test getting the list of available cities."""
        # Initialize with mock config and mocked LlamaCloudIndex
        with patch('src.rag.llama_cloud.LlamaCloudIndex'):
            rag = LlamaCloudRAG(config=self.mock_config, init_llm=False)
            
            # Get the list of cities
            cities = rag.get_available_cities()
            
            # Check that the expected cities are returned
            expected_cities = [
                "New York City", "Los Angeles", "Chicago", 
                "Houston", "Miami", "Seattle"
            ]
            self.assertEqual(set(cities), set(expected_cities))
            self.assertEqual(len(cities), 6)


if __name__ == "__main__":
    unittest.main()
