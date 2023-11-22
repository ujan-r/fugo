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

        return (
            self.letter == other.letter
            and self.accidental == other.accidental
            and self.octave == other.octave
        )

    def __lt__(self, other: 'Note') -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented

        # The notes are in different octaves. Note that this means B#3
        # is considered "lower" than Cb4.
        if self.octave != other.octave:
            return self.octave < other.octave

        # The notes are in the same octave, so compare their letter
        # names. Note that A# is "lower" than Bb.
        if self.letter != other.letter:
            # Get the letters in definition order (C, D, E, F, G, A, B).
            order = [*LetterName]

            return order.index(self.letter) < order.index(other.letter)

        # The notes have the same octave number and letter name, so
        # compare their accidentals. This works as you'd expect.
        if self.accidental != other.accidental:
            return self.accidental.value < other.accidental.value

        # The notes have the same octave, letter name, and accidental.
        # They are equal.
        return False

    def __hash__(self):
        return self.pitch

    @classmethod
    def from_attrs(cls, letter: LetterName, accidental: Accidental, octave: int = 4):
        note = super().__new__(cls)

        note.letter = letter
        note.accidental = accidental
        note.octave = octave

        return note

    @classmethod
    def from_string(cls, /, note: str):
        letter: LetterName
        accidental: Accidental
        octave: int

        buffer = (char for char in note.strip())

        # Get the letter name from the beginning of the string.
        # Don't skip leading whitespace, as it's already been stripped.
        try:
            _letter = next(buffer)
        except StopIteration:
            raise ValueError(f'no note in string {note!r}')

        letter = LetterName[_letter.upper()]

        # Skip whitespace after letter.
        try:
            while (char := next(buffer)).isspace():
                continue
        except StopIteration:
            raise ValueError(f'no octave in string {note!r}')

        _accidental = []
        while char not in ' +-0123456789':
            _accidental.append(char)
            try:
                char = next(buffer)
            except StopIteration:
                raise ValueError(f'no octave in string {note!r}')

        accidental = Accidental.from_string(''.join(_accidental))

        while char.isspace():
            char = next(buffer)

        _octave = ''.join([char, *buffer])

        try:
            octave = int(_octave)
        except ValueError:
            raise ValueError(f'invalid octave {_octave!r} in string {note!r}')

        return cls.from_attrs(letter, accidental, octave)

    @property
    def pitch(self) -> int:
        """Return the MIDI note number for a `Note`."""

        # MIDI note numbers are higher than you might expect. The lowest
        # note (what fugo calls C-1) is assigned the value 0.
        #
        # This means--for example--that C4 (despite its octave number)
        # is actually five octaves above zero. We account for this
        # offset here.
        octave = self.octave + 1

        # Add the correct number of semitones above C based on the
        # note's letter name.
        letter = self.letter.value

        # Adjust the pitch by the correct number of semitones based on
        # the applied accidental.
        accidental = self.accidental.value

        return (octave * 12) + letter + accidental
