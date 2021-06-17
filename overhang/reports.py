# from datetime import datetime
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
    # now = datetime.now().strftime("%Y-%m-%d")
    defaults = {
        "sidebar_text": "EGF's overhang compendium (version %s)" % (__version__),
        # "end_logo_url": os.path.join(ASSETS_PATH, "imgs", "logo.png"),
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
    # if not comparatorgroup.comparisons_performed:
    #     return "Run perform_all_comparisons()!"

    # comparatorgroup.report_table = dataframe_to_html(
    #     comparatorgroup.summary_table, extra_classes=("definition",)
    # )

    # def tr_modifier(tr):
    #     tds = list(tr.find_all("td"))
    #     if len(tds) == 0:
    #         return
    #     result = tds[1]  # second element of list is the result symbol
    #     if result.text == "☑":
    #         add_css_class(tr, "positive")
    #     elif result.text == "☒":
    #         add_css_class(tr, "negative")

    # # This colours the summary table:
    # comparatorgroup.report_table = style_table_rows(
    #     comparatorgroup.report_table, tr_modifier
    # )

    # Histogram of reads in the report summary
    # comparatorgroup.fastq_figure_data = pdf_tools.figure_data(
    #     comparatorgroup.fastq_plot, fmt="svg"
    # )
    for overhang in overhangs:
        overhang.is_usable = overhang.is_good()
        overhang.gc_content_percent = int(overhang.gc_content * 100)
    # for comparator in comparatorgroup.comparators:
    #     comparator.figure_data = pdf_tools.figure_data(comparator.fig, fmt="svg")

    #     if hasattr(comparator, "is_comparison_successful"):
    #         if comparator.is_comparison_successful:
    #             height = comparator.comparison_figure.figure.get_size_inches()[1]
    #             if height > 10:
    #                 height = 10  # to fit on one page
    #             comparator.comparison_figure_data = pdf_tools.figure_data(
    #                 comparator.comparison_figure, fmt="svg", size=[7, height]
    #             )
    #         else:
    #             comparator.comparison_figure_data = None

    #     comparator.has_comparison_error = True
    #     if comparator.geneblocks_outcome == "none":
    #         comparator.geneblocks_text = (
    #             "Missing <i>de novo</i> assembly file for comparison!"
    #         )
    #     elif comparator.geneblocks_outcome == "incorrect_length":
    #         comparator.geneblocks_text = (
    #             "Incorrect length! " + comparator.incorrect_length_msg
    #         )
    #     elif comparator.geneblocks_outcome == "geneblocks_error":
    #         comparator.geneblocks_text = (
    #             "GeneBlocks comparison of <i>de novo<i/> assembly and reference failed."
    #         )
    #     elif comparator.geneblocks_outcome == "swapped_diffblocks":
    #         comparator.geneblocks_text = (
    #             "Note: the plot compares the <i>de novo</i> assembly to the "
    #             "reference " + comparator.name + " therefore there are no annotations."
    #         )
    #         comparator.has_comparison_error = False
    #     elif comparator.geneblocks_outcome == "all_good":
    #         comparator.geneblocks_text = (
    #             "<b>"
    #             + comparator.name
    #             + "</b> reference vs <i>de novo</i> assembly of reads:"
    #         )
    #         comparator.has_comparison_error = False

    #     if (
    #         hasattr(comparator, "is_assembly_reverse_complement")
    #         and comparator.is_assembly_reverse_complement
    #     ):
    #         comparator.geneblocks_text += (
    #             "Note: the <i>de novo<i/> assembly is the "
    #             "reverse complement of the reference."
    #         )

    html = end_pug_to_html(
        REPORT_TEMPLATE, overhangs=overhangs, number_of_overhangs=len(overhangs)
    )
    write_report(html, target, extra_stylesheets=(STYLESHEET,))
