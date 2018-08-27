
import json
import subprocess

from flask import Flask

app = Flask(__name__)


CMDS = {
    "ll": ["ls", "-al"],
    "x": "whoami"
}

GROUPS = {
    "ll": ["ll", "x"]
}


def has_cmd(cmd, cmd_list):
    return True if cmd in cmd_list else False


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


def handle_cmd(cmd):
    return run_cmd(CMDS.get(cmd))


def cmd_filter(cmd):
    return has_cmd(cmd, CMDS)


def handle_cmds(cmds):
    outs = []
    for cmd in cmds:
        outs.append(handle_cmd(cmd))
    return json.dumps(outs)


def group_filter(cmd):
    return has_cmd(cmd, GROUPS)


def handle_group(cmd):
    return handle_cmds(GROUPS.get(cmd))


@app.route('/')
def list_cmds():
    return json.dumps(CMDS)


@app.route('/<cmd>')
def cmd_api(cmd):
    if cmd_filter(cmd):
        return handle_cmd(cmd)
    else:
        return "NO CMD !"


@app.route('/group/<cmd>')
def group_api(cmd):
    if group_filter(cmd):
        return handle_group(cmd)
    else:
        return "NO GROUP CMD !"


if __name__ == '__main__':
    app.run()
