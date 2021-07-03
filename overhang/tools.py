import itertools

import tatapov

import numpy as np
import matplotlib.pyplot as plt

complements = {"A": "T", "T": "A", "C": "G", "G": "C"}

enzyme_tatapov_lookup = {
    "BsaI": "2020_01h_BsaI",
    "BsmBI": "2020_01h_BsmBI",
    "Esp3I": "2020_01h_Esp3I",
    "BbsI": "2020_01h_BbsI",
}


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

    **sequence**
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
    """Subset Tatapov dataframe for given overhang.


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


def plot_data(df, ax=None, colorbar=True, figwidth=8, plot_color="Reds"):
    """Plot a (restricted) Tatapov dataframe.


    **Parameters**

    **df**
    > One of the data sheets provided by tatapov, e.g. ``annealing_data["37C"]["01h"]``.
    Or a restriction using ``data_subset``.

    **ax**
    > A Matplotlib ax. If none is provided, one will be created and returned at the end.

    **colorbar**
    > If True, the figure will have a colorbar.

    **figwidth**
    > Custom width of the figure.

    **plot_color**
    > A Matplotlib colormap name.
    """
    # Adapted from tatapov.plot_data()
    if ax is None:
        _, ax = plt.subplots(1, figsize=(figwidth, 1.5))
    values = np.log10(np.maximum(0.5, df.values[::-1]))
    im = ax.imshow(values, cmap=plot_color)
    if colorbar:
        ax.figure.colorbar(im, label="log10( occurrences )")

    xtick_labels = df.columns
    ax.set_xticks(range(len(xtick_labels)))
    ax.set_xticklabels(xtick_labels, rotation=90)
    ax.xaxis.tick_top()
    ax.set_xlim(right=len(xtick_labels) - 0.5)

    ytick_labels = df.index[::-1]
    ax.set_yticks(range(len(ytick_labels)))
    ax.set_yticklabels(ytick_labels)
    ax.set_ylim(-0.5, len(ytick_labels) - 0.5)
    plt.close()

    return ax, im


def filter_overhangs(overhangs, enzyme="Esp3I"):
    """Filter overhangs using the Tatapov package.

    Filter out the weakly annealing and self-misannealing overhangs.


    **Parameters**

    **overhangs**
    > List of Overhang instances (`list`).

    **enzyme**
    > Enzyme used with the overhangs (`str`). See `overhang.tools.enzyme_tatapov_lookup`
    for options.
    """
    data = tatapov.annealing_data["37C"][enzyme_tatapov_lookup[enzyme]]
    overhang_input = [overhang.overhang for overhang in overhangs]
    subset = tatapov.data_subset(data, overhang_input, add_reverse=True)

    # WEAK ANNEALS
    # See cutoff 400 in Pryor et al. Figure 2.
    strong_overhangs = []
    for overhang in overhangs:
        if subset[overhang.overhang][overhang.overhang_rc] >= 400:
            strong_overhangs += [overhang]

    # SELF-MISANNEALS
    # Use 0 as cutoff:
    good_overhangs = []
    for overhang in strong_overhangs:
        if (
            subset[overhang.overhang][overhang.overhang] == 0
            and subset[overhang.overhang_rc][overhang.overhang_rc] == 0
        ):
            good_overhangs += [overhang]

    return good_overhangs
