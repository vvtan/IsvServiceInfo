#!/bin/bash
sudo service supervisor start -c ./app.conf &
sudo supervisorctl start app
