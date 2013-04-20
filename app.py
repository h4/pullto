# coding = utf-8

import json
import subprocess
import os
from hashlib import sha256
from bottle import request, abort, Bottle
from settings import *

app = Bottle()


def log(message):
    print message


def check_auth(auth_header):
    checksum = sha256(GITHUB_USER + '/' + GITHUB_REPO + TRAVIS_TOKEN).hexdigest()
    return checksum == auth_header


def verify_status(payload):
    return payload['repository']['url'] == REPOSITORY_URL and payload['result'] == 0


def run_shell_commands(stack):
    for command in stack:
        try:
            subprocess.check_call(command)
        except subprocess.CalledProcessError, e:
            log(e)


def validate_working_copy(path, repository):
    if not os.path.exists(path):
        os.mkdir(path, 0775)
    os.chdir(path)
    try:
        subprocess.check_call(['git', 'status'])
    except subprocess.CalledProcessError:
        subprocess.call(['git', 'clone', '--depth', '1', repository, path])


def deploy(branch_name):
    branch_dir = BRANCH_DIRS[branch_name] if branch_name in BRANCH_DIRS else STAGING_DIR

    validate_working_copy(branch_dir, REPOSITORY_URL)

    run_shell_commands(BEFORE_DEPLOY)

    try:
        subprocess.check_call(['git', 'fetch'])
        subprocess.check_call(['git', 'checkout', branch_name])
        subprocess.check_call(['git', 'pull'])
    except subprocess.CalledProcessError, e:
        log(e)

    run_shell_commands(AFTER_DEPLOY)


@app.route('/', method='GET')
def reject():
    abort(400, 'Bad request')


@app.route('/', method='POST')
def index():
    if not check_auth(request.get_header('Authorization')):
        abort(401, 'Unauthorized')
    travis_payload = json.loads(request.POST.get('payload'))

    if not verify_status(travis_payload):
        abort(400, 'Bad request')

    branch = travis_payload['branch']

    try:
        deploy(branch)
        return '<b>Ok!</p>'
    except Exception, e:
        log(e)
        abort(500, 'Deploy error')


if __name__ == '__main__':
    if DEBUG:
        app.run(host='0.0.0.0', port=8080, reloader=True)
    else:
        if LISTEN_TO == 'socket':
            app.run(server='flup', bindAddress=SOCKET)
        else:
            # I'm not sure, that it's works
            app.run(server='flup', bindAddress='{0}:{1}'.format(HTTP_HOST, HTTP_PORT))
