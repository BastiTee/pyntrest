#!/bin/bash
out_zip="pyntrest_deploy-HEAD.zip"
echo "Cleaning workspace first ... "
echo 
rm -f $out_zip
./workspace_reset.sh
git archive -o $out_zip HEAD
echo "Packing successful"