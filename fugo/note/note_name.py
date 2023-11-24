__all__ = ['NoteName']

from dataclasses import dataclass

from .internals import Accidental, LetterName


@dataclass
class NoteName:
    letter: LetterName
    accidental: Accidental
