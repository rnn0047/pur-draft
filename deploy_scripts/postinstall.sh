#!/bin/bash

#at this time expect install by codedeploy has copied all foles to pur-draft folder
export PROJ_LOC=tiger-styles
export PROJ_ROOT=$HOME/$PROJ_LOC
cd $PROJ_ROOT
export MODELDIR=$PROJ_ROOT/xform
export PYTHONPATH=$PROJ_ROOT:$PROJ_ROOT/xform:$PROJ_ROOT/tools:$PROJ_ROOT/xform/src
#python3 -m pip install -r requirements.txt
#python3 -m pip install gunicorn
