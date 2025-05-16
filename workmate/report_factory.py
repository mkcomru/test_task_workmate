from typing import Optional, Type

from workmate.report_generators import ReportGenerator, PayoutReportGenerator


class ReportFactory:
    
    _generators = {
        'payout': PayoutReportGenerator
    }
    
    @classmethod
    def get_generator(cls, report_type: str) -> Optional[ReportGenerator]:
        generator_class = cls._generators.get(report_type)
        if generator_class:
            return generator_class()
        return None
    
    @classmethod
    def register_generator(cls, report_type: str, generator_class: Type[ReportGenerator]) -> None:
        cls._generators[report_type] = generator_class 