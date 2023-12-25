__all__ = ['Quality']

from enum import Enum

from fugo import Interval


class Quality(list[Interval], Enum):
    intervals = lambda s: [Interval(i) for i in s.split()]
    # fmt: off
    MAJOR      = intervals('P1 M3 P5')
    MINOR      = intervals('P1 m3 P5')
    DIMINISHED = intervals('P1 m3 d5')
    AUGMENTED  = intervals('P1 M3 A5')

    MAJ_MIN_7  = intervals('P1 M3 P5 m7')
    MAJ_7      = intervals('P1 M3 P5 M7')
    MIN_7      = intervals('P1 m3 P5 m7')
    MIN_MAJ_7  = intervals('P1 m3 P5 M7')
    DIM_7      = intervals('P1 m3 d5 d7')
    HALF_DIM_7 = intervals('P1 m3 d5 m7')
    # fmt: on
    del intervals
