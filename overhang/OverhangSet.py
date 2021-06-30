import itertools

import tatapov

from .Overhang import Overhang, get_overhang_distance
from .tools import reverse_complement


class OverhangSet:
    """Class for *overhang sets*.

    An overhang set is a collection of (mutually compatible) overhangs used for
    DNA assembly.


    **Parameters**

    **overhangs**
    > A list of overhang strings (`list`). Example: `["TAGG", "ATGG", "GACT"]`.

    **enzymes**
    > Enzyme used for assembly (`list`). Example: `["Esp3I"]`.
    """

    enzyme_tatapov_lookup = {
        "BsaI": "2020_01h_BsaI",
        "BsmBI": "2020_01h_BsmBI",
        "Esp3I": "2020_01h_Esp3I",
        "BbsI": "2020_01h_BbsI",
    }

    def __init__(self, overhangs, enzymes=None, name="Unnamed set"):
        self.overhangs = [Overhang(overhang) for overhang in overhangs]
        if len(set(overhangs)) != len(overhangs):
            self.has_duplicates = True
        else:
            self.has_duplicates = False
        self.overhang_input = overhangs
        self.enzymes = enzymes
        self.name = name
        self.has_warnings = False  # used during evaluation of set and reporting
        self.has_errors = False  # used during evaluation of set and reporting
        self.overhang_length = len(self.overhang_input[0])

    def inspect_overhangs(self):
        if self.has_duplicates:
            print("Incorrect set! Duplicate overhangs")

        self.palindromic_oh = []
        self.palindromic_oh += [
            overhang.overhang for overhang in self.overhangs if overhang.is_palindromic
        ]
        if len(self.palindromic_oh) != 0:
            print(
                "Incorrect set! Palindromic overhang(s):", self.palindromic_oh,
            )

        nonpalindromic_oh = set(self.overhang_input) - set(self.palindromic_oh)
        nonpalindromic_oh_rc = {reverse_complement(oh) for oh in nonpalindromic_oh}
        rc_oh = nonpalindromic_oh & nonpalindromic_oh_rc
        if rc_oh:
            self.has_rc_error = True
            print(
                "Incorrect set! Nonpalindromic overhang(s) with reverse complement:",
                rc_oh,
            )
        else:
            self.has_rc_error = False

        self.similar_overhangs = self.find_similar_overhangs()

        # Based on Pryor et al., PLoS ONE (2020):
        if self.overhang_length == 3:  # check overhang length on first one
            if len(self.overhang_input) > 10:
                print(
                    "Warning! Assembly fidelity significantly decreases when using "
                    "more than 10 overhangs."
                )
        if self.overhang_length == 4:
            if len(self.overhang_input) > 20:
                print(
                    "Warning! Assembly fidelity significantly decreases when using "
                    "more than 20 overhangs."
                )

        # Tatapov plots:
        if self.enzymes:
            figwidth = len(self.overhang_input)
            for enzyme in self.enzymes:
                print(enzyme, "Tatapov plot (37 Celsius, 1 hour):")
                data = tatapov.annealing_data["37C"][self.enzyme_tatapov_lookup[enzyme]]
                subset = tatapov.data_subset(
                    data, self.overhang_input, add_reverse=True
                )
                self.ax, _ = tatapov.plot_data(
                    subset, figwidth=figwidth, plot_color="Reds"
                )
                self.ax.figure.tight_layout()
                self.ax.plot()

    def find_similar_overhangs(self, difference_threshold=None):
        """Find overhangs that differ in fewer nucleotides than the threshold.


        **Parameters**

        **difference_threshold**
        > Acceptable number of matching nucleotides in an overhang pair (`int`).
        Overhang pairs with fewer differences are marked as similar. Defaults to 0.
        """
        if difference_threshold is None:
            difference_threshold = 0
        similar_overhangs = ""
        for oh1, oh2 in itertools.combinations(self.overhangs, 2):
            if get_overhang_distance(oh1, oh2) < difference_threshold:
                similar_overhangs += (
                    oh1.overhang
                    + "/"
                    + oh1.overhang_rc
                    + " ~ "
                    + oh2.overhang
                    + "/"
                    + oh2.overhang_rc
                    + " ;  "
                )

        if similar_overhangs == "":
            similar_overhangs = (
                "No overhangs (including reverse complements) "
                "differ by fewer than %d nucleotides." % difference_threshold
            )
        else:
            similar_overhangs = (
                "These overhang pairs (including reverse complements) have fewer than "
                "%d differences: " % difference_threshold + similar_overhangs
            )

        return similar_overhangs
