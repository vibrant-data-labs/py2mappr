#!/bin/bash

NAME="py2map"
PORT=8000
echo running $NAME locally on port $PORT
exec python -m http.server $PORT