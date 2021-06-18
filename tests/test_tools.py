import overhang


def test_order_overhangs():
    assert overhang.order_overhangs("TTT") == ("AAA", "TTT")


def test_generate_overhang_pairs():
    assert overhang.generate_overhang_pairs(1) == {
        frozenset({"C", "G"}),
        frozenset({"A", "T"}),
    }
