import subprocess

def test_cli_help():
    result = subprocess.run(["python", "-m", "hercules.cli", "--help"], capture_output=True)
    assert result.returncode == 0
    assert "HERCULES" in result.stdout.decode()
