__all__ = ['distance', 'Note']

from functools import total_ordering

from fugo import Interval
from ..interval.internals import Size, Quality
from .internals import Accidental, LetterName


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
