import pytest

from workmate.report_generators import ReportGenerator, PayoutReportGenerator
from workmate.report_factory import ReportFactory


class TestReportFactory:

    def test_get_generator_existing(self):
        generator = ReportFactory.get_generator('payout')

        assert generator is not None
        assert isinstance(generator, PayoutReportGenerator)

    def test_get_generator_non_existing(self):
        generator = ReportFactory.get_generator('non_existing')

        assert generator is None

    def test_register_generator(self):
        class TestGenerator(ReportGenerator):
            def generate(self, data):
                return "Test report"

        ReportFactory.register_generator('test', TestGenerator)

        generator = ReportFactory.get_generator('test')
        assert generator is not None
        assert isinstance(generator, TestGenerator)

        report = generator.generate([])
        assert report == "Test report"
        
        del ReportFactory._generators['test']

    def test_register_and_override_generator(self):
        original_generator_class = ReportFactory._generators.get('payout')
        
        try:
            class NewPayoutGenerator(ReportGenerator):
                def generate(self, data):
                    return "New payout report"

            ReportFactory.register_generator('payout', NewPayoutGenerator)

            generator = ReportFactory.get_generator('payout')
            assert generator is not None
            assert isinstance(generator, NewPayoutGenerator)
            assert not isinstance(generator, PayoutReportGenerator)

            report = generator.generate([])
            assert report == "New payout report"
        finally:
            if original_generator_class:
                ReportFactory._generators['payout'] = original_generator_class 