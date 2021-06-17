import goldenhinges
from .tools import order_overhangs


class Overhang:
    def __init__(self, seq):
        self.overhang, self.overhang_rc = order_overhangs(seq)
        if len(set([self.overhang, self.overhang_rc])) == 1:
            self.is_good = False
        else:
            self.is_good = True
        # its reverse complement has the same GC content:
        self.gc_content = goldenhinges.gc_content(seq)
