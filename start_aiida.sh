#!/usr/bin/env bash

if [[ $1 ]]; then n=$1; else n=1; fi

sudo service postgresql start
sudo service rabbitmq-server start

verdi daemon start $n
verdi status

# activate autocompletion for aiida-quanumespresso
eval "$(_AIIDA_QUANTUMESPRESSO_COMPLETE=bash_source aiida-quantumespresso)"
