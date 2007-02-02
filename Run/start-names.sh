#!/bin/bash

Z=$HOME/Zones
PYTHONPATH=$PYTHONPATH:$Z

cd $HOME/Run/dns

authbind --deep twistd dns \
    --pyzone $Z/twistedmatrix.com \
    --pyzone $Z/divunal.com \
    --pyzone $Z/intarweb.us \
    --pyzone $Z/ynchrono.us
