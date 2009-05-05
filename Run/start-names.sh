#!/bin/bash

. ~t-names/.bashrc

Z=~t-names/Zones
export PYTHONPATH=$PYTHONPATH:$Z

cd ~t-names/Run/dns

authbind --deep twistd dns \
    --pyzone $Z/twistedmatrix.com \
    --pyzone $Z/divunal.com \
    --pyzone $Z/intarweb.us \
    --pyzone $Z/ynchrono.us
