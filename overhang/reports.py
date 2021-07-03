import os

# import matplotlib.pyplot as plt
# import pandas
import tatapov

from pdf_reports import (
    add_css_class,
    dataframe_to_html,
    pug_to_html,
    style_table_rows,
    write_report,
)

import pdf_reports.tools as pdf_tools

from .tools import subset_data_for_overhang, plot_data, enzyme_tatapov_lookup
from .version import __version__

THIS_PATH = os.path.dirname(os.path.realpath(__file__))
ASSETS_PATH = os.path.join(THIS_PATH, "report_assets")
REPORT_TEMPLATE = os.path.join(ASSETS_PATH, "overhang_report.pug")
SET_REPORT_TEMPLATE = os.path.join(ASSETS_PATH, "overhangset_report.pug")
STYLESHEET = os.path.join(ASSETS_PATH, "report_style.css")


def end_pug_to_html(template, **context):
    defaults = {
        "sidebar_text": "EGF's compendium of overhangs (version %s)" % (__version__),
    }
    for k in defaults:
        if k not in context:
            context[k] = defaults[k]
    return pug_to_html(template, **context)


def write_pdf_report(target, overhangs, enzyme="Esp3I"):
    """Write an overhang compendium.


    **Parameters**

    **target**
    > Path for PDF file (`str`).

    **overhangs**
    > List of `Overhang` instances (`list`).

    **enzyme**
    > Enzyme used for assembly (`str`). Options: `"BsaI"`, `"BsmBI"`, `"Esp3I"` or
    `"BbsI"`.
    """
    # Prepare data for the plots:
    data = tatapov.annealing_data["37C"][enzyme_tatapov_lookup[enzyme]]

    for overhang in overhangs:
        overhang.is_usable = overhang.is_good()
        overhang.gc_content_percent = int(overhang.gc_content * 100)  # to display as %
        if overhang.gc_content < 0.25 or 0.75 < overhang.gc_content:  # none or all GC
            overhang.has_extreme_gc = True
        else:
            overhang.has_extreme_gc = False

        # Prepare the plotting data:
        subset_data = subset_data_for_overhang(data, overhang)

        # Make the plot:
        overhang.tatapov_figure, _ = plot_data(subset_data)

        # Convert the plot for PDF:
        overhang.figure_data = pdf_tools.figure_data(overhang.tatapov_figure, fmt="svg")

    html = end_pug_to_html(
        REPORT_TEMPLATE,
        overhangs=overhangs,
        number_of_overhangs=len(overhangs),
        enzyme=enzyme,
    )
    write_report(html, target, extra_stylesheets=(STYLESHEET,))


def write_overhangset_report(target, overhangset):
    """Write a report on an overhang set.


    **Parameters**

    **target**
    > Path for PDF file (`str`).

    **overhangset**
    > An `OverhangSet` instance.
    """
    # Prepare data for the plots:
    data = tatapov.annealing_data["37C"][enzyme_tatapov_lookup[overhangset.enzyme]]

    overhangset.inspect_overhangs()
    height = overhangset.ax.figure.get_size_inches()[1]
    if height > 10:
        height = 10  # to fit on the page
    overhangset.figure_data = pdf_tools.figure_data(
        overhangset.ax, fmt="svg", size=[7, height]
    )

    for overhang in overhangset.overhangs:
        overhang.is_usable = overhang.is_good()
        overhang.gc_content_percent = int(overhang.gc_content * 100)  # to display as %
        if overhang.gc_content < 0.25 or 0.75 < overhang.gc_content:  # none or all GC
            overhang.has_extreme_gc = True
        else:
            overhang.has_extreme_gc = False

        # Prepare the plotting data:
        subset_data = subset_data_for_overhang(data, overhang)

        # Make the plot:
        overhang.tatapov_figure, _ = plot_data(subset_data)

        # Convert the plot for PDF:
        overhang.figure_data = pdf_tools.figure_data(overhang.tatapov_figure, fmt="svg")

    html = end_pug_to_html(
        SET_REPORT_TEMPLATE,
        overhangset=overhangset,
        number_of_overhangs=len(overhangset.overhangs),
        # Report overhang pairs with 1 (less than 2) difference:
        similar_overhangs=overhangset.find_similar_overhangs(difference_threshold=2),
    )
    write_report(html, target, extra_stylesheets=(STYLESHEET,))
