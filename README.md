<p align="center">
<img alt="EGF logo" title="EGF" src="images/egf.png" width="120">
</p>


# EGF's Compendium of overhangs

**Work in progress**

Compendium of overhangs.


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


## Versioning

Overhang uses the [semantic versioning](https://semver.org) scheme.


## Copyright

Copyright 2021 Edinburgh Genome Foundry

Overhang was written at the [Edinburgh Genome Foundry](https://edinburgh-genome-foundry.github.io/)
by [Peter Vegh](https://github.com/veghp).
