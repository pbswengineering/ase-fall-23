#!/usr/bin/env bash

# Somehow this makes docker connections to
# the registry to work under Linux (Ubuntu 22.04),
# otherwise they'll end up with an HTTP 408 timeout.
sudo ip link set dev wlp1s0 mtu 1450
