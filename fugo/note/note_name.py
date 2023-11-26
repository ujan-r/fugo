__all__ = ['NoteName']

from dataclasses import dataclass

from fugo import Interval
from .internals import Accidental, LetterName


@dataclass
class NoteName:
    letter: LetterName
    accidental: Accidental

    def __init__(self, name: str):
        copy = self.from_string(name)

        self.letter = copy.letter
        self.accidental = copy.accidental

    def __hash__(self):
        return self.pitch

    def __add__(self, interval: Interval) -> 'NoteName':
        letters = [*LetterName]
        current = letters.index(self.letter)
        new = current + interval.size.value
        letter = letters[new % len(letters)]

        distance = letter.steps_above_C - self.pitch
        offset = (interval.steps - distance) % 12
        offset = min(offset, offset - 12, key=abs)
        accidental = Accidental(offset)

        return NoteName.from_attrs(letter, accidental)

    def __sub__(self, interval: Interval) -> 'NoteName':
        return self + ~interval

    @classmethod
    def from_string(cls, name: str):
        name = name.strip()

        letter = LetterName.from_string(name[0])
        accidental = Accidental.from_string(name[1:])

        return cls.from_attrs(letter, accidental)

    @classmethod
    def from_attrs(cls, letter: LetterName, accidental: Accidental):
        obj = super().__new__(cls)

        obj.letter = letter
        obj.accidental = accidental

        return obj

    @property
    def pitch(self) -> int:
        return (self.letter.steps_above_C + self.accidental.offset) % 12
