import subprocess


# examples of how to execute git commands via python script
subprocess.call(["git", "add", "test.txt"])
subprocess.call(["git", "commit", "-m", "commit message test"])
subprocess.call(["git", "push", "origin", "master"])


