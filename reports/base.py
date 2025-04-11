from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseReport(ABC):
    
    def __init__(self, data: List[Dict[str, Any]]):
        self.data = data
    
    @abstractmethod
    def generate(self) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def format_output(self, report_data: Dict[str, Any]) -> str:
        pass
    
    def run(self) -> str:
        report_data = self.generate()
        return self.format_output(report_data)