__all__ = ['Mode']

from enum import Enum

from fugo import Interval


class Mode(Enum):
    parse = lambda s: tuple(Interval(i) for i in s.split())
    # fmt: off
    MAJOR = IONIAN  = parse('P1 M2 M3 P4 P5 M6 M7')
    DORIAN          = parse('P1 M2 m3 P4 P5 M6 m7')
    PHRYGIAN        = parse('P1 m2 m3 P4 P5 m6 m7')
    LYDIAN          = parse('P1 M2 M3 A4 P5 M6 M7')
    MIXOLYDIAN      = parse('P1 M2 M3 P4 P5 M6 m7')
    MINOR = AEOLIAN = parse('P1 M2 m3 P4 P5 m6 m7')
    LOCRIAN         = parse('P1 m2 m3 P4 d5 m6 m7')
    # fmt: on
    del parse

    @property
    def intervals(self) -> tuple[Interval, ...]:
        return self.value

    def __len__(self):
        return len(self.intervals)
