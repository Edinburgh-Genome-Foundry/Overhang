import itertools

complements = {"A": "T", "T": "A", "C": "G", "G": "C"}


def reverse_complement(sequence):
    """Return the reverse complement of a DNA sequence.
    For instance `reverse_complement("ATGC")` returns `"GCAT"`.


    **Parameters**

    **sequence**
    > An ATGC string (`str`).
    """
    return "".join([complements[c] for c in sequence[::-1]])


def gc_content(sequence):
    """Return the proportion of G and C in the sequence (between 0 and 1).

    This function is equivalent to `goldenhinges.biotools.gc_content()`.


    **Parameters**

    **sequence*
    > An ATGC string (`str`).
    """
    return 1.0 * len([c for c in sequence if c in "GC"]) / len(sequence)


def order_overhangs(seq):
    """Create an overhang's reverse complement, and return them in order.

    Overhangs are ordered by the letters, e.g. AATA < TATT.


    **Parameters**

    **seq**
    > ACGT sequence (`str`)."""
    sorted_overhangs = [seq, reverse_complement(seq)]
    sorted_overhangs.sort()
    return sorted_overhangs[0], sorted_overhangs[1]


def generate_overhang_pairs(overhang_length=4):
    """Generate all overhang pairs of given length.


    **Parameters**

    **overhang_length**
    > Length of overhangs (`int`).
    """
    raw_overhangs = [
        "".join(overhang)
        for overhang in itertools.product(*overhang_length * ("ACGT",))
    ]  # adapted from goldenhinges

    overhang_pairs = []  # for each overhang and its complement
    for overhang in raw_overhangs:
        overhang_pairs += [frozenset([overhang, reverse_complement(overhang)])]
    overhang_pairs = set(overhang_pairs)  # remove duplicate pairs

    return overhang_pairs


def subset_data_for_overhang(dataframe, overhang, horizontal=True, filter=True):
    """Subset tatapov dataframe for given overhang.


    **Parameters**

    **dataframe**
    > Tatapov dataset, for example `tatapov.annealing_data["25C"]["01h"]`

    **overhang**
    > Overhang class instance (`Overhang`)

    **horizontal**
    > Orientation of returned dataframe (`bool`).

    **filter**
    > If True, keep only columns (if horizontal=True) or rows (if horizontal=False)
    with nonzero values (`bool`).
    """
    overhangs = [overhang.overhang, overhang.overhang_rc]
    if horizontal:
        subset_data = dataframe.loc[overhangs]
        if filter:
            subset_data = subset_data.loc[:, subset_data.sum(axis=0) != 0]
        return subset_data
    else:  # vertical
        subset_data = dataframe[overhangs]
        if filter:
            subset_data = subset_data.loc[subset_data.sum(axis=1) != 0, :]
        return subset_data
