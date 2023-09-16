__all__ = ['Note']


from enum import Enum


class LetterName(Enum):
    C = 0
    D = 2
    E = 4
    F = 5
    G = 7
    A = 9
    B = 11

    def __repr__(self):
        return f'LetterName.{self.name}'

    @classmethod
    def from_string(cls, /, letter: str) -> 'LetterName':
        try:
            return cls[letter.strip().upper()]
        except KeyError:
            raise ValueError(f"invalid letter: '{letter}'") from None


class Accidental(Enum):
    DOUBLE_FLAT = -2
    FLAT = -1
    NATURAL = 0
    SHARP = +1
    DOUBLE_SHARP = +2

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


class Note:
    def __init__(self, letter: LetterName, accidental: Accidental, octave: int = 4):
        self.letter = letter
        self.accidental = accidental
        self.octave = octave

    def __eq__(self, other: 'Note') -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented

        return (
            self.letter == other.letter
            and self.accidental == other.accidental
            and self.octave == other.octave
        )

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

        return cls(letter, accidental, octave)
