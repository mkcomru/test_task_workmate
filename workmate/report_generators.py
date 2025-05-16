from typing import List, Dict, Any


class ReportGenerator:
    
    def generate(self, data: List[Dict[str, Any]]) -> str:
        raise NotImplementedError("Subclasses must implement this method")


class PayoutReportGenerator(ReportGenerator):
    
    def generate(self, data: List[Dict[str, Any]]) -> str:
        if not data:
            return "Нет данных для формирования отчёта"
        
        departments = {}
        for employee in data:
            department = employee.get('department', 'Unknown')
            if department not in departments:
                departments[department] = []
            departments[department].append(employee)
        
        report = []
        
        header = f"{'name':20} {'hours':10} {'rate':10} {'payout':10}"
        separator = "-" * 50
        
        for department, employees in sorted(departments.items()):
            report.append(department)
            
            total_hours = 0
            total_payout = 0
            
            for employee in employees:
                name = employee.get('name', 'Unknown')
                hours = employee.get('hours_worked', 0)
                rate = employee.get('hourly_rate', 0)
                payout = hours * rate
                
                report.append(f"{'-' * 15} {name:20} {hours:<10.0f} {rate:<10.0f} ${payout:<10.0f}")
                
                total_hours += hours
                total_payout += payout
            
            report.append(f"{' ':36} {total_hours:<10.0f} {' ':10} ${total_payout:<10.0f}")
            
        return "\n".join(report) 