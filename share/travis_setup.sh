#!/bin/bash
set -evx

mkdir ~/.poliscore

# safety check
if [ ! -f ~/.poliscore/.polis.conf ]; then
  cp share/polis.conf.example ~/.poliscore/polis.conf
fi
