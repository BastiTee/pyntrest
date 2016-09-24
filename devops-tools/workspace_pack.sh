#!/bin/bash
out_zip="pyntrest_deploy-HEAD.tar"
rm -f $out_zip

echo "Cleaning workspace first ... "
echo 
./workspace_reset.sh

echo "Packing content ... "
tar -cvf $out_zip pyntrest/ pyntrest_project/ LICENSE manage.py \
README.md requirements.txt --exclude pyntrest/pyntrest_config.py

echo "Packing successful ..." 
