#!/bin/bash

# actions
gitdo_actions=("push" "pull" "help")

# help manual
if [ $# -lt 1 ] || [[ "$1" == "help" || "$1" == "--help" || "$1" == "-h" ]]; then
    cat <<EOF
gitdo.sh - manage multiple remote locations at once.
Usage: $0 <action> remote1 remote2 ..."
    action: ${gitdo_actions[@]}

Example: ./gitdo.sh push github gitlab codeberg
EOF
    exit 0
fi

# define contains function
contains() {
    local array="$1[@]"
    local value="$2"
    for item in "${!array}"; do
        if [[ "$item" == "$value" ]]; then
            return 0 # found
        fi
    done
    return 1 # not found
}

# check for invalid arguments
if contains gitdo_actions $1; then
    # capture remote arguments
    gitdo_remote_locations=("${@:2}")
    if [ ${#gitdo_remote_locations[@]} -lt 1 ]; then
        echo "No remote locations specified!"
        exit 1
    fi

    # execute action
    for name in "${gitdo_remote_locations[@]}"; do
        echo "Execute: git $1 $name"
        git $1 $name

        # check exit status of the previous operation
        if [ $? -ne 0 ]; then
            echo "Error occured! Exit."
            exit 1
        fi
    done
else
    echo "Invalid argument: $1"
    exit 1
fi
