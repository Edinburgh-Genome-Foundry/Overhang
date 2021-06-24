import tatapov

from .Overhang import Overhang


class OverhangSet:
    """Class for *overhang sets*.

    An overhang set is a collection of (mutually compatible) overhangs used for
    DNA assembly.


    **Parameters**

    **overhangs**
    > A list of overhang strings (`list`). Example: `["TAGG", "ATGG", "GACT"]`.

    **enzymes**
    > Enzyme(s) used for assembly (`list`). Example: `["Esp3I"]`.
    """

    enzyme_tatapov_lookup = {
        "BsaI": "2020_01h_BsaI",
        "BsmBI": "2020_01h_BsmBI",
        "Esp3I": "2020_01h_Esp3I",
        "BbsI": "2020_01h_BbsI",
    }

    def __init__(self, overhangs, enzymes=None):
        self.overhangs = [Overhang(overhang) for overhang in overhangs]
        if len(set(overhangs)) != len(overhangs):
            self.has_duplicates = True
        else:
            self.has_duplicates = False
        self.overhang_input = overhangs
        self.enzymes = enzymes

    def inspect_overhangs(self):
        if self.has_duplicates:
            print("Duplicate overhangs in the list!")

        # Based on Pryor et al., PLoS ONE (2020):
        if len(self.overhang_input[0]) == 3:  # check overhang length on first one
            if len(self.overhang_input) > 10:
                print(
                    "Assembly fidelity significantly decreases when using "
                    "more than 10 overhangs."
                )
        if len(self.overhang_input[0]) == 4:
            if len(self.overhang_input) > 20:
                print(
                    "Assembly fidelity significantly decreases when using "
                    "more than 20 overhangs."
                )

        self.palindromic_oh = []
        self.palindromic_oh += [
            overhang.overhang for overhang in self.overhangs if overhang.is_palindromic
        ]
        if len(self.palindromic_oh) != 0:
            print(
                "The set has the following palindromic overhangs:", self.palindromic_oh
            )
        if self.enzymes:
            figwidth = len(self.overhang_input) * 0.54  # good multiplier for nice plot
            for enzyme in self.enzymes:
                print(enzyme, "tatapov plot (37 Celsius, 1 hour):")
                data = tatapov.annealing_data["37C"][self.enzyme_tatapov_lookup[enzyme]]
                subset = tatapov.data_subset(
                    data, self.overhang_input, add_reverse=True
                )
                self.ax, _ = tatapov.plot_data(
                    subset, figwidth=figwidth, plot_color="Reds"
                )
                self.ax.figure.tight_layout()
                self.ax.plot()
