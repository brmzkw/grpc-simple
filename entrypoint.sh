#!/bin/sh

poetry install
. $(poetry env info -p)/bin/activate
exec "$@"
