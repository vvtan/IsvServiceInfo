#!/bin/bash
supervisord -c ./app.conf &
supervisorctl -c ./app.conf &
supervisorctl start app
