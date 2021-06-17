import goldenhinges


def order_overhangs(seq):
    sorted_overhangs = [seq, goldenhinges.reverse_complement(seq)]
    sorted_overhangs.sort()
    return sorted_overhangs[0], sorted_overhangs[1]
