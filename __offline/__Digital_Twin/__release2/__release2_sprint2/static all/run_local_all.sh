#!/usr/bin/env bash

export PYTHONPATH=../../common/python:.

# Populate cfg/follower.ini with agent credentials

# Docker-friendly run method
if [[ $1 == '--storeutil' ]]; then
    export STOREUTIL_HOSTING=local
    export STOREUTIL_LOCALPATH=cfg

    # These can be fixed, or set at build/run time for a particular environment. Note: For local storage blobs are just
    # files so exploiting that here.
    export IOTIC_INTEGRATOR_CFG=integrator.cfg.yml
    export IOTIC_INTEGRATOR_LOG_CFG=integrator.log.yml
    export IOTIC_INTEGRATOR_AGENT_INI=integrator.ini

    ARGS=(--log-cfg IOTIC_INTEGRATOR_LOG_CFG IOTIC_INTEGRATOR_CFG IOTIC_INTEGRATOR_AGENT_INI)
# Simple/legacy argument method
else
    ARGS=(--log-cfg cfg/integrator.log.yml cfg/integrator.cfg.yml cfg/integrator.ini)
fi


rrps-dt-integrator-sapmasterdata "${ARGS[@]}" "$@"
