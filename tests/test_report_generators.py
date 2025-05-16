import pytest

from workmate.report_generators import ReportGenerator, PayoutReportGenerator


class TestReportGenerator:

    def test_generate_not_implemented(self):
        generator = ReportGenerator()
        with pytest.raises(NotImplementedError):
            generator.generate([])


class TestPayoutReportGenerator:

    def test_generate_empty_data(self):
        generator = PayoutReportGenerator()

        result = generator.generate([])

        assert result == "Нет данных для формирования отчёта"

    def test_generate(self):
        generator = PayoutReportGenerator()

        data = [
            {'id': '1', 'name': 'Alice Johnson', 'department': 'Marketing', 'hours_worked': 160.0, 'hourly_rate': 50.0},
            {'id': '2', 'name': 'Bob Smith', 'department': 'Design', 'hours_worked': 150.0, 'hourly_rate': 40.0},
            {'id': '3', 'name': 'Carol Williams', 'department': 'Design', 'hours_worked': 170.0, 'hourly_rate': 60.0}
        ]

        result = generator.generate(data)

        assert "Design" in result
        assert "Marketing" in result
        assert "Bob Smith" in result
        assert "Carol Williams" in result
        assert "Alice Johnson" in result
        assert "$6000" in result
        assert "$10200" in result
        assert "$8000" in result
        
        assert "320" in result  
        assert "$16200" in result
        assert "160" in result  
        assert "$8000" in result

    def test_generate_single_department(self):
        generator = PayoutReportGenerator()

        data = [
            {'id': '1', 'name': 'Alice Johnson', 'department': 'Marketing', 'hours_worked': 160.0, 'hourly_rate': 50.0},
            {'id': '2', 'name': 'Frank Miller', 'department': 'Marketing', 'hours_worked': 150.0, 'hourly_rate': 45.0}
        ]

        result = generator.generate(data)

        assert "Marketing" in result
        assert "Alice Johnson" in result
        assert "Frank Miller" in result
        assert "$8000" in result
        assert "$6750" in result
        
        assert "310" in result  
        assert "$14750" in result

    def test_generate_missing_fields(self):
        generator = PayoutReportGenerator()

        data = [
            {'id': '1', 'name': 'Alice Johnson', 'department': 'Marketing', 'hours_worked': 160.0, 'hourly_rate': 50.0},
            {'id': '2', 'hours_worked': 150.0, 'hourly_rate': 40.0},  
            {'id': '3', 'name': 'Carol Williams', 'department': 'Design'}  
        ]

        result = generator.generate(data)

        assert "Marketing" in result
        assert "Unknown" in result  
        assert "Alice Johnson" in result
        assert "Unknown" in result  