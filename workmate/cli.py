import argparse
import os
import sys

from workmate.csv_reader import CSVReader
from workmate.data_processor import EmployeeDataProcessor
from workmate.report_factory import ReportFactory


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Генератор отчётов по данным сотрудников')
    parser.add_argument('files', nargs='+', help='CSV файлы с данными сотрудников')
    parser.add_argument('--report', required=True, help='Тип отчёта (например, payout)')
    
    return parser.parse_args()


def main() -> int:
    args = parse_arguments()
    
    for file_path in args.files:
        if not os.path.isfile(file_path):
            print(f"Ошибка: файл '{file_path}' не существует", file=sys.stderr)
            return 1
    
    report_generator = ReportFactory.get_generator(args.report)
    if not report_generator:
        print(f"Ошибка: неизвестный тип отчёта '{args.report}'", file=sys.stderr)
        return 1
    
    all_data = []
    for file_path in args.files:
        try:
            data = CSVReader.read_csv(file_path)
            normalized_data = EmployeeDataProcessor.normalize_employee_data(data)
            all_data.extend(normalized_data)
        except Exception as e:
            print(f"Ошибка при обработке файла '{file_path}': {e}", file=sys.stderr)
            return 1
    
    report = report_generator.generate(all_data)
    
    print(report)
    
    return 0 