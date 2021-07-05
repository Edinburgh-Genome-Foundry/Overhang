import minotaor

from .tools import gc_content, order_overhangs, generate_overhang_pairs


class Overhang:
    """Class for an overhang and its reverse complement.

    Note that the overhang with the lower order (e.g. AATA < TATT) will be stored in
    `Overhang.overhang` and the reverse complement in `Overhang.overhang_rc`, regardless
    of which was given as parameter.


    **Parameters**

    **seq**
    > ACGT sequence (`str`).
    """

    def __init__(self, seq):
        self.overhang, self.overhang_rc = order_overhangs(seq)
        if len(set([self.overhang, self.overhang_rc])) == 1:
            self.is_palindromic = True
        else:
            self.is_palindromic = False
        # its reverse complement has the same GC content:
        self.gc_content = gc_content(seq)
        self.aa_patterns = minotaor.convert_dna_to_aa_pattern(self.overhang)
        self.count_max_repeat()
        self.find_codons()

    def is_good(self):
        """Summarise attributes and decide whether overhang can be used for assembly."""
        return not any([self.is_palindromic])

    def count_max_repeat(self, repeat=3):
        """Check overhang for repeating letters.


        **Parameters**

        **repeat**
        > Number of minimum repeats to flag (`int`). For example, 3 checks for AAA etc.
        """
        for letter in "ATCG":
            if self.overhang.count(letter * repeat) != 0:
                self.has_multimer = True
                return
        self.has_multimer = False

    def find_codons(self):
        """Check overhang for presence of start and stop codons.

        This is important information on the suitability of an overhang.
        """
        start = ["ATG"]
        stop = ["TAA", "TAG", "TGA"]
        self.has_start_codon = False
        self.has_stop_codon = False
        self.has_rc_start_codon = False
        self.has_rc_stop_codon = False
        for codon in start:
            if self.overhang.count(codon) != 0:
                self.has_start_codon = True

        for codon in stop:  # "ATGA" can have both
            if self.overhang.count(codon) != 0:
                self.has_stop_codon = True

        for codon in start:
            if self.overhang_rc.count(codon) != 0:
                self.has_rc_start_codon = True

        for codon in stop:  # "ATGA" can have both
            if self.overhang_rc.count(codon) != 0:
                self.has_rc_stop_codon = True


def generate_all_overhangs(overhang_length=4):
    """Generate list Overhang class instances for all overhangs of given length.


    **Parameters**

    **overhang_length**
    > Length of overhangs (`int`).
    """
    overhang_pairs = generate_overhang_pairs(overhang_length=overhang_length)
    overhang_strings = [next(iter(overhang_pair)) for overhang_pair in overhang_pairs]
    overhang_strings.sort()

    overhangs = []
    for overhang_string in overhang_strings:
        overhang_class = Overhang(overhang_string)
        overhangs += [overhang_class]

    return overhangs


def get_overhang_distance(oh1, oh2):
    """Calculate number of different letters between two `Overhang` instances.


    **Parameters**

    **oh1**
    > An `Overhang` instance.

    **oh2**
    > An `Overhang` instance.
    """
    distance = get_hamming_distance(oh1.overhang, oh2.overhang)
    distance_rc = get_hamming_distance(oh1.overhang, oh2.overhang_rc)
    if distance < distance_rc:  # we want to find the most similar ones
        return distance
    else:
        return distance_rc


def get_hamming_distance(seq1, seq2):
    """Calculate Hamming distance between two overhang sequences.


    **Parameters**

    **seq1**
    > ACGT sequence (`str`).

    **seq2**
    > ACGT sequence (`str`).
    """
    distance = 0
    for i, letter in enumerate(seq1):
        if letter != seq2[i]:
            distance += 1

    return distance
