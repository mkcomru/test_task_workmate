import os
import tempfile
import pytest

from workmate.csv_reader import CSVReader


class TestCSVReader:

    def test_read_csv(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write("id,name,department,hours_worked,hourly_rate\n")
            temp_file.write("1,Alice Johnson,Marketing,160,50\n")
            temp_file.write("2,Bob Smith,Design,150,40\n")
            temp_file_path = temp_file.name

        try:
            result = CSVReader.read_csv(temp_file_path)

            assert len(result) == 2
            assert result[0]['id'] == '1'
            assert result[0]['name'] == 'Alice Johnson'
            assert result[0]['department'] == 'Marketing'
            assert result[0]['hours_worked'] == '160'
            assert result[0]['hourly_rate'] == '50'
            assert result[1]['id'] == '2'
            assert result[1]['name'] == 'Bob Smith'
            assert result[1]['department'] == 'Design'
            assert result[1]['hours_worked'] == '150'
            assert result[1]['hourly_rate'] == '40'
        finally:
            os.unlink(temp_file_path)

    def test_read_csv_empty_file(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write("id,name,department,hours_worked,hourly_rate\n")
            temp_file_path = temp_file.name

        try:
            result = CSVReader.read_csv(temp_file_path)

            assert len(result) == 0
        finally:
            os.unlink(temp_file_path)

    def test_read_csv_mismatched_columns(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write("id,name,department,hours_worked,hourly_rate\n")
            temp_file.write("1,Alice Johnson,Marketing,160\n")  
            temp_file.write("2,Bob Smith,Design,150,40,extra\n")
            temp_file.write("3,Carol Williams,Design,170,60\n") 
            temp_file_path = temp_file.name

        try:
            result = CSVReader.read_csv(temp_file_path)

            assert len(result) == 1
            assert result[0]['id'] == '3'
            assert result[0]['name'] == 'Carol Williams'
        finally:
            os.unlink(temp_file_path) 