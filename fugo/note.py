from enum import Enum
from functools import total_ordering


class LetterName(Enum):
    C = 0
    D = 2
    E = 4
    F = 5
    G = 7
    A = 9
    B = 11

    def __init__(self, steps_above_C: int):
        self.steps_above_C = steps_above_C

    def __repr__(self):
        return f'LetterName.{self.name}'

    @classmethod
    def from_string(cls, /, letter: str) -> 'LetterName':
        try:
            return cls[letter.strip().upper()]
        except KeyError:
            raise ValueError(f'invalid letter: {letter!r}') from None


class Accidental(Enum):
    # fmt: off
    DOUBLE_FLAT  = -2
    FLAT         = -1
    NATURAL      =  0
    SHARP        = +1
    DOUBLE_SHARP = +2
    # fmt: on

    def __init__(self, offset: int):
        self.offset = offset

    @classmethod
    def from_string(cls, /, accidental: str) -> 'Accidental':
        mapping = {
            '𝄫': cls.DOUBLE_FLAT,
            'bb': cls.DOUBLE_FLAT,
            '♭': cls.FLAT,
            'b': cls.FLAT,
            '♮': cls.NATURAL,
            '': cls.NATURAL,
            '♯': cls.SHARP,
            '#': cls.SHARP,
            '𝄪': cls.DOUBLE_SHARP,
            'x': cls.DOUBLE_SHARP,
        }

        try:
            return mapping[accidental.strip()]
        except KeyError:
            raise ValueError(f'invalid accidental: {accidental!r}') from None


@total_ordering
class Note:
    def __init__(self, /, note: str):
        copy = Note.from_string(note)

        self.letter: LetterName = copy.letter
        self.accidental: Accidental = copy.accidental
        self.octave: int = copy.octave

    def __eq__(self, other: 'Note') -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented

        t1 = (self.octave, self.letter.steps_above_C, self.accidental.offset)
        t2 = (other.octave, other.letter.steps_above_C, other.accidental.offset)
        return t1 == t2

    def __lt__(self, other: 'Note') -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented

        t1 = (self.octave, self.letter.steps_above_C, self.accidental.offset)
        t2 = (other.octave, other.letter.steps_above_C, other.accidental.offset)
        return t1 < t2

    def __hash__(self):
        return self.pitch

    @classmethod
    def from_attrs(cls, letter: LetterName, accidental: Accidental, octave: int):
        # Create a new `Note` object without using the constructor,
        # which relies on this method internally.
        note = super().__new__(cls)

        note.letter = letter
        note.accidental = accidental
        note.octave = octave

        return note

    @classmethod
    def from_string(cls, note: str) -> 'Note':
        # Use a generator to simplify parsing code.
        stream = (c for c in note.strip())

        # Since letter names are one character long, we can grab easily
        # the letter name.
        _letter = next(stream)
        try:
            letter = LetterName.from_string(_letter)
        except ValueError:
            raise ValueError(f"couldn't find letter name in {note!r}")

        _accidental = ''
        for c in stream:
            if c in '+-0123456789':
                # We have reached the end of the accidental once we
                # encounter something that looks like a number. The
                # remaining characters must be the octave number.
                _octave = c + ''.join(stream)
                break

            # If we haven't encountered a number, assume we are still
            # reading the accidental.
            #
            # While repeated string concatenation is generally
            # considered bad style, the strings involved are so short
            # that it doesn't matter here.
            _accidental += c
        else:
            # If we reach the end of the buffer without encountering a
            # numeric character, there must not be an octave number.
            raise ValueError(f'missing octave number in {note!r}')

        accidental = Accidental.from_string(_accidental)
        octave = int(_octave)

        return cls.from_attrs(letter, accidental, octave)

    @property
    def pitch(self) -> int:
        """Get the MIDI note number."""
        # MIDI note numbers are higher than you might expect. The lowest
        # note (what fugo calls C-1) is assigned the value 0.
        #
        # This means--for example--that C4 (despite its octave number)
        # is actually five octaves above zero. Account for this offset.
        octave = self.octave + 1

        return octave * 12 + self.letter.steps_above_C + self.accidental.offset
