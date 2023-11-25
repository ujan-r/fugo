from fugo import NoteName
from fugo.note.internals import Accidental, LetterName


def test_parsing():
    expected = {
        'A#': NoteName.from_attrs(LetterName.A, Accidental.SHARP),
        'bbb': NoteName.from_attrs(LetterName.B, Accidental.DOUBLE_FLAT),
        'C': NoteName.from_attrs(LetterName.C, Accidental.NATURAL),
    }

    for string, note_name in expected.items():
        assert NoteName(string) == note_name
