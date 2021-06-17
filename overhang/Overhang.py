import goldenhinges
import minotaor

from .tools import order_overhangs


class Overhang:
    def __init__(self, seq):
        self.overhang, self.overhang_rc = order_overhangs(seq)
        if len(set([self.overhang, self.overhang_rc])) == 1:
            self.is_palindromic = True
        else:
            self.is_palindromic = False
        # its reverse complement has the same GC content:
        self.gc_content = goldenhinges.gc_content(seq)
        self.aa_patterns = minotaor.convert_dna_to_aa_pattern(self.overhang)
        self.count_max_repeat()
        self.find_codons()

    def is_good(self):
        return not any([self.is_palindromic])

    def count_max_repeat(self, repeat=3):
        for letter in "ATCG":
            if self.overhang.count(letter * repeat) != 0:
                self.has_trimer = True
                return
        self.has_trimer = False

    def find_codons(self):
        start = ["ATG"]
        stop = ["TAA", "TAG", "TGA"]
        for codon in start:
            if self.overhang.count(codon) != 0:
                self.has_start_codon = True
            else:
                self.has_start_codon = False

        for codon in stop:  # "ATGA" can have both
            if self.overhang.count(codon) != 0:
                self.has_stop_codon = True
            else:
                self.has_stop_codon = False

        for codon in start:
            if self.overhang_rc.count(codon) != 0:
                self.has_rc_start_codon = True
            else:
                self.has_rc_start_codon = False

        for codon in stop:  # "ATGA" can have both
            if self.overhang_rc.count(codon) != 0:
                self.has_rc_stop_codon = True
            else:
                self.has_rc_stop_codon = False
