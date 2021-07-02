import overhang


def test_OverhangSet():
    overhangset = overhang.OverhangSet(
        overhangs=overhang.DISASTANDARD, name="Disastandard"
    )
    overhangset.inspect_overhangs()
    assert overhangset.has_duplicates
    assert overhangset.has_errors
    assert overhangset.has_rc_error
    assert overhangset.has_warnings

    overhangset = overhang.OverhangSet(overhangs=["CTAT", "GGAC", "TGTT"], name="Test")
    overhangset.find_perfect_subset()
    assert set(overhangset.subset) == set(["TGTT", "CTAT"])
