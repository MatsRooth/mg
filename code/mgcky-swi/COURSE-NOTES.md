# CL1 copy of mgcky-swi

This directory contains Edward P. Stabler's CKY-like minimalist grammar parser for SWI-Prolog. The original `readme`, GPL license (`license`), and source-file author credits are retained. The implementation also includes contributions from Willemijn Vermaat, John Hale, Mark Johnson, and the Shieber–Schabes–Pereira chart-parsing code; see individual files for attribution.

Copied from the instructor's local distribution on 2026-10-08 for CL1 teaching. This is a teaching copy, not a claim to be an untouched upstream release.

The copied `setup.pl` is configured for `mghapx`/`lhapx` and grammar `gh6`, rather than `larsonian1`. The local `gh6.pl` and `gh6.orig.pl` are both retained; the latter provides a reference copy. The optional decomposed auxiliary entry discussed in class has not been added to this teaching copy. The `tex/Makefile` builds PDFs via latex, dvips, and ps2pdf. Generated tree files, notebooks, editor backups, and temporary viewer scripts were omitted.

The parser is distributed under GNU GPL version 2 or later, as stated in the original `readme`. See `license` for the full license text.
