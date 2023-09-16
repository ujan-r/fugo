from fugo import Interval
from fugo.interval import Quality, Size

def test_parsing():
    expected = {
        'P5': Interval(Quality.PERFECT, Size.FIFTH),
        ' d10': Interval(Quality.DIMINSHED, Size.THIRD),
        'm3  ': Interval(Quality.MINOR, Size.THIRD),
        'M3': Interval(Quality.MAJOR, Size.THIRD),
        'a8': Interval(Quality.AUGMENTED, Size.OCTAVE),
        'A11': Interval(Quality.AUGMENTED, Size.FOURTH)
    }

    for string, interval in expected.items():
        assert Interval.from_string(string) == interval
