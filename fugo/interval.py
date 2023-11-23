from enum import Enum, auto

from fugo import Note, LetterName


class Size(Enum):
    UNISON = 0
    SECOND = 1
    THIRD = 2
    FOURTH = 3
    FIFTH = 4
    SIXTH = 5
    SEVENTH = 6
    OCTAVE = 7

    # Replace compound intervals with their simple equivalents.
    @classmethod
    def _missing_(cls, value: int):
        return cls(value % 7 or 7)


class Quality(Enum):
    PERFECT = auto()
    MAJOR = auto()
    MINOR = auto()
    DIMINISHED = auto()
    AUGMENTED = auto()


class Interval:
    """Represent the distance between two notes."""

    def __init__(self, /, interval: str):
        self.quality: Quality
        self.size: Size

        copy = self.from_string(interval)
        vars(self).update(vars(copy))

    def __str__(self):
        quality = self.quality.name.lower()
        size = self.size.name.lower()

        return f'<Interval: {quality} {size}>'

    def __eq__(self, other: 'Interval'):
        if not isinstance(other, type(self)):
            return NotImplemented

        return self.quality == other.quality and self.size == other.size

    @classmethod
    def from_attrs(cls, quality: Quality, size: Size) -> 'Interval':
        obj = super().__new__(cls)

        obj.quality = quality
        obj.size = size

        return obj

    @classmethod
    def from_string(cls, interval: str) -> 'Interval':
        """Initialize an `Interval` with a human-readable string.

        args:
            - `interval`: human-readable string representing an interval
            (e.g. 'P5', 'm6', 'A2')

        returns:
            - initialized `Interval` object

        notes:
            - grammar:

            ```
            interval    := whitespace? quality size whitespace?

            quality     := perfect | major | minor | diminished | augmented
            size        := number
            whitespace  := # spaces and stuff

            perfect     := 'P' | 'p'
            major       := 'M'
            minor       := 'm'
            diminished  := 'd' | 'D'
            augmented   := 'A' | 'a'

            number      := nonzero digit* | digit
            digit       := zero | nonzero
            zero        := '0'
            nonzero     := '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
            ```
        """
        # interval = 'p32' -> _quality, _size = 'p', 32
        _quality, *_size = interval.strip()
        _size = ''.join(_size)

        try:
            _size = int(_size)
        except ValueError:
            raise ValueError('invalid interval string %r' % interval)

        if _size <= 0:
            raise ValueError(
                'invalid interval size %r in string %r' % (_size, interval)
            )

        qualities = {
            'P': Quality.PERFECT,
            'p': Quality.PERFECT,
            'M': Quality.MAJOR,
            'm': Quality.MINOR,
            'd': Quality.DIMINISHED,
            'D': Quality.DIMINISHED,
            'A': Quality.AUGMENTED,
            'a': Quality.AUGMENTED,
        }

        try:
            quality = qualities[_quality]
        except KeyError:
            raise ValueError(
                'unrecognized interval quality %r in string %r' % (_quality, interval)
            )
        size = Size(_size - 1)

        return cls.from_attrs(quality, size)


def distance(note1: Note, note2: Note, /) -> Interval:
    """Return the interval between two notes.

    args:
        - `note1`, `note2`

    returns:
        - `Interval` representing the distance between the two notes

    notes:
        - only simple intervals are returned (compound intervals, such
        as tenths, will be converted to their simple equivalents, like
        thirds)
    """
    low, high = sorted((note1, note2))

    # Get the letter names in definition order (C, D, E, F, G, A, B).
    order = [*LetterName]

    # For each note, find the position of its unaltered version within
    # the octave. Since we know which note is lower, this is sufficient
    # to determine the size of the interval (or at least its simple
    # equivalent).
    low_index = order.index(low.letter)
    high_index = order.index(high.letter)

    # Ensure that `high_index` >= `low_index` while still distinguishing
    # between unisons and octaves.
    if low.octave != high.octave:
        high_index += 7

    size = Size(high_index - low_index)

    # Find the distance (in semitones) between the two notes (mod 12 to
    # ignore octave differences). Use this, along with the interval
    # size, to determine the quality.
    distance = (high.pitch - low.pitch) % 12
    qualities = {
        Size.UNISON: {
            11: Quality.DIMINISHED,
            0: Quality.PERFECT,
            1: Quality.AUGMENTED,
        },
        Size.OCTAVE: {
            11: Quality.DIMINISHED,
            0: Quality.PERFECT,
            1: Quality.AUGMENTED,
        },
        Size.SECOND: {
            0: Quality.DIMINISHED,
            1: Quality.MINOR,
            2: Quality.MAJOR,
            3: Quality.AUGMENTED,
        },
        Size.THIRD: {
            2: Quality.DIMINISHED,
            3: Quality.MINOR,
            4: Quality.MAJOR,
            5: Quality.AUGMENTED,
        },
        Size.FOURTH: {
            4: Quality.DIMINISHED,
            5: Quality.PERFECT,
            6: Quality.AUGMENTED,
        },
        Size.FIFTH: {
            6: Quality.DIMINISHED,
            7: Quality.PERFECT,
            8: Quality.AUGMENTED,
        },
        Size.SIXTH: {
            7: Quality.DIMINISHED,
            8: Quality.MINOR,
            9: Quality.MAJOR,
            10: Quality.AUGMENTED,
        },
        Size.SEVENTH: {
            9: Quality.DIMINISHED,
            10: Quality.MINOR,
            11: Quality.MAJOR,
            0: Quality.AUGMENTED,
        },
    }
    quality = qualities[size][distance]

    return Interval.from_attrs(quality, size)
