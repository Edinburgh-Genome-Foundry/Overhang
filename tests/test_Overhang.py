import overhang


def test_Overhang():
    oh_aaa = overhang.Overhang("AAA")
    assert oh_aaa.overhang == "AAA"
    assert oh_aaa.overhang_rc == "TTT"
    assert oh_aaa.has_multimer is True  # tests count_max_repeat()
    assert oh_aaa.is_good() is True
    assert oh_aaa.gc_content == 0

    oh_ttaa = overhang.Overhang("TTAA")
    assert oh_ttaa.is_palindromic is True

    expected = [
        "L[KIRTMSN]",
        "[YFPILRTHSCDNAGV]*",
        "[IFVL][KN]",
        "L[KIRTMSN]",
        "[YFPILRTHSCDNAGV]*",
        "[IFVL][KN]",
    ]
    for index, pattern in enumerate(oh_ttaa.aa_patterns):
        assert set(pattern) == set(expected[index])

    # first example AAA had no start / stop codons
    oh_atga = overhang.Overhang("ATGA")
    assert oh_atga.has_start_codon is True
    assert oh_atga.has_stop_codon is True

    assert overhang.Overhang("ATGT").has_rc_start_codon is True
    assert overhang.Overhang("TGA").has_rc_stop_codon is True


def test_generate_all_overhangs():
    assert len(overhang.generate_all_overhangs(3)) == 32
