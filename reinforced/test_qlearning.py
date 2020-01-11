import subprocess



for i in range(144):
    cmd = "python q_learning.py 50000"
    subprocess.call(cmd.split())
