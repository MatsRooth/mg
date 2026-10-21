"""Install %cat, !command and %%bash in the active Prolog kernel environment."""
from importlib.util import find_spec
from pathlib import Path


def install():
    spec = find_spec('prolog_kernel')
    if spec is None or spec.origin is None:
        raise SystemExit('Install prolog_kernel in the active environment first.')
    package = Path(spec.origin).parent
    target = package / 'kernel.py'
    source = target.read_text(encoding='utf-8')
    marker = '        return self.active_kernel_implementation.do_execute(code, silent, store_history, user_expressions, allow_stdin)'
    hook = '''        # mg notebook magics
        from prolog_kernel.notebook_magics import execute_magic
        reply = execute_magic(self, code, silent)
        if reply is not None:
            return reply
'''
    if '# mg notebook magics' not in source:
        if source.count(marker) != 1:
            raise SystemExit('Unrecognized kernel version; no files changed.')
        updated = source.replace(marker, hook + marker)
    else:
        updated = source
    updated = updated.replace(
        'def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):',
        'def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False, **kwargs):')
    helper = Path(__file__).with_name('notebook_magics.py').read_text(encoding='utf-8')
    compile(updated, str(target), 'exec')
    compile(helper, 'notebook_magics.py', 'exec')
    backup = target.with_suffix('.py.before-notebook-magics')
    if not backup.exists():
        backup.write_text(source, encoding='utf-8')
    (package / 'notebook_magics.py').write_text(helper, encoding='utf-8')
    target.write_text(updated, encoding='utf-8')
    print('Installed notebook magics. Restart existing Prolog notebook kernels.')


if __name__ == '__main__':
    install()
