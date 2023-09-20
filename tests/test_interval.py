from fugo import Interval, Note
from fugo.interval import Quality, Size, distance


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


def test_distance():
    """Test the `distance()` function."""
    expected = {
        (Note('D4'), Note('G4')): Interval('P4'),
        (Note('A3'), Note('E4')): Interval('P5'),
        (Note('Bb2'), Note('F4')): Interval('P5'),
        (Note('G#3'), Note('E2')): Interval('M3'),
        (Note('Gx4'), Note('E2')): Interval('A3'),
    }

    for notes, interval in expected.items():
        assert distance(*notes) == interval
