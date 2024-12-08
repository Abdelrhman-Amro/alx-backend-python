#!/bin/bash

# setup.sh - set up virtual environment and install dependencies

# create venv if it doesn't already exist
if [ ! -d venv ]
then
    python3 -m venv venv
fi

# shellcheck source=/dev/null  # don't check venv activate script
source venv/bin/activate

pip install -r requirements.txt
