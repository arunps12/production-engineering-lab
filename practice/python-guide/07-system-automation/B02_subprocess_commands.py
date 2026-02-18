"""
Exercise 7.B.2 — subprocess Commands
Guide: docs/python-guide/07-system-automation-scripting.md
"""
import subprocess


def run_basic_commands():
    """Run basic system commands."""
    # TODO 1: Run 'uname -a' and capture output
    # result = subprocess.run(["uname", "-a"], capture_output=True, text=True)
    # print(f"System: {result.stdout.strip()}")

    # TODO 2: Run 'df -h' to check disk usage
    # result = subprocess.run(["df", "-h"], capture_output=True, text=True)
    # print(result.stdout)

    # TODO 3: Run a command that fails, check returncode
    # result = subprocess.run(["ls", "/nonexistent"], capture_output=True, text=True)
    # print(f"Return code: {result.returncode}")
    # print(f"Stderr: {result.stderr.strip()}")

    # TODO 4: Use check=True to raise on error
    # try:
    #     subprocess.run(["false"], check=True)
    # except subprocess.CalledProcessError as e:
    #     print(f"Command failed with code: {e.returncode}")

    # TODO 5: Pipe two commands: ps aux | grep python
    # ps = subprocess.Popen(["ps", "aux"], stdout=subprocess.PIPE)
    # grep = subprocess.Popen(["grep", "python"], stdin=ps.stdout, stdout=subprocess.PIPE, text=True)
    # ps.stdout.close()
    # output, _ = grep.communicate()
    # print(f"Python processes:\n{output}")
    pass


if __name__ == "__main__":
    run_basic_commands()
