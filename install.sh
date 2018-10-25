#!/usr/bin/env bash
#
#
DIR=$(cd $(dirname ${0}) && pwd)
if [[ ! -d ${DIR}/venv ]] ; then
    virtualenv -p python3.6 "${DIR}/venv"
    echo "export PYTHONPATH=${PYTHONPATH}:$DIR" >> ${DIR}/venv/bin/activate
fi
. ${DIR}/venv/bin/activate
pip install -r ${DIR}/requirements.txt
