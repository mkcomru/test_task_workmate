import os
import tempfile
import pytest
from unittest.mock import patch
from io import StringIO

from workmate.csv_reader import CSVReader
from workmate.data_processor import EmployeeDataProcessor
from workmate.report_generators import PayoutReportGenerator
from workmate.cli import main


class TestIntegration:

    def test_full_workflow(self):
        temp_files = []
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write("id,email,name,department,hours_worked,hourly_rate\n")
            temp_file.write("1,alice@example.com,Alice Johnson,Marketing,160,50\n")
            temp_files.append(temp_file.name)
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write("id,email,name,department,hours_worked,rate\n")
            temp_file.write("2,bob@example.com,Bob Smith,Design,150,40\n")
            temp_files.append(temp_file.name)
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write("id,email,name,department,hours_worked,salary\n")
            temp_file.write("3,carol@example.com,Carol Williams,Design,170,60\n")
            temp_files.append(temp_file.name)

        try:
            all_data = []
            
            for file_path in temp_files:
                data = CSVReader.read_csv(file_path)
                
                normalized_data = EmployeeDataProcessor.normalize_employee_data(data)
                
                all_data.extend(normalized_data)
            
            generator = PayoutReportGenerator()
            report = generator.generate(all_data)
            
            assert "Marketing" in report
            assert "Design" in report
            assert "Alice Johnson" in report
            assert "Bob Smith" in report
            assert "Carol Williams" in report
            assert "$8000" in report
            assert "$6000" in report
            assert "$10200" in report
            assert "$16200" in report  
            
            test_args = ['main.py'] + temp_files + ['--report', 'payout']
            
            with patch('sys.argv', test_args), \
                 patch('sys.stdout', new=StringIO()) as stdout:
                result = main()
            
            assert result == 0
            cli_report = stdout.getvalue()
            
            assert "Marketing" in cli_report
            assert "Design" in cli_report
            assert "Alice Johnson" in cli_report
            assert "Bob Smith" in cli_report
            assert "Carol Williams" in cli_report
            assert "$8000" in cli_report
            assert "$6000" in cli_report
            assert "$10200" in cli_report
            assert "$16200" in cli_report 
            
        finally:
            for file_path in temp_files:
                os.unlink(file_path)

    def test_error_handling(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write("id,name,department,hours_worked,hourly_rate\n")
            temp_file.write("1,Alice Johnson,Marketing,invalid,50\n")  
            temp_file_path = temp_file.name

        try:
            data = CSVReader.read_csv(temp_file_path)
            normalized_data = EmployeeDataProcessor.normalize_employee_data(data)
            
            assert len(normalized_data) == 0
            
            generator = PayoutReportGenerator()
            report = generator.generate(normalized_data)
            
            assert report == "Нет данных для формирования отчёта"
            
            test_args = ['main.py', temp_file_path, '--report', 'payout']
            
            with patch('sys.argv', test_args), \
                 patch('sys.stdout', new=StringIO()) as stdout:
                result = main()
            
            assert result == 0
            cli_report = stdout.getvalue()
            
            assert cli_report == "Нет данных для формирования отчёта\n"
            
        finally:
            os.unlink(temp_file_path) 