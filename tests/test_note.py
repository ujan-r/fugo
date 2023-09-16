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
