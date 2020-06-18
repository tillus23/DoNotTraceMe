import subprocess, platform, os
from flask import Flask
from flask import render_template
from flask import send_from_directory
from datetime import datetime
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

class PingDevice:
    def __init__(self, name, ip):
        self.name = name
        self.ip = ip
        self.lastSeen = None
        self.status = None
        self.lastRefresh = None
    
    def ping(self):
        now = datetime.now()
        self.lastRefresh = now.strftime("%d.%m.%Y, %H:%M:%S")

        try:
            subprocess.check_output("ping -{} 1 {}".format('n' if platform.system().lower()=="windows" else 'c', self.ip), shell=True)
            self.status = True
            self.lastSeen = self.lastRefresh
        except Exception:
            self.status = False

devicesToPing = [PingDevice('Max','192.168.0.241'), PingDevice('Till','192.168.0.220'), PingDevice('Lara','192.168.0.87')]

@app.before_first_request
def pingAllMobiles():
    for dev in devicesToPing:
        dev.ping()


@app.route('/')
def index():
    return render_template('template.html', pingDevices=devicesToPing)


def pingOk(sHost):
    try:
        subprocess.check_output("ping -{} 1 {}".format('n' if platform.system().lower()=="windows" else 'c', sHost), shell=True)
    except Exception:
        return False
    return True


if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=pingAllMobiles, trigger="interval", seconds=60)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())

    app.run(host='0.0.0.0', port=80, debug=True)