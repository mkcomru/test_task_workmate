import pytest
from unittest.mock import patch
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from log_parser import LogParser


@pytest.fixture
def sample_log_lines():
    return [
        '2025-03-28 12:44:46,000 INFO django.request: GET /api/v1/reviews/ 204 OK [192.168.1.59]',
        '2025-03-28 12:45:46,000 DEBUG django.request: GET /admin/dashboard/ 200 OK [192.168.1.60]',
        '2025-03-28 12:46:46,000 WARNING django.request: POST /api/v1/auth/login/ 401 Unauthorized [192.168.1.61]',
        '2025-03-28 12:47:46,000 ERROR django.request: GET /api/v1/products/ 500 ServerError [192.168.1.62]',
        '2025-03-28 12:48:46,000 CRITICAL django.request: POST /api/v1/payments/ 503 ServiceUnavailable [192.168.1.63]',
        '2025-03-28 12:49:46,000 INFO django.db.backends: Database query executed in 0.5s',  
        'Invalid log line format'  
    ]


def test_log_parser_init():
    parser = LogParser('test.log')
    assert parser.log_file == 'test.log'


@patch('builtins.open')
def test_parse_log_with_valid_requests(mock_open, sample_log_lines):
    mock_open.return_value.__enter__.return_value.__iter__.return_value = sample_log_lines
    
    parser = LogParser('test.log')
    log_entries = list(parser.parse_log())
    
    http_entries = [entry for entry in log_entries if entry['component'] == 'django.request']
    assert len(http_entries) == 5
    
    info_entry = log_entries[0]
    assert info_entry['level'] == 'INFO'
    assert info_entry['component'] == 'django.request'
    assert info_entry['handler'] == '/api/v1/reviews/'
    assert info_entry['status_code'] == '204'
    assert info_entry['status'] == 'OK'
    assert info_entry['ip'] == '192.168.1.59'
