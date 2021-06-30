import overhang as oh

# Disaster + standard =
overhangset = oh.OverhangSet(overhangs=oh.DISASTANDARD, name="Disastandard")
oh.write_overhangset_report("set_Disastandard_report.pdf", overhangset)

EMMA_overhangs = [
    "TAGG",
    "ATGG",
    "GACT",
    "GGAC",
    "TCCG",
    "CCAG",
    "CAGC",
    "AGGC",
    "ATCC",
    "GCGT",
    "TGCT",
    "GGTA",
    "CGTC",
    "TCAC",
    "CTAC",
    "GCAA",
    "CCCT",
    "GCTC",
    "CGGT",
    "GTGC",
    "AGCG",
    "TGGA",
    "GTTG",
    "CGAA",
    "CACG",
    "ACTG",
    "ACGA",
]
overhangset = oh.OverhangSet(overhangs=EMMA_overhangs, name="EMMA")
oh.write_overhangset_report("set_report_EMMA.pdf", overhangset)

ecoflex_level_1 = ["ATCT", "TGCC", "CCGG", "GAAG", "CTTC", "TTAG"]
overhangset = oh.OverhangSet(overhangs=ecoflex_level_1, name="EcoFlex level 1")
oh.write_overhangset_report("set_report_ecoflex_level_1.pdf", overhangset)

ecoflex_level_2 = ["CTAT", "GTAC", "GGAC", "TCGA", "TGTT"]
overhangset = oh.OverhangSet(overhangs=ecoflex_level_2, name="EcoFlex level 2")
oh.write_overhangset_report("set_report_ecoflex_level_2.pdf", overhangset)
