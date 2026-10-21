"""Exercise the extension through a real, fresh Jupyter Prolog kernel."""
from pathlib import Path
from tempfile import TemporaryDirectory
from jupyter_client import KernelManager

helper = str(Path(__file__).with_name('notebook_magics.py').resolve())
bootstrap = '''
import importlib.util
from ipykernel.kernelapp import IPKernelApp
from prolog_kernel.kernel import PrologKernel
spec = importlib.util.spec_from_file_location('mg_magics', HELPER)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
original = PrologKernel.do_execute
def execute(self, code, silent, *args, **kwargs):
    result = m.execute_magic(self, code, silent)
    return original(self, code, silent, *args, **{k:v for k,v in kwargs.items() if k in ('store_history', 'user_expressions', 'allow_stdin')}) if result is None else result
PrologKernel.do_execute = execute
IPKernelApp.launch_instance(kernel_class=PrologKernel)
'''.replace('HELPER', repr(helper))
with TemporaryDirectory() as directory:
    Path(directory, 'a file.pl').write_text('hello\nworld\n')
    km = KernelManager(kernel_name='prolog')
    from jupyter_client.kernelspec import KernelSpec
    km._kernel_spec = KernelSpec(display_name='Prolog test', language='prolog')
    km.kernel_spec.argv = [__import__('sys').executable, '-c', bootstrap, '-f', '{connection_file}']
    km.start_kernel(cwd=directory)
    client = km.client()
    client.start_channels()
    try:
        client.wait_for_ready(timeout=30)
        def run(code, silent=False):
            msgid = client.execute(code, silent=silent)
            outputs = []
            while True:
                msg = client.get_iopub_msg(timeout=30)
                if msg['parent_header'].get('msg_id') != msgid:
                    continue
                if msg['msg_type'] == 'status' and msg['content']['execution_state'] == 'idle':
                    break
                outputs.append((msg['msg_type'], msg['content']))
            while True:
                reply = client.get_shell_msg(timeout=30)
                if reply['parent_header'].get('msg_id') == msgid:
                    return reply['content'], outputs
        reply, output = run('%cat -n "a file.pl"')
        assert reply['status'] == 'ok' and any('   2  world' in str(o) for o in output)
        assert run('%%cat "a file.pl"')[0]['status'] == 'ok'
        reply, output = run('!printf hello; printf error >&2; exit 7')
        assert reply['status'] == 'error' and '7' in reply['evalue']
        assert {o['name'] for t, o in output if t == 'stream'} == {'stdout', 'stderr'}
        assert run('%%bash\nx=world\nprintf "$x"')[0]['status'] == 'ok'
        assert run('%cat missing.pl')[0]['status'] == 'error'
        assert run('%cat')[0]['status'] == 'error'
        assert run('!echo hello\necho world')[0]['status'] == 'error'
        reply, output = run('!echo hidden', silent=True)
        assert reply['status'] == 'ok' and not any(t in ('stream', 'display_data', 'error') for t, o in output)
        assert run('member(X, [hello, world]).')[0]['status'] == 'ok'
        assert run('!.')[0]['status'] == 'ok'
        assert run('% ordinary comment\ntrue.')[0]['status'] == 'ok'
        print('PASS: file display, numbering, aliases, Bash, stderr, failures, silent execution, Prolog and cut')
    finally:
        client.stop_channels()
        km.shutdown_kernel(now=True)
