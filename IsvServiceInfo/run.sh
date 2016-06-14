#!/bin/bash
sudo supervisord -c ./app.conf &
sudo supervisorctl start app
