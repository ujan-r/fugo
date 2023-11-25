__all__ = ['NoteName']

from dataclasses import dataclass

from .internals import Accidental, LetterName


@dataclass
class NoteName:
    letter: LetterName
    accidental: Accidental

    def __init__(self, name: str):
        copy = self.from_string(name)

        self.letter = copy.letter
        self.accidental = copy.accidental

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
