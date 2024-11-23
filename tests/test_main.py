import subprocess
import sys

def test_output():

    args = [sys.executable, '-m', "hyper_tokuma"]
    result = subprocess.run(args,capture_output=True, check=True)

    assert result.stdout
