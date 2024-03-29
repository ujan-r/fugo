from fugo import Interval, Note, distance
from fugo.interval import Size, Quality


def test_parsing():
    expected = {
        'P5': Interval.from_attrs(Quality.PERFECT, Size.FIFTH),
        'd10': Interval.from_attrs(Quality.DIMINISHED, Size.THIRD),
        'm3': Interval.from_attrs(Quality.MINOR, Size.THIRD),
        'M3': Interval.from_attrs(Quality.MAJOR, Size.THIRD),
        'a8': Interval.from_attrs(Quality.AUGMENTED, Size.OCTAVE),
        'A11': Interval.from_attrs(Quality.AUGMENTED, Size.FOURTH),
    }

    for string, interval in expected.items():
        assert Interval(string) == interval


def test_invert():
    expected = {
        Interval('P1'): Interval('P8'),
        Interval('a1'): Interval('d8'),
        Interval('M3'): Interval('m6'),
        Interval('d7'): Interval('A2'),
        Interval('m2'): Interval('M7'),
    }

    for interval, inverse in expected.items():
        assert ~interval == inverse
        assert interval == ~inverse


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


def test_addition():
    cases = [
        ('d1', 'M7', 'm7'),
        ('d1', 'P8', 'd8'),
        ('P1', 'd2', 'd2'),
        ('P1', 'P1', 'P1'),
        ('P1', 'P8', 'P8'),
        ('A1', 'M3', 'A3'),
        ('M2', 'M2', 'M3'),
        ('m3', 'P5', 'm7'),
        ('A3', 'm2', 'A4'),
        ('P4', 'P5', 'P8'),
        ('m6', 'm3', 'd8'),
        ('m7', 'P4', 'm3'),
        ('d8', 'M3', 'm3'),
    ]

    for a, b, c in cases:
        assert Interval(a) + Interval(b) == Interval(c), Interval(a) + Interval(b)
