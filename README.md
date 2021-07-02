<p align="center">
<img alt="EGF logo" title="EGF" src="images/egf.png" width="120">
</p>


# EGF's Compendium of overhangs

[![build](https://github.com/Edinburgh-Genome-Foundry/Overhang/actions/workflows/build.yml/badge.svg)](https://github.com/Edinburgh-Genome-Foundry/Overhang/actions/workflows/build.yml)


This Python package generates a description of an input set DNA overhangs and outputs a PDF file.
Additionally it evaluates suitability of an input set of overhangs for Golden Gate DNA assembly.


## Install

```
# pip install overhang
pip install --upgrade git+https://github.com/Edinburgh-Genome-Foundry/overhang.git@main
```


## Usage

```python
import overhang as oh

overhang = oh.Overhang("TCAT")
dir(overhang)

overhang_classes = oh.generate_all_overhangs()
oh.write_pdf_report(target="examples/compendium.pdf", overhangs=overhang_classes)
```

Inspect a set of overhangs for assembly:
```python
overhangset = oh.OverhangSet(
    overhangs=["ATGG", "GAAA", "CACC", "GACT", "ATGG", "CCAG",], name="Example",
)
oh.write_overhangset_report("examples/set_report_Example.pdf", overhangset)
# Esp3I Tatapov plot (37 Celsius, 1 hour):
```
<p align="center">
<img alt="EGF logo" title="EGF" src="images/plot.png" width="300">
</p>


## Versioning

Overhang uses the [semantic versioning](https://semver.org) scheme.


## Copyright

Copyright 2021 Edinburgh Genome Foundry

Overhang was written at the [Edinburgh Genome Foundry](https://edinburgh-genome-foundry.github.io/)
by [Peter Vegh](https://github.com/veghp).
