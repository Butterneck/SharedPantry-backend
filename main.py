import api
import worker
import subprocess

if __name__ == '__main__':
    subprocess.call(['gunicorn', 'main:app'])
    subprocess.call(['python', 'worker'])