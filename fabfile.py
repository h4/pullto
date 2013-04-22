# coding = utf-8

from __future__ import with_statement
import fabric.api as fabric

fabric.env.hosts = ['home.brnv.ru']
fabric.env.user = 'h4'
fabric.env.key_filename = '~/.ssh/id_rsa'


def deploy():
    project_dir = '/tmp/pullto'
    with fabric.cd(project_dir):
        fabric.run("touch test.md")
