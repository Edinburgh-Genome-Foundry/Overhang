import overhang as oh

for key, value in oh.enzyme_tatapov_lookup.items():
    overhang_classes = oh.generate_all_overhangs()
    target = "examples/compendium_" + key + ".pdf"
    oh.write_pdf_report(target=target, overhangs=overhang_classes, enzyme=key)
