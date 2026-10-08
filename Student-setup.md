# Minimalist parsing in CL1: setup

We will run Edward Stabler's minimalist grammar parser in SWI-Prolog, using a Jupyter notebook. You can enter sentences, inspect derivations, and draw syntax trees. This is a separate environment from our Python parser exercises.

## 1. Get the course files

Open [the mg repository](https://github.com/MatsRooth/mg). Choose **Code → Download ZIP**, unzip it, and put the folder somewhere convenient. Git users can instead run:

```sh
git clone https://github.com/MatsRooth/mg.git
cd mg
```

The commands below assume your terminal is in the downloaded repository folder. For the ZIP download it may be named `mg-main`.

## 2. Install SWI-Prolog

Use the [official SWI-Prolog downloads](https://www.swi-prolog.org/download/stable):

- **Windows:** use the 64-bit Windows installer. Make sure its executable directory is on your PATH.
- **macOS:** use the macOS application bundle, or a package manager if you already use one. Both Intel and Apple Silicon bundles are available.
- **Linux:** use your distribution's SWI-Prolog package.

In a terminal, check:

```sh
swipl --version
```

If the command is not found, add the directory containing `swipl` to your PATH and reopen the terminal. On Windows the executable is `swipl.exe`. On macOS with MacPorts, for example:

```sh
export PATH="/opt/local/bin:$PATH"
```

That MacPorts path is an example, not a requirement. Keep using this terminal to launch Jupyter so it inherits the working PATH.

## 3. Create the notebook environment

If you already use conda for class, use the same conda installation. Otherwise install [Miniforge](https://github.com/conda-forge/miniforge), then open a terminal with conda available. On Windows, a Miniforge/conda prompt is convenient.

```sh
conda create -n prolog -c conda-forge python=3.12 pip jupyterlab graphviz
conda activate prolog
python -m pip install prolog_kernel
python -m prolog_kernel.install --user
python code/fix_prolog_kernel.py
```

The last command applies a small compatibility fix to the installed kernel and keeps a backup. We needed it with SWI-Prolog 9.2.9; it handles the error `Unknown procedure: toplevel_variables:expand_query/4`. It does not change SWI-Prolog or the grammar.

Check that both commands are available in this environment:

```sh
swipl --version
dot -V
```

Graphviz (`dot`) is used for inline tree images. You do not need LaTeX, Ghostscript, or Tcl/Tk for the initial notebook exercise.

## 4. Start Jupyter and test Prolog

From the repository folder:

```sh
conda activate prolog
jupyter lab
```

Create a notebook with the **Prolog** kernel. Enter this in a code cell and press **Shift+Enter**:

```prolog
member(X, [mommy, likes, cookies]).
```

Expect `X = mommy`. In another cell:

```prolog
jupyter:retry.
```

Further retries produce `likes`, then `cookies`, then `false`. This is Prolog exploring the alternatives.

Do not type the terminal prompt `?-` in notebook cells. End Prolog statements with a period.

## 5. Load the parser

The course parser files are in `code/mgcky-swi/`. In Jupyter, open the `notebooks/` folder and create or open your Prolog notebook there. Run:

```prolog
:- consult('../code/mgcky-swi/setup.pl').
:- consult('../code/mgcky-swi/grammars/gh6.pl').
:- consult('../code/inline_tree.pl').
```

The `:-` prefixes tell the notebook these are instructions to execute. Without them, multiple calls in one cell can be mistaken for predicate definitions.

This exercise uses the extended parser pair `mghapx` and `lhapx`, with grammar `gh6`. The distributed `setup.pl` must select that pair and `gh6` as its sole grammar.

Some original source files produce loading warnings. A warning alone does not mean loading failed; an `ERROR` needs attention.

## 6. Parse a sentence and draw its tree

```prolog
once(parse([the,king,laugh,'-s'], 'C', D)),
lparse(D, _, _, X, _, _),
inline_tree(X).
```

You should see an acceptance message, a derivation, and an inline syntax tree. The parser's input represents morphology as separate tokens: `laugh` plus `'-s'` corresponds to *laughs*.

Try these as well:

```prolog
parse([the,king,will,'-s',laugh], 'C', D).
```

```prolog
parse(['Titus',be,'-s',laugh,'-ing'], 'C', D).
```

```prolog
parse(['Titus',have,'-s',been,laugh,'-ing'], 'C', D).
```

Capitalized words and hyphenated suffixes need quotes. `'C'` is the grammar's sentence category. `D` is the sequence of lexical-entry numbers used in a derivation; these numbers depend on the loaded grammar.

## Optional: the Tcl/Tk tree popup

If Tcl/Tk is installed and `wish` is on the Jupyter server's PATH, a locally running notebook can open the original tree viewer:

```prolog
once(parse([the,king,laugh,'-s'], 'C', D)),
lparse(D, _, _, X, _, _),
wish_tree(X).
```

Its **dump ps** button saves `ltree.ps` in Prolog's working directory. This older launcher was tested on the instructor's Mac; it may need adjustment on Windows. It is optional. Use `inline_tree/1` for the initial exercise.

Avoid `showParse/1` in notebooks: it asks for terminal input to choose display options.

## Troubleshooting

- **`Unknown procedure: parse/3`:** run the loading cell again. Restarting a kernel clears its loaded programs.
- **“Asserting clauses for user:consult/1”:** restart the kernel, then use the loading cell with `:-` prefixes.
- **`toplevel_variables:expand_query/4` error:** activate `prolog`, run `python code/fix_prolog_kernel.py`, and restart the notebook kernel.
- **Graphviz cannot find `dot`:** activate `prolog` and check `dot -V` before launching Jupyter.
- **A source file cannot be found:** check the notebook's working directory with `working_directory(Dir, Dir).` For the loading cell above it should be the `notebooks/` folder. Run terminal setup commands from the repository root.
- **No Prolog kernel is listed:** run `python -m prolog_kernel.install --user` from the `prolog` environment, then restart Jupyter.

## Instructor validation before release

The parser is bundled in `code/mgcky-swi/` and configured for `mghapx`, `lhapx`, and `gh6`. The kernel compatibility script is included in `code/`.

The terminal parser and inline conversion have been checked on the instructor's Mac. Before assigning the setup, test the complete sequence in a fresh environment and notebook, including on Windows. The inline helper uses an internal kernel display interface, so validate the kernel version used for class.
