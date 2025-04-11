from collections import defaultdict
from typing import List, Dict, Any

from reports.base import BaseReport

class HandlersReport(BaseReport):
    
    def generate(self) -> Dict[str, Any]:
        levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        
        handlers_data = defaultdict(lambda: {level: 0 for level in levels})
        total_requests = 0
        
        for entry in self.data:
            if entry['component'] == 'django.request' and entry['handler']:
                handlers_data[entry['handler']][entry['level']] += 1
                total_requests += 1
        
        sorted_handlers = dict(sorted(handlers_data.items()))
        
        return {
            'handlers': sorted_handlers,
            'levels': levels,
            'total_requests': total_requests
        }
    
    def format_output(self, report_data: Dict[str, Any]) -> str:
        handlers = report_data['handlers']
        levels = report_data['levels']
        total_requests = report_data['total_requests']
        
        handler_width = max(len(handler) for handler in handlers.keys()) if handlers else 20
        handler_width = max(handler_width, 20)
        
        level_width = 8
        
        output = [f"Total requests: {total_requests}\n"]
        
        header = "HANDLER".ljust(handler_width)
        for level in levels:
            header += "\t" + level.ljust(level_width)
        output.append(header)
        
        level_totals = {level: 0 for level in levels}
        
        for handler, level_counts in handlers.items():
            row = handler.ljust(handler_width)
            for level in levels:
                count = level_counts[level]
                level_totals[level] += count
                row += "\t" + str(count).ljust(level_width)
            output.append(row)
        
        total_row = "".ljust(handler_width)
        for level in levels:
            total_row += "\t" + str(level_totals[level]).ljust(level_width)
        output.append(total_row)
        
        return "\n".join(output)