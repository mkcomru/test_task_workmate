from typing import List, Dict, Any


class EmployeeDataProcessor:
    
    RATE_COLUMN_VARIANTS = ['hourly_rate', 'rate', 'salary']
    
    @staticmethod
    def normalize_employee_data(data: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        normalized_data = []
        
        for employee in data:
            normalized_employee = {}
            
            for key, value in employee.items():
                normalized_employee[key] = value
            
            rate_key = None
            for variant in EmployeeDataProcessor.RATE_COLUMN_VARIANTS:
                if variant in employee:
                    rate_key = variant
                    break
            
            if rate_key:
                normalized_employee['hourly_rate'] = employee[rate_key]
            
            try:
                normalized_employee['hours_worked'] = float(normalized_employee['hours_worked'])
                normalized_employee['hourly_rate'] = float(normalized_employee['hourly_rate'])
            except (KeyError, ValueError):
                continue
                
            normalized_data.append(normalized_employee)
            
        return normalized_data 