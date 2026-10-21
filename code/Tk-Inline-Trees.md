# Inline trees using the original Tcl/Tk renderer

This optional helper reuses the Johnson/Stabler layout and the original Tk drawing commands. It creates a hidden canvas, exports the full tree to PostScript, converts it to a 144-dpi PNG, and embeds the PNG in notebook output. Intermediate files are removed. The saved notebook contains the image bytes, so readers do not need the temporary files or Tk to view existing output.

## Setup

Install Tcl/Tk (`wish`) and Ghostscript (`gs`). Both executables must be on the PATH inherited by Jupyter. This has been tested on macOS with MacPorts executables in `/opt/local/bin`. Apple’s system `/usr/bin/wish` failed during testing. Linux needs a graphical session (or a configured virtual display). Windows has not been tested; Ghostscript may need a launcher named `gs`.

From the repository root, in the notebook's conda environment:

```sh
conda activate prolog
python code/install_inline_images.py
export PATH="/opt/local/bin:$PATH"  # MacPorts example
jupyter lab
```

The installer extends the installed `prolog_kernel` PNG response handling and keeps a `.py.before-inline-png` backup. It is idempotent. Reinstalling the kernel package can overwrite the extension; rerun the installer afterward. **Restart existing Prolog notebook kernels after installation.**

## Notebook use

For a notebook in `notebook/`, run:

```prolog
:- consult('../code/mgcky-swi/setup.pl').
:- consult('../code/tk_inline_tree.pl').
```

Then:

```prolog
once(parse(['Titus',will,'-s',laugh], 'C', D)),
lparse(D, _, _, X, _, _),
tk_inline_tree(X).
```

The existing `inline_tree/1` Graphviz helper and `wish_tree/1` popup remain available.

## Export or inspect separately

To keep a PNG (relative to the kernel's working directory):

```prolog
once(parse(['Titus',will,'-s',laugh], 'C', D)),
lparse(D, _, _, X, _, _),
tk_tree_png(X, 'img/titus-will-s-laugh.png').
```

The `img/` directory must exist; an existing output file is overwritten. `tk_tree_script(X, Script)` returns the Tcl drawing program as a Prolog string. The exported tree includes the entire canvas content, even for trees larger than the original popup window.

This implementation requires Tk and Ghostscript to generate new images. It uses an internal response interface of the current Prolog Jupyter kernel. Local validation checked actual PNG output through a fresh Jupyter kernel; no existing lecture notebook was modified.
