import os

# import matplotlib.pyplot as plt
# import pandas

from pdf_reports import (
    add_css_class,
    dataframe_to_html,
    pug_to_html,
    style_table_rows,
    write_report,
)

# import pdf_reports.tools as pdf_tools

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


def write_pdf_report(target, overhangs):
    """Write an overhang compendium.


    **Parameters**

    **target**
    > Path for PDF file.

    **overhangs**
    > List of Overhang instances.
    """
    for overhang in overhangs:
        overhang.is_usable = overhang.is_good()
        overhang.gc_content_percent = int(overhang.gc_content * 100)
        if overhang.gc_content < 0.25 or 0.75 < overhang.gc_content:
            overhang.has_extreme_gc = True
        else:
            overhang.has_extreme_gc = False
    html = end_pug_to_html(
        REPORT_TEMPLATE, overhangs=overhangs, number_of_overhangs=len(overhangs)
    )
    write_report(html, target, extra_stylesheets=(STYLESHEET,))
