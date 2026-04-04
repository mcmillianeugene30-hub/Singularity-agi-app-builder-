#!/usr/bin/env bash
set -e
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
# Source cargo environment to make tools available
source $HOME/.cargo/env
