#!/bin/bash

if [[ $# -ne 1 ]]; then
    echo "Error: provide your email address!"
    exit 1
fi

ssh-keygen -t ed25519 -C $1



