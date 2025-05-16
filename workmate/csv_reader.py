from typing import List, Dict


class CSVReader:

    @staticmethod
    def read_csv(file_path: str) -> List[Dict[str, str]]:
        result = []
        
        with open(file_path, 'r', encoding='utf-8') as file:
            headers = file.readline().strip().split(',')
            
            for line in file:
                values = line.strip().split(',')
                if len(values) == len(headers):
                    row = {headers[i]: values[i] for i in range(len(headers))}
                    result.append(row)
                    
        return result 