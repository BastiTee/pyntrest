#!/bin/bash

list_unwanted_files () {
    git status --ignored -s | grep -e "^!!" | sed -e "s/^!! //g" |\
    grep -v -e "^\\." -e "\\.py$"
}

no_files=$( list_unwanted_files | wc -l )
[ $no_files == 0 ] && { echo "Nothing to do."; exit 0; }
list_unwanted_files

echo 
read -p "Are you sure you want to delete these files? (y/n) " -n 1 -r
echo "" # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    list_unwanted_files | while read file;
    do
        rm -rf $file
    done
else
    exit 0
fi
