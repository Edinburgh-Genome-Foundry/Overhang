import itertools
import goldenhinges


def order_overhangs(seq):
    """Create an overhang's reverse complement, and return an ordered list of them.

    Overhangs are ordered by the letters, e.g. AATA < TATT.


    **Parameters**

    **seq**
    > ACGT sequence (`str`)."""
    sorted_overhangs = [seq, goldenhinges.reverse_complement(seq)]
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
        overhang_pairs += [
            frozenset([overhang, goldenhinges.reverse_complement(overhang)])
        ]
    overhang_pairs = set(overhang_pairs)  # remove duplicate pairs

    return overhang_pairs
