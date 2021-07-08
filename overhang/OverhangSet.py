import itertools
import networkx

import tatapov

from .Overhang import Overhang, get_overhang_distance
from .tools import reverse_complement, enzyme_tatapov_lookup


class OverhangSet:
    """Class for *overhang sets*.

    An overhang set is a collection of (mutually compatible) overhangs used for
    DNA assembly.


    **Parameters**

    **overhangs**
    > A list of overhang strings (`list`). Example: `["TAGG", "ATGG", "GACT"]`.

    **enzyme**
    > Enzyme used for assembly (`str`). Example: `"Esp3I"`.

    **name**
    > Name of the set (`str`).
    """

    def __init__(self, overhangs, enzyme="Esp3I", name="Unnamed set"):
        self.overhangs = [Overhang(overhang) for overhang in overhangs]
        if len(set(overhangs)) != len(overhangs):
            self.has_duplicates = True
        else:
            self.has_duplicates = False
        self.overhang_input = overhangs
        self.overhang_input_txt = ", ".join(self.overhang_input)
        self.enzyme = enzyme
        self.name = name
        self.has_warnings = False  # used during evaluation of set and reporting
        self.has_errors = False  # used during evaluation of set and reporting
        self.overhang_length = len(self.overhang_input[0])  # check length on first one

    def inspect_overhangs(self, make_plot=True):
        """Inspect compatibility of overhangs and detect potential errors in the set."""
        # DUPLICATES
        if self.has_duplicates:
            print("Incorrect set! Duplicate overhangs")
            self.has_errors = True

        # PALINDROMIC
        self.palindromic_oh = []
        self.palindromic_oh += [
            overhang.overhang for overhang in self.overhangs if overhang.is_palindromic
        ]
        if len(self.palindromic_oh) != 0:
            self.palindromic_text = "Palindromic overhang(s): " + "; ".join(
                self.palindromic_oh
            )
            print(("Incorrect set! " + self.palindromic_text))
            self.has_errors = True

        # REVERSE COMPLEMENT
        nonpalindromic_oh = set(self.overhang_input) - set(self.palindromic_oh)
        nonpalindromic_oh_rc = {reverse_complement(oh) for oh in nonpalindromic_oh}
        rc_oh = nonpalindromic_oh & nonpalindromic_oh_rc
        if rc_oh:
            self.has_rc_error = True
            self.rc_error_text = (
                "Nonpalindromic overhang(s) with reverse complement: "
                + "; ".join(rc_oh)
            )
            print(("Incorrect set! " + self.rc_error_text))
            self.has_errors = True
        else:
            self.has_rc_error = False

        # SIMILAR OVERHANGS -- we do not consider it as a flaw
        self.similar_overhangs = self.find_similar_overhangs()

        # SET SIZE
        # Based on Pryor et al., PLoS ONE (2020):
        if self.overhang_length == 3:
            n = 10
        elif self.overhang_length == 4:
            n = 20
        else:
            n = 0  # serves as False

        if n and len(self.overhang_input) > n:
            self.set_size_text = (
                "Assembly fidelity significantly decreases when using "
                + "more than %d overhangs." % n
            )  # text used in report
            print("Warning! " + self.set_size_text)
        else:
            self.set_size_text = ""

        # MISANNEALING
        self.evaluate_annealing()  # also sets `has_warnings`

        # Tatapov plots:
        if make_plot:
            figwidth = len(self.overhang_input)
            print(self.enzyme, "Tatapov plot (37 Celsius, 1 hour):")
            data = tatapov.annealing_data["37C"][enzyme_tatapov_lookup[self.enzyme]]
            subset = tatapov.data_subset(data, self.overhang_input, add_reverse=True)
            self.ax, _ = tatapov.plot_data(subset, figwidth=figwidth, plot_color="Reds")
            self.ax.figure.tight_layout()
            self.ax.plot()

    def evaluate_annealing(self):
        """Evaluate weak anneals, self-misanneals and misanneals between overhangs.

        Used in `inspect_overhangs()`.
        """
        # Prepare data:
        data = tatapov.annealing_data["37C"][enzyme_tatapov_lookup[self.enzyme]]
        subset = tatapov.data_subset(data, self.overhang_input, add_reverse=True)

        # WEAK ANNEALS
        # See cutoff 400 in Pryor et al. Figure 2.
        self.weak_anneals_list = [
            [oh.overhang, oh.overhang_rc]
            for oh in self.overhangs
            if subset[oh.overhang][oh.overhang_rc] < 400
        ]
        # Convert to text
        self.weak_anneals = [
            oh_pair[0] + "/" + oh_pair[1] for oh_pair in self.weak_anneals_list
        ]
        self.weak_anneals = "; ".join(self.weak_anneals)
        if not self.weak_anneals == "":
            self.has_warnings = True

        # SELF-MISANNEALS
        self.self_misanneals_list = [
            [oh.overhang, oh.overhang_rc]
            for oh in self.overhangs
            if subset[oh.overhang][oh.overhang] != 0
            or subset[oh.overhang_rc][oh.overhang_rc] != 0
        ]
        self.self_misanneals = [
            oh_pair[0] + "/" + oh_pair[1] for oh_pair in self.self_misanneals_list
        ]
        self.self_misanneals = "; ".join(self.self_misanneals)
        if not self.self_misanneals == "":
            self.has_warnings = True

        # MISANNEALS
        self.misanneals_list = []
        for oh1, oh2 in itertools.combinations(self.overhangs, 2):
            # 10 below is a good cutoff for misannealing pairs
            if (
                subset.loc[
                    [oh1.overhang, oh1.overhang_rc], [oh2.overhang, oh2.overhang_rc]
                ]
                > 10
            ).any(axis=None):
                # oh and reverse complement, in a list with its misannealing pair
                self.misanneals_list += [
                    [[oh1.overhang, oh1.overhang_rc], [oh2.overhang, oh2.overhang_rc]]
                ]
        # Create a text from the 4 overhangs, for the report:
        self.misanneals = [
            misannealing_pair[0][0]
            + "/"
            + misannealing_pair[0][1]
            + " ~ "
            + misannealing_pair[1][0]
            + "/"
            + misannealing_pair[1][1]
            for misannealing_pair in self.misanneals_list
        ]
        self.misanneals = "; ".join(self.misanneals)
        if not self.misanneals == "":
            self.has_warnings = True

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

    def find_perfect_subset(self):
        """Find a better overhang set by removing bad overhang interactions.

        Bad interactions are weak anneals, self-misanneals and misanneals.
        """
        self.inspect_overhangs(make_plot=False)
        # REMOVE WEAK
        oh_to_remove = [oh for oh_pair in self.weak_anneals_list for oh in oh_pair]
        self.subset = set(self.overhang_input) - set(oh_to_remove)
        # REMOVE SELF-MISANNEALING
        oh_to_remove = [oh for oh_pair in self.self_misanneals_list for oh in oh_pair]
        self.subset = set(self.subset) - set(oh_to_remove)
        # REMOVE MISANNEALING
        compatible_overhangs = []
        misanneals_for_loop = [pair[0] + pair[1] for pair in self.misanneals_list]
        for oh1, oh2 in itertools.combinations(self.subset, 2):
            add_oh = True
            for pair in misanneals_for_loop:
                if oh1 in pair and oh2 in pair:
                    add_oh = False
                    break
            if add_oh:
                compatible_overhangs += [(oh1, oh2)]
        graph = networkx.Graph(compatible_overhangs)
        max_clique, clique_size = networkx.max_weight_clique(graph, None)
        self.subset = max_clique
        print("Overhangs in subset: " + str(self.subset))
        print("Number of overhangs in subset: " + str(clique_size))
        # Visualize subset:
        figwidth = len(self.subset)
        print(self.enzyme, "Tatapov plot (37 Celsius, 1 hour):")
        data = tatapov.annealing_data["37C"][enzyme_tatapov_lookup[self.enzyme]]
        subset = tatapov.data_subset(data, self.subset, add_reverse=True)
        self.ax, _ = tatapov.plot_data(subset, figwidth=figwidth, plot_color="Reds")
        self.ax.figure.tight_layout()
        self.ax.plot()
