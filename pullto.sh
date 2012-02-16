#!/bin/bash

dir="/var/www/dev/moodle/theme/spbspu"

echo 'Content-Type: text/html'
echo
echo '<html/>'

exec > /tmp/GIT.log.$$
cd $dir  && git pull
