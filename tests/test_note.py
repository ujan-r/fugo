from fugo import Note
from fugo.note import Accidental, LetterName


def test_parsing():
    expected = {
        'C4': Note(LetterName.C, Accidental.NATURAL, 4),
        '   d#4': Note(LetterName.D, Accidental.SHARP, 4),
        '  ebb-20  ': Note(LetterName.E, Accidental.DOUBLE_FLAT, -20)
    }

    for string, note in expected.items():
        assert Note.from_string(string) == note


def test_pitch():
    """Test the `Note.pitch` property."""
    expected = {
        Note(LetterName.C, Accidental.NATURAL, 4): 60,
        Note(LetterName.D, Accidental.DOUBLE_FLAT, 4): 60,
        Note(LetterName.B, Accidental.SHARP, 3): 60,
        Note(LetterName.C, Accidental.NATURAL, -1): 0
    }

    for note, number in expected.items():
        assert note.pitch == number
