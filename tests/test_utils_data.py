import pytest  
import pandas as pd  
from unittest.mock import mock_open, patch  
from src.utils import read_transactions_from_csv, read_transactions_from_xlsx  
  
@patch("src.utils.pd.read_csv")  
def test_read_transactions_from_csv_success(mock_read_csv):  
    test_df = pd.DataFrame({  
        "id": [1, 2],  
        "state": ["EXECUTED", "CANCELED"],  
        "amount": [100.5, 200.0]  
    })  
    mock_read_csv.return_value = test_df  
    result = read_transactions_from_csv("fake_path.csv")  
    assert isinstance(result, list)  
    assert len(result) == 2  
    assert result[0]["id"] == 1  
    mock_read_csv.assert_called_once_with("fake_path.csv")  
  
@patch("src.utils.pd.read_csv")  
def test_read_transactions_from_csv_file_not_found(mock_read_csv):  
    mock_read_csv.side_effect = FileNotFoundError  
    result = read_transactions_from_csv("non_existent.csv")  
    assert result == []  
    mock_read_csv.assert_called_once_with("non_existent.csv")  
  
@patch("src.utils.pd.read_csv")  
def test_read_transactions_from_csv_general_error(mock_read_csv):  
    mock_read_csv.side_effect = Exception("Something went wrong")  
    result = read_transactions_from_csv("bad_file.csv")  
    assert result == []  
  
@patch("src.utils.pd.read_excel")  
def test_read_transactions_from_xlsx_success(mock_read_excel):  
    test_df = pd.DataFrame({  
        "id": [1, 2],  
        "state": ["EXECUTED", "CANCELED"],  
        "amount": [100.5, 200.0]  
    })  
    mock_read_excel.return_value = test_df  
    result = read_transactions_from_xlsx("fake_path.xlsx")  
    assert isinstance(result, list)  
    assert len(result) == 2  
    assert result[0]["id"] == 1  
    mock_read_excel.assert_called_once_with("fake_path.xlsx", engine='openpyxl')  
  
@patch("src.utils.pd.read_excel")  
def test_read_transactions_from_xlsx_file_not_found(mock_read_excel):  
    mock_read_excel.side_effect = FileNotFoundError  
    result = read_transactions_from_xlsx("non_existent.xlsx")  
    assert result == []  
    mock_read_excel.assert_called_once_with("non_existent.xlsx", engine='openpyxl')  
  
@patch("src.utils.pd.read_excel")  
def test_read_transactions_from_xlsx_general_error(mock_read_excel):  
    mock_read_excel.side_effect = Exception("Something went wrong")  
    result = read_transactions_from_xlsx("bad_file.xlsx")  
    assert result == []  
  
