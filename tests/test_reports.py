import os

import overhang


def test_write_pdf_report(tmpdir):
    pdf_path = os.path.join(str(tmpdir), "test_report.pdf")
    overhangs = overhang.generate_all_overhangs(4)
    overhang.write_pdf_report(target=pdf_path, overhangs=overhangs[0:10])

    with open(pdf_path, "rb") as f:
        filesize = len(f.read())
        assert filesize > 300000
