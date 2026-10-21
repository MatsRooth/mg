"""Enable embedded PNG responses in prolog_kernel. Restart kernels afterward."""
from importlib.util import find_spec
from pathlib import Path

spec = find_spec('prolog_kernel')
if spec is None or spec.origin is None:
    raise SystemExit('Install prolog_kernel in the active environment first.')
p = Path(spec.origin).parent / 'prolog_kernel_base_implementation.py'
s = p.read_text(encoding='utf-8')
marker = "        failure_keys = []\n"
addition = '''
        # mg inline PNG support: data is base64, embedded in the saved notebook.
        if 'inline_png' in dict:
            self.kernel.send_response(self.kernel.iopub_socket, 'display_data', {
                'data': {'image/png': dict['inline_png'], 'text/plain': 'Syntax tree'},
                'metadata': {}})
'''
if '# mg inline PNG support' in s:
    print('Inline PNG support is already installed.')
else:
    if s.count(marker) != 1:
        raise SystemExit('Unrecognized kernel version; no files changed.')
    updated = s.replace(marker, marker + addition)
    compile(updated, str(p), 'exec')
    backup = p.with_suffix('.py.before-inline-png')
    if not backup.exists():
        backup.write_text(s, encoding='utf-8')
    p.write_text(updated, encoding='utf-8')
    print('Installed inline PNG support. Restart the Prolog notebook kernel.')
