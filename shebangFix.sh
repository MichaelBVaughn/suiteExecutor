#!/bin/bash
find ../testplans.alt -name "setup*" | xargs sed -i '1 s_^.*$_#!/usr/bin/env expect -f_g'
