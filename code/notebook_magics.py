"""File display and Bash cells for prolog_kernel (installed by installer)."""
import os
from pathlib import Path
import shlex
import shutil
import signal
import subprocess


def execute_magic(kernel, code, silent):
    """Return None for Prolog cells, otherwise a Jupyter execute reply."""
    source = code.lstrip()
    header, _, body = source.partition('\n')
    command = header.split(maxsplit=1)[0] if header.strip() else ''
    file_magic = command in ('%cat', '%%cat')
    bash_magic = command == '%%bash'
    # Preserve standalone Prolog cut and cut followed by a comma/period.
    shell_magic = source.startswith('!') and source[1:].lstrip()[:1] not in ('', '.', ',')
    if not (file_magic or bash_magic or shell_magic):
        return None

    def emit(kind, content):
        if not silent:
            kernel.send_response(kernel.iopub_socket, kind, content)

    def error(name, message):
        content = dict(ename=name, evalue=message, traceback=[])
        emit('error', content)
        return dict(status='error', execution_count=kernel.execution_count, **content)

    try:
        if file_magic:
            if body.strip():
                raise ValueError('File display cells accept only a filename on the first line.')
            args = shlex.split(header[len(command):], posix=True)
            numbered = bool(args and args[0] == '-n')
            if numbered:
                args.pop(0)
            if args[:1] == ['--']:
                args.pop(0)
            if len(args) != 1:
                raise ValueError('Usage: %cat [-n] [--] "path/to/file" (or %%cat)')
            text = Path(args[0]).expanduser().read_text(encoding='utf-8')
            if numbered:
                text = '\n'.join(f'{i:4}  {line}' for i, line in enumerate(text.splitlines(), 1))
            emit('display_data', dict(data={'text/plain': text}, metadata={}))
        else:
            if bash_magic:
                if header[len(command):].strip():
                    raise ValueError('Usage: %%bash followed by a script on subsequent lines.')
                script = body
            else:
                if body.strip():
                    raise ValueError('Use %%bash for a multi-line shell script.')
                script = header[1:]
            bash = shutil.which('bash')
            if bash is None:
                raise FileNotFoundError('Bash is not on PATH. Install Bash (Git Bash on Windows).')
            proc = subprocess.Popen(
                [bash, '-c', script], stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True, encoding='utf-8', errors='replace',
                start_new_session=(os.name == 'posix'))
            try:
                stdout, stderr = proc.communicate()
            except BaseException:
                if os.name == 'posix':
                    os.killpg(proc.pid, signal.SIGKILL)
                else:
                    proc.kill()
                proc.communicate()
                raise
            if stdout:
                emit('stream', dict(name='stdout', text=stdout))
            if stderr:
                emit('stream', dict(name='stderr', text=stderr))
            if proc.returncode:
                return error('ShellCommandError', f'Bash exited with status {proc.returncode}')
    except KeyboardInterrupt:
        return error('KeyboardInterrupt', 'Shell command interrupted')
    except (OSError, ValueError) as exc:
        return error(type(exc).__name__, str(exc))
    return dict(status='ok', execution_count=kernel.execution_count,
                payload=[], user_expressions={})
