from fugo import Chord, Quality, NoteName


def test_members():
    def note_names(s: str):
        return [NoteName(n) for n in s.split()]

    expected = {
        Chord(NoteName('A'), Quality.MAJOR): note_names('A C# E'),
        Chord(NoteName('C#'), Quality.MINOR, 1): note_names('E G# C#'),
        Chord(NoteName('G'), Quality.DIMINISHED, 2): note_names('Db G Bb'),
        Chord(NoteName('Cb'), Quality.AUGMENTED): note_names('Cb Eb G'),
        Chord(NoteName('C'), Quality.MAJ_MIN_7, 3): note_names('Bb C E G'),
        Chord(NoteName('E'), Quality.MAJ_7): note_names('E G# B D#'),
        Chord(NoteName('Eb'), Quality.MIN_7): note_names('Eb Gb Bb Db'),
        Chord(NoteName('D'), Quality.MIN_MAJ_7): note_names('D F A C#'),
        Chord(NoteName('F'), Quality.DIM_7): note_names('F Ab Cb Ebb'),
        Chord(NoteName('B'), Quality.HALF_DIM_7): note_names('B D F A'),
    }

    for chord, names in expected.items():
        assert chord.note_names == names
