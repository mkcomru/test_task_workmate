from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any

from log_parser import LogParser
from reports.handlers import HandlersReport

class ReportGenerator:
    REPORT_TYPES = {
        'handlers': HandlersReport
    }
    
    def __init__(self, log_files: List[str], report_type: str):
        self.log_files = log_files
        self.report_type = report_type
        
        if report_type not in self.REPORT_TYPES:
            raise ValueError(f"Неизвестный тип отчета: {report_type}")
    
    def process_log_file(self, log_file: str) -> List[Dict[str, Any]]:
        parser = LogParser(log_file)
        return list(parser.parse_log())
    
    def process_log_files_parallel(self) -> List[Dict[str, Any]]:
        all_data = []
        
        with ThreadPoolExecutor() as executor:
            future_to_log = {executor.submit(self.process_log_file, log_file): log_file 
                            for log_file in self.log_files}
            
            for future in as_completed(future_to_log):
                log_file = future_to_log[future]
                try:
                    data = future.result()
                    all_data.extend(data)
                except Exception as exc:
                    print(f"Ошибка при обработке {log_file}: {exc}")
        
        return all_data
    
    def generate_report(self) -> str:
        data = self.process_log_files_parallel()
        
        report_class = self.REPORT_TYPES[self.report_type]
        report = report_class(data)
        
        return report.run()