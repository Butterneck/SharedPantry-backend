import api
import worker
import subprocess

if __name__ == '__main__':
    subprocess.call(['python', 'api.py'])
    subprocess.call(['python', 'worker'])