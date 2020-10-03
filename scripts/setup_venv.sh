#!/bin/bash

set -e

# Sets up a python virtual environment with all python dependencies installed
function setup_python_venv {
    local VENV_PATH=$1

    mkdir -p ${VENV_PATH}

    virtualenv --python=python3 ${VENV_PATH}

    # activate venv and install requirements
    source ${VENV_PATH}/bin/activate

    pip3 install --upgrade pip
    pip3 install -r ${ROOT_DIR}/requirements.txt

    deactivate

    PYTHON_ROOT=${ROOT_DIR}/python
    echo "export PYTHONPATH=${PYTHON_ROOT}" >> ${VENV_PATH}/bin/activate
}


ROOT_DIR="$PWD"
VENV_PATH=${ROOT_DIR}/artifacts/venv

setup_python_venv ${VENV_PATH}
