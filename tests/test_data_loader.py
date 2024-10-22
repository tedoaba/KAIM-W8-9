import os
import sys
import unittest
from unittest.mock import patch
import pandas as pd

sys.path.append(os.path.abspath('../src'))

from src.data_loader import load_data

class TestDataLoader(unittest.TestCase):

    @patch('pandas.read_csv')
    def test_load_data(self, mock_read_csv):
        # Create a mock DataFrame to be returned by pandas.read_csv
        mock_df = pd.DataFrame({
            'column1': [1, 2, 3],
            'column2': ['A', 'B', 'C']
        })
        
        # Set the mock to return this DataFrame
        mock_read_csv.return_value = mock_df
        
        # Call the load_data function
        file_path = 'dummy/path/to/file.csv'
        result = load_data(file_path)
        
        # Assertions
        mock_read_csv.assert_called_once_with(file_path)  # Check that read_csv was called with the correct file path
        pd.testing.assert_frame_equal(result, mock_df)    # Check that the result is as expected

if __name__ == '__main__':
    unittest.main()
