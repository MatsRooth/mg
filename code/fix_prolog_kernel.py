"""Compatibility fix for prolog_kernel with newer SWI-Prolog versions.
Run inside the conda prolog environment. Restart notebook kernels afterward.
"""
from importlib.util import find_spec
from pathlib import Path

spec = find_spec('prolog_kernel')
if spec is None or spec.origin is None:
    raise SystemExit('Install prolog_kernel in this environment first.')
path = Path(spec.origin).parent / 'prolog_server' / 'jupyter_term_handling.pl'
original = path.read_text(encoding='utf-8')
updated = original.replace(
    'toplevel_variables:expand_query(Term, UpdatedTerm, Bindings, UpdatedBindings)',
    'jupyter_variable_bindings:term_with_stored_var_bindings(Term, Bindings, UpdatedTerm, UpdatedBindings)',
).replace(
    'toplevel_variables:expand_answer(BindingsWithoutSingletons, _NewBindings)',
    'jupyter_variable_bindings:store_var_bindings(BindingsWithoutSingletons)',
)
if updated == original:
    print('No changes needed: obsolete calls were not found.')
else:
    backup = path.with_suffix('.pl.bak')
    if not backup.exists():
        backup.write_text(original, encoding='utf-8')
    path.write_text(updated, encoding='utf-8')
    print(f'Patched {path}\nBackup: {backup}\nRestart your notebook kernel.')
