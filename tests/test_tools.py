import overhang


def test_order_overhangs():
    assert overhang.order_overhangs("TTT") == ("AAA", "TTT")


def test_generate_overhang_pairs():
    assert overhang.generate_overhang_pairs(1) == {
        frozenset({"C", "G"}),
        frozenset({"A", "T"}),
    }


def test_filter_overhangs():
    overhangs = [
        overhang.Overhang(ovhg)
        for ovhg in [
            "TAGG",
            "ATGG",  # Good overhangs
            "CACC",  # Weakly annealing
            "GACT",  # Self misannealing
        ]
    ]
    filtered_overhangs = overhang.filter_overhangs(overhangs)
    assert len(filtered_overhangs) == 2
    assert set([ovhg.overhang for ovhg in filtered_overhangs]) == set(["CCTA", "ATGG"])
