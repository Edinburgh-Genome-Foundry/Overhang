import os

import overhang


def test_write_pdf_report(tmpdir):
    pdf_path = os.path.join(str(tmpdir), "test_report.pdf")
    overhangs = overhang.generate_all_overhangs(3)
    overhang.write_pdf_report(target=pdf_path, overhangs=overhangs)

    with open(pdf_path, "rb") as f:
        filesize = len(f.read())
        assert filesize > 100000
