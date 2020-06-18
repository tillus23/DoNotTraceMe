import subprocess, platform, os
from flask import Flask
from flask import render_template
from flask import send_from_directory


app = Flask(__name__)

@app.route('/')
def hello_world():
    pingMaxRes = pingOk('192.168.0.241')
    pingTillRes = pingOk('192.168.0.220')

    return render_template('template.html', pingMaxRes=pingMaxRes, pingTillRes=pingTillRes)

def pingOk(sHost):
    try:
        subprocess.check_output("ping -{} 1 {}".format('n' if platform.system().lower()=="windows" else 'c', sHost), shell=True)
    except Exception:
        return False

    return True


app.run(host='0.0.0.0', port=8080, debug=True)