import pytest
import sys
import os
from typing import Dict, Any, List

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from reports.handlers import HandlersReport


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
        },
        {
            'timestamp': '2025-03-28 12:46:46,000',
            'level': 'WARNING',
            'component': 'django.request',
            'message': 'POST /api/v1/auth/login/ 401 Unauthorized [192.168.1.61]',
            'handler': '/api/v1/auth/login/',
            'status_code': '401',
            'status': 'Unauthorized',
            'ip': '192.168.1.61'
        },
        {
            'timestamp': '2025-03-28 12:47:46,000',
            'level': 'ERROR',
            'component': 'django.request',
            'message': 'GET /api/v1/products/ 500 ServerError [192.168.1.62]',
            'handler': '/api/v1/products/',
            'status_code': '500',
            'status': 'ServerError',
            'ip': '192.168.1.62'
        },
        {
            'timestamp': '2025-03-28 12:48:46,000',
            'level': 'CRITICAL',
            'component': 'django.request',
            'message': 'POST /api/v1/payments/ 503 ServiceUnavailable [192.168.1.63]',
            'handler': '/api/v1/payments/',
            'status_code': '503',
            'status': 'ServiceUnavailable',
            'ip': '192.168.1.63'
        },
        {
            'timestamp': '2025-03-28 12:49:46,000',
            'level': 'INFO',
            'component': 'django.db.backends',
            'message': 'Database query executed in 0.5s',
            'handler': None,
            'status_code': None,
            'status': None,
            'ip': None
        }
    ]


def test_handlers_report_generate(sample_log_entries):
    report = HandlersReport(sample_log_entries)
    report_data = report.generate()
    
    assert 'handlers' in report_data
    assert 'levels' in report_data
    assert 'total_requests' in report_data
    
    assert report_data['total_requests'] == 5
    
    handlers = report_data['handlers']
    assert len(handlers) == 5
    assert '/api/v1/reviews/' in handlers
    assert '/admin/dashboard/' in handlers
    assert '/api/v1/auth/login/' in handlers
    assert '/api/v1/products/' in handlers
    assert '/api/v1/payments/' in handlers
    
    assert report_data['levels'] == ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    
    reviews_handler = handlers['/api/v1/reviews/']
    assert reviews_handler['INFO'] == 1
    assert reviews_handler['DEBUG'] == 0
    assert reviews_handler['WARNING'] == 0
    assert reviews_handler['ERROR'] == 0
    assert reviews_handler['CRITICAL'] == 0


def test_handlers_report_format_output(sample_log_entries):
    report = HandlersReport(sample_log_entries)
    report_data = report.generate()
    output = report.format_output(report_data)
    
    assert "Total requests: 5" in output
    assert "HANDLER" in output
    assert "DEBUG" in output
    assert "INFO" in output
    assert "WARNING" in output
    assert "ERROR" in output
    assert "CRITICAL" in output
    assert "/api/v1/reviews/" in output
    assert "/admin/dashboard/" in output
    assert "/api/v1/auth/login/" in output
    assert "/api/v1/products/" in output
    assert "/api/v1/payments/" in output


def test_handlers_report_run(sample_log_entries):
    report = HandlersReport(sample_log_entries)
    output = report.run()
    
    assert output
    
    assert "Total requests: 5" in output