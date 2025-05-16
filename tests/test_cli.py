import os
import sys
import tempfile
import pytest
from unittest.mock import patch, MagicMock
from io import StringIO

from workmate.cli import parse_arguments, main


class TestArgumentParsing:

    def test_parse_arguments(self):
        test_args = ['main.py', 'file1.csv', 'file2.csv', '--report', 'payout']

        with patch('sys.argv', test_args):
            args = parse_arguments()

        assert args.files == ['file1.csv', 'file2.csv']
        assert args.report == 'payout'


class TestMain:

    def test_main_non_existing_file(self):
        test_args = ['main.py', 'non_existing_file.csv', '--report', 'payout']

        with patch('sys.argv', test_args), \
             patch('sys.stderr', new=StringIO()) as stderr:
            result = main()

        # Проверяем результат
        assert result == 1
        assert "не существует" in stderr.getvalue()

    def test_main_unknown_report_type(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write("id,name,department,hours_worked,hourly_rate\n")
            temp_file.write("1,Alice Johnson,Marketing,160,50\n")
            temp_file_path = temp_file.name

        try:
            test_args = ['main.py', temp_file_path, '--report', 'unknown']

            with patch('sys.argv', test_args), \
                 patch('sys.stderr', new=StringIO()) as stderr:
                result = main()

            assert result == 1
            assert "неизвестный тип отчёта" in stderr.getvalue()
        finally:
            os.unlink(temp_file_path)

    def test_main_success(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write("id,name,department,hours_worked,hourly_rate\n")
            temp_file.write("1,Alice Johnson,Marketing,160,50\n")
            temp_file_path = temp_file.name

        try:
            test_args = ['main.py', temp_file_path, '--report', 'payout']

            with patch('sys.argv', test_args), \
                 patch('sys.stdout', new=StringIO()) as stdout:
                result = main()

            assert result == 0
            assert "Marketing" in stdout.getvalue()
            assert "Alice Johnson" in stdout.getvalue()
            assert "$8000" in stdout.getvalue()
        finally:
            os.unlink(temp_file_path) 