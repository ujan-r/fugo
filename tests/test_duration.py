from fugo import Duration


def test_operators():
    assert Duration.QUARTER + Duration.QUARTER == Duration.HALF
    assert Duration.WHOLE - Duration.QUARTER - Duration.QUARTER == Duration.HALF
    assert 4 * Duration.SIXTEENTH == Duration.QUARTER
    assert Duration.EIGHTH / 2 == Duration.SIXTEENTH
    assert (Duration.HALF + Duration.EIGHTH) % Duration.HALF == Duration.EIGHTH
