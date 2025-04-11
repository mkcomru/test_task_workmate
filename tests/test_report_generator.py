import pytest
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from report_generator import ReportGenerator


@pytest.fixture
def sample_log_entries():
    return [
        {
            'timestamp': '2025-03-28 12:44:46,000',
            'level': 'INFO',
            'component': 'django.request',
            'message': 'GET /api/v1/reviews/ 204 OK [192.168.1.59]',
            'handler': '/api/v1/reviews/',
            'status_code': '204',
            'status': 'OK',
            'ip': '192.168.1.59'
        },
        {
            'timestamp': '2025-03-28 12:45:46,000',
            'level': 'DEBUG',
            'component': 'django.request',
            'message': 'GET /admin/dashboard/ 200 OK [192.168.1.60]',
            'handler': '/admin/dashboard/',
            'status_code': '200',
            'status': 'OK',
            'ip': '192.168.1.60'
        }
    ]


def test_report_generator_init():
    generator = ReportGenerator(['log1.log', 'log2.log'], 'handlers')
    assert generator.log_files == ['log1.log', 'log2.log']
    assert generator.report_type == 'handlers'


def test_report_generator_init_invalid_report_type():
    with pytest.raises(ValueError):
        ReportGenerator(['log1.log'], 'invalid_report')


@patch('report_generator.LogParser')
def test_process_log_file(mock_log_parser, sample_log_entries):
    mock_parser_instance = MagicMock()
    mock_parser_instance.parse_log.return_value = sample_log_entries
    mock_log_parser.return_value = mock_parser_instance
    
    generator = ReportGenerator(['log1.log'], 'handlers')
    result = generator.process_log_file('log1.log')
    
    mock_log_parser.assert_called_once_with('log1.log')
    mock_parser_instance.parse_log.assert_called_once()
    assert result == sample_log_entries


@patch('report_generator.ThreadPoolExecutor')
def test_process_log_files_parallel(mock_executor, sample_log_entries):
    mock_executor_instance = MagicMock()
    mock_executor.return_value.__enter__.return_value = mock_executor_instance
    
    mock_future = MagicMock()
    mock_future.result.return_value = sample_log_entries
    
    mock_executor_instance.submit.return_value = mock_future
    
    with patch('report_generator.as_completed', return_value=[mock_future]):
        generator = ReportGenerator(['log1.log'], 'handlers')
        
        with patch.object(generator, 'process_log_file', return_value=sample_log_entries):
            result = generator.process_log_files_parallel()
    
    assert mock_executor_instance.submit.call_count == 1
    assert result == sample_log_entries


@patch('report_generator.ReportGenerator.process_log_files_parallel')
def test_generate_report(mock_process_log_files, sample_log_entries):
    mock_process_log_files.return_value = sample_log_entries
    
    generator = ReportGenerator(['log1.log'], 'handlers')
    report = generator.generate_report()
    
    mock_process_log_files.assert_called_once()
    assert isinstance(report, str)
    assert "Total requests:" in report