import pytest
import sys
import os
from unittest.mock import patch, MagicMock
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import main


@patch('argparse.ArgumentParser.parse_args')
def test_parse_args(mock_parse_args):
    mock_args = MagicMock()
    mock_args.log_files = ['file1.log', 'file2.log']
    mock_args.report = 'handlers'
    mock_parse_args.return_value = mock_args
    
    args = main.parse_args()
    
    assert args.log_files == ['file1.log', 'file2.log']
    assert args.report == 'handlers'


@patch('pathlib.Path.is_file')
@patch('sys.exit')
def test_validate_args_valid(mock_exit, mock_is_file):
    mock_is_file.return_value = True
    
    args = argparse.Namespace()
    args.log_files = ['file1.log', 'file2.log']
    args.report = 'handlers'
    
    main.validate_args(args)
    
    mock_exit.assert_not_called()


@patch('pathlib.Path.is_file')
@patch('sys.exit')
def test_validate_args_file_not_exists(mock_exit, mock_is_file):
    mock_is_file.return_value = False
    
    args = argparse.Namespace()
    args.log_files = ['nonexistent.log']
    args.report = 'handlers'
    
    with patch('sys.stderr'):  
        main.validate_args(args)
    
    mock_exit.assert_called_once_with(1)


@patch('sys.exit')
def test_validate_args_invalid_report(mock_exit):
    args = argparse.Namespace()
    args.log_files = ['file1.log']
    args.report = 'invalid_report'
    
    with patch('pathlib.Path.is_file', return_value=True), \
        patch('main.ReportGenerator.REPORT_TYPES', {'handlers': None}), \
        patch('sys.stderr'):
        main.validate_args(args)
    
    mock_exit.assert_called_once_with(1)


@patch('main.parse_args')
@patch('main.validate_args')
@patch('main.ReportGenerator')
def test_main_success(mock_report_generator, mock_validate_args, mock_parse_args):
    mock_args = MagicMock()
    mock_args.log_files = ['file1.log', 'file2.log']
    mock_args.report = 'handlers'
    mock_parse_args.return_value = mock_args
    
    mock_generator_instance = MagicMock()
    mock_generator_instance.generate_report.return_value = "Report content"
    mock_report_generator.return_value = mock_generator_instance
    
    with patch('builtins.print') as mock_print:
        main.main()
    
    mock_parse_args.assert_called_once()
    mock_validate_args.assert_called_once_with(mock_args)
    mock_report_generator.assert_called_once_with(['file1.log', 'file2.log'], 'handlers')
    mock_generator_instance.generate_report.assert_called_once()
    mock_print.assert_called_once_with("Report content")


@patch('main.parse_args')
@patch('main.validate_args')
@patch('main.ReportGenerator')
@patch('sys.exit')
def test_main_exception(mock_exit, mock_report_generator, mock_validate_args, mock_parse_args):
    mock_args = MagicMock()
    mock_args.log_files = ['file1.log']
    mock_args.report = 'handlers'
    mock_parse_args.return_value = mock_args
    
    mock_report_generator.side_effect = Exception("Test exception")
    
    with patch('sys.stderr'):
        main.main()
    
    mock_exit.assert_called_once_with(1)