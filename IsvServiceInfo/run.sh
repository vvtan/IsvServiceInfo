#!/bin/bash
sudo service supervisor start &
sudo supervisorctl start app
