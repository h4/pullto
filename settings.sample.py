# coding = utf-8

DEBUG = True

TRAVIS_TOKEN = 'yourTravisToken'

GITHUB_USER = 'h4'

GITHUB_REPO = 'pullto'

REPOSITORY_URL = "https://github.com/h4/pullto"

BRANCHES_DIRS = {
    'master': 'PATH_TO_DIR_FOR_MASTER',
    'develop': 'PATH_TO_DIR_FOR_DEVELOP'
}

STAGING_DIR = 'PATH_TO_DIR_FOR_UNMAPPED_BRANCHES'

BEFORE_DEPLOY = [
    'service nginx stop',
]

AFTER_DEPLOY = [
    'service nginx start',
]
