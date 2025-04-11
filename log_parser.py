import re
from typing import List, Dict, Generator, Any

class LogParser:
    
    def __init__(self, log_file: str):
        self.log_file = log_file
    
    def parse_log(self) -> Generator[Dict[str, Any], None, None]:
        log_pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) (\w+) ([\w\.]+): (.+)'
        request_pattern = r'(?:GET|POST|PUT|DELETE|PATCH) (\S+) (\d{3}) (\w+) \[([\d\.]+)\]'
        
        with open(self.log_file, 'r', encoding='utf-8') as file:
            for line in file:
                match = re.match(log_pattern, line.strip())
                if not match:
                    continue
                
                timestamp, level, component, message = match.groups()
                
                log_entry = {
                    'timestamp': timestamp,
                    'level': level,
                    'component': component,
                    'message': message,
                    'handler': None,
                    'status_code': None,
                    'status': None,
                    'ip': None
                }
                
                if component == 'django.request':
                    req_match = re.search(request_pattern, message)
                    if req_match:
                        handler, status_code, status, ip = req_match.groups()
                        log_entry.update({
                            'handler': handler,
                            'status_code': status_code,
                            'status': status,
                            'ip': ip
                        })
                
                yield log_entry