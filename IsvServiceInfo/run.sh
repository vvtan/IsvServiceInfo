#!/bin/bash
supervisord &
supervisorctl start app
