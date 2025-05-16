import pytest

from workmate.data_processor import EmployeeDataProcessor


class TestEmployeeDataProcessor:

    def test_normalize_employee_data(self):
        data = [
            {'id': '1', 'name': 'Alice Johnson', 'department': 'Marketing', 'hours_worked': '160', 'hourly_rate': '50'},
            {'id': '2', 'name': 'Bob Smith', 'department': 'Design', 'hours_worked': '150', 'rate': '40'},
            {'id': '3', 'name': 'Carol Williams', 'department': 'Design', 'hours_worked': '170', 'salary': '60'}
        ]

        result = EmployeeDataProcessor.normalize_employee_data(data)

        assert len(result) == 3
        assert result[0]['id'] == '1'
        assert result[0]['name'] == 'Alice Johnson'
        assert result[0]['department'] == 'Marketing'
        assert result[0]['hours_worked'] == 160.0
        assert result[0]['hourly_rate'] == 50.0
        assert result[1]['id'] == '2'
        assert result[1]['name'] == 'Bob Smith'
        assert result[1]['department'] == 'Design'
        assert result[1]['hours_worked'] == 150.0
        assert result[1]['hourly_rate'] == 40.0
        assert result[2]['id'] == '3'
        assert result[2]['name'] == 'Carol Williams'
        assert result[2]['department'] == 'Design'
        assert result[2]['hours_worked'] == 170.0
        assert result[2]['hourly_rate'] == 60.0

    def test_normalize_employee_data_with_invalid_data(self):
        data = [
            {'id': '1', 'name': 'Alice Johnson', 'department': 'Marketing', 'hours_worked': 'invalid', 'hourly_rate': '50'},
            {'id': '2', 'name': 'Bob Smith', 'department': 'Design', 'hours_worked': '150', 'hourly_rate': 'invalid'},
            {'id': '3', 'name': 'Carol Williams', 'department': 'Design', 'hours_worked': '170', 'other_field': '60'}
        ]

        result = EmployeeDataProcessor.normalize_employee_data(data)

        assert len(result) == 0  

    def test_normalize_employee_data_mixed_valid_invalid(self):
        data = [
            {'id': '1', 'name': 'Alice Johnson', 'department': 'Marketing', 'hours_worked': '160', 'hourly_rate': '50'},
            {'id': '2', 'name': 'Bob Smith', 'department': 'Design', 'hours_worked': 'invalid', 'rate': '40'},
            {'id': '3', 'name': 'Carol Williams', 'department': 'Design', 'hours_worked': '170', 'salary': '60'}
        ]

        result = EmployeeDataProcessor.normalize_employee_data(data)

        assert len(result) == 2
        assert result[0]['id'] == '1'
        assert result[0]['name'] == 'Alice Johnson'
        assert result[1]['id'] == '3'
        assert result[1]['name'] == 'Carol Williams' 