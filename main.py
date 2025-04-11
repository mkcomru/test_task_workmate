#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

from log_parser import LogParser
from report_generator import ReportGenerator


def parse_args():
    parser = argparse.ArgumentParser(description='Анализатор логов для Django-приложения')
    parser.add_argument('log_files', nargs='+', type=str, help='Пути к лог-файлам')
    parser.add_argument('--report', type=str, required=True, help='Тип отчета для генерации')
    
    return parser.parse_args()


def validate_args(args):
    for log_file in args.log_files:
        if not Path(log_file).is_file():
            print(f"Ошибка: Файл {log_file} не существует", file=sys.stderr)
            sys.exit(1)
    
    valid_reports = list(ReportGenerator.REPORT_TYPES.keys())
    if args.report not in valid_reports:
        print(f"Ошибка: Некорректный тип отчета. Доступные отчеты: {', '.join(valid_reports)}", file=sys.stderr)
        sys.exit(1)


def main():
    args = parse_args()
    
    validate_args(args)
    
    try:
        report_generator = ReportGenerator(args.log_files, args.report)
        
        report = report_generator.generate_report()
        print(report)
    
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()