#!/bin/bash

cd /home/ec2-user
sudo yum -y update
sudo yum -y install python36
sudo yum -y install nginx
#mkdir /home/ec2-user/tiger-styles
export PROJ_LOC=tiger-styles
mkdir $HOME/$PROJ_LOC
