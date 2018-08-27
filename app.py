
import json
import subprocess

from flask import Flask

app = Flask(__name__)


CMDS = {
    "ll": ["ls", "-al"],
    "x": "whoami"
}


def run_cmd(command):
    try:
        output = subprocess.check_output(command)
    except FileNotFoundError:
        output = "COMMAND NOT FOUND !"
    except subprocess.CalledProcessError as e:
        output = e.output
    except Exception as e:
        output = e.args
    return output


def cmd_filters(cmd):
    return CMDS[cmd] if cmd in CMDS else False


def handle_cmd(cmd):
    return run_cmd(CMDS.get(cmd))


@app.route('/')
def list_cmds():
    return json.dumps(CMDS)


@app.route('/<cmd>')
def api(cmd):
    if cmd_filters(cmd):
        return handle_cmd(cmd)
    else:
        return "NO CMD !"


if __name__ == '__main__':
    app.run()
