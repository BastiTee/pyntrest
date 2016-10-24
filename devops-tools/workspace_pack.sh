#!/bin/bash

out_zip="pyntrest_deploy-HEAD.tar"
spath=$( readlink -f $( dirname $0 ))
echo $spath

echo "Cleaning workspace first ... "
echo 
${spath}/workspace_reset.sh

echo "Packing content ... "

tar -cvf $out_zip \
devops-tools/*.example \
pyntrest/ \
pyntrest_project/ \
pyntrest_tests/ \
LICENSE \
manage.py \
README.md \
requirements.txt \
--exclude pyntrest/pyntrest_config.py

echo "Packing successful ..." 
