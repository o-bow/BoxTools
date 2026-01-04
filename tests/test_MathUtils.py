from unittest import TestCase

from boxtools.data.util.mathUtils import format_number_suffix


class TestNumberSuffix(TestCase):

    def test_basic_numbers(self):
        # Default right-align (width 5)
        assert format_number_suffix(123) == '  123'
        assert format_number_suffix(9.5) == '  9.5'
        assert format_number_suffix(-7.2) == ' -7.2'

    def test_thousands(self):
        assert format_number_suffix(1234) == ' 1.2K'
        assert format_number_suffix(12000) == '  12K'
        assert format_number_suffix(-4500) == '-4.5K'

    def test_millions(self):
        assert format_number_suffix(1234567) == ' 1.2M'
        assert format_number_suffix(987654321) == ' 988M'

    def test_billions_trillions(self):
        # Standard cases
        assert format_number_suffix(999_999_999_999) == '   1T'
        assert format_number_suffix(1_234_567_890_123) == ' 1.2T'

        # Edge cases just below the next suffix
        assert format_number_suffix(999_499_999_999) == ' 999G'
        assert format_number_suffix(999_949_999_999) == '   1T'

    def test_right_align_false(self):
        # Disabling right alignment
        assert format_number_suffix(123, right_align=False) == '123'
        assert format_number_suffix(1234, right_align=False) == '1.2K'
        assert format_number_suffix(-4500, right_align=False) == '-4.5K'

    def test_small_and_negative_numbers(self):
        assert format_number_suffix(0) == '    0'
        assert format_number_suffix(0.5) == '  0.5'
        assert format_number_suffix(-999) == ' -999'

    def test_large_numbers_edge(self):
        # Very large numbers
        assert format_number_suffix(1_234_567_890_123_456) == ' 1.2P'  # Peta
        assert format_number_suffix(999_999_999_999_999_999) == '   1E'  # Exa

