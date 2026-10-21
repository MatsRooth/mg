# File display and Bash cells

Install from the repository root in the Prolog conda environment:

```sh
conda activate prolog
python code/install_notebook_magics.py
```

Restart existing notebook kernels. The installer keeps a `kernel.py.before-notebook-magics` backup and can be rerun after reinstalling/updating `prolog_kernel`. Keep `notebook_magics.py` beside the installer.

Display a UTF-8 text file (relative to the notebook's starting directory):

```text
%cat ../grammar/gh6.pl
```

Use `%cat -n "path with spaces.pl"` for line numbers. `%%cat` is an alias; put the filename on the same line and leave the rest of the cell empty. Output is plain text and is saved with notebook output.

Run a single Bash command:

```text
!ls ../grammar
```

Run a script:

```bash
%%bash
for file in ../grammar/*.pl; do
    echo "$file"
done
```

Bash must be on PATH (on Windows, install Git Bash). Commands inherit the kernel environment and run in its starting directory. Each shell cell starts a new Bash process; `cd` and environment assignments do not persist between cells. A Prolog `working_directory/2` change affects the separate Prolog process, not these commands. Use `cd directory && command` in a shell cell when needed.

Standard output and standard error appear when the command finishes. A nonzero exit status makes the cell fail. Interactive terminal input is unavailable. Interrupting a running shell command stops its process group on macOS/Linux.

Shell cells occupy the whole cell; keep Prolog in separate cells. Standalone Prolog cuts (`!`, `!.`, `!, ...`) retain their Prolog meaning. Ordinary Prolog comment cells are unaffected; `%cat` and `%%bash` are reserved commands.
