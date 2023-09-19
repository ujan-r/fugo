from fugo import Interval
from fugo.interval import Quality, Size


def test_parsing():
    expected = {
        'P5': Interval.from_attrs(Quality.PERFECT, Size.FIFTH),
        ' d10': Interval.from_attrs(Quality.DIMINSHED, Size.THIRD),
        'm3  ': Interval.from_attrs(Quality.MINOR, Size.THIRD),
        'M3': Interval.from_attrs(Quality.MAJOR, Size.THIRD),
        'a8': Interval.from_attrs(Quality.AUGMENTED, Size.OCTAVE),
        'A11': Interval.from_attrs(Quality.AUGMENTED, Size.FOURTH),
    }

    for string, interval in expected.items():
        assert Interval(string) == interval
