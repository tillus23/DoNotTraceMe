import subprocess, platform, os
from flask import Flask
from flask import render_template
from flask import send_from_directory
from datetime import datetime
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)


pingMaxRes = None
pingTillRes = None
lastRefresh = None

@app.route('/')
def index():
    if(pingMaxRes == None):
        pingAllMobiles()

    return render_template('template.html', pingMaxRes=pingMaxRes, pingTillRes=pingTillRes, timestamp=lastRefresh)


def pingAllMobiles():
    global pingMaxRes
    global pingTillRes
    global lastRefresh
    pingMaxRes = pingOk('192.168.0.241')
    pingTillRes = pingOk('192.168.0.220')
    now = datetime.now()
    lastRefresh = now.strftime("%d.%m.%Y, %H:%M:%S")

def pingOk(sHost):
    try:
        subprocess.check_output("ping -{} 1 {}".format('n' if platform.system().lower()=="windows" else 'c', sHost), shell=True)
    except Exception:
        return False

    return True


scheduler = BackgroundScheduler()
scheduler.add_job(func=pingAllMobiles, trigger="interval", seconds=60)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

app.run(host='0.0.0.0', port=8080, debug=True)