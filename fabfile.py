# coding = utf-8

from __future__ import with_statement
import fabric.api as fabric

fabric.env.hosts = ['brnv.ru']
fabric.env.user = 'h4'
fabric.env.key_filename = '~/travis'
fabric.env.disable_known_hosts = True
fabric.env.use_ssh_config = True
fabric.env.ssh_config_path = './ssh_config'
fabric.env.no_keys = True


def deploy():
    project_dir = '/tmp'
    with fabric.cd(project_dir):
        fabric.run("touch test.md")
