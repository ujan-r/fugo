__all__ = ['Interval']

from .internals import Size, Quality


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
