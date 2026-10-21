# mg
Minimalist grammar materials for CL1.

## Student setup

See [Student-Setup.md](Student-Setup.md) for SWI-Prolog and Jupyter installation and a first parsing exercise.

## Parser credits

The bundled [mgcky-swi](code/mgcky-swi/) parser is Edward P. Stabler's CKY-like minimalist grammar parser, distributed under GPL version 2 or later. Original author credits and the [license](code/mgcky-swi/license) are retained. See [course notes](code/mgcky-swi/COURSE-NOTES.md) for the teaching configuration and additional contributors.

## License

This repository's original code and teaching materials are distributed under the GNU General Public License, version 2 or (at your option) any later version (SPDX: GPL-2.0-or-later). See [LICENSE](LICENSE).

Bundled third-party files retain their original copyright, attribution, and license notices. In particular, the mgcky-swi parser remains under its original GPL version 2-or-later terms. The kernel compatibility script does not relicense the separately installed Prolog Jupyter kernel.

## Repository layout

- `code/`: the bundled parser and notebook support scripts.
- `notebook/`: Prolog notebooks; their loading cells use paths beginning with `../code/` or `../grammar/`.

## Development
Design and implementation were carried out by Mats Rooth with
extensive assistance from OpenAI’s ChatGPT and Codex through an
iterative design, implementation, and code-review process.
