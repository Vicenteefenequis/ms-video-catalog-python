#!/bin/bash

pdm install

eval "$(pdm --pep582)"

tailf -f /dev/null