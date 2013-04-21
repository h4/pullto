# coding = utf-8
import os
import json
import subprocess
from hashlib import sha256
from bottle import request, abort, Bottle

settings_module = os.environ.get('PULLTO_SETTINGS_MODULE')

settings = __import__(settings_module)

app = Bottle()


def log(message):
    print message


def check_auth(auth_header, user=settings.GITHUB_USER, repo=settings.GITHUB_REPO, token=settings.TRAVIS_TOKEN):
    checksum = sha256(user + '/' + repo + token).hexdigest()
    return checksum == auth_header


def verify_status(payload, repository=settings.REPOSITORY_URL):
    return payload['repository']['url'] == repository and payload['result'] == 0


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
    branch_dir = settings.BRANCH_DIRS[branch_name] if branch_name in settings.BRANCH_DIRS else settings.STAGING_DIR

    validate_working_copy(branch_dir, settings.REPOSITORY_URL)

    run_shell_commands(settings.BEFORE_DEPLOY)

    try:
        subprocess.check_call(['git', 'fetch'])
        subprocess.check_call(['git', 'checkout', branch_name])
        subprocess.check_call(['git', 'pull'])
    except subprocess.CalledProcessError, e:
        log(e)

    run_shell_commands(settings.AFTER_DEPLOY)


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
    os.environ.setdefault("PULLTO_SETTINGS_MODULE", "settings")
    if settings.DEBUG:
        app.run(host='0.0.0.0', port=8080, reloader=True)
    else:
        if settings.LISTEN_TO == 'socket':
            app.run(server='flup', bindAddress=settings.SOCKET)
        else:
            # I'm not sure, that it's works
            app.run(server='flup', bindAddress='{0}:{1}'.format(settings.HTTP_HOST, settings.HTTP_PORT))
