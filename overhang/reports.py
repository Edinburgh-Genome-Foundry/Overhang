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

from .tools import subset_data_for_overhang, plot_data
from .version import __version__

THIS_PATH = os.path.dirname(os.path.realpath(__file__))
ASSETS_PATH = os.path.join(THIS_PATH, "report_assets")
REPORT_TEMPLATE = os.path.join(ASSETS_PATH, "overhang_report.pug")
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
    > Path for PDF file.

    **overhangs**
    > List of Overhang instances.

    **enzyme**
    > Enzyme used for assembly (`str`). Options: `"BsaI"`, `"BsmBI"`, `"Esp3I"` or
    `"BbsI"`.
    """
    enzyme_tatapov_lookup = {
        "BsaI": "2020_01h_BsaI",
        "BsmBI": "2020_01h_BsmBI",
        "Esp3I": "2020_01h_Esp3I",
        "BbsI": "2020_01h_BbsI",
    }
    # Prepare data for the plots:
    data = tatapov.annealing_data["37C"][enzyme_tatapov_lookup[enzyme]]

    for overhang in overhangs:
        overhang.is_usable = overhang.is_good()
        overhang.gc_content_percent = int(overhang.gc_content * 100)
        if overhang.gc_content < 0.25 or 0.75 < overhang.gc_content:
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

