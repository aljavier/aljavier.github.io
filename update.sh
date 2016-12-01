#/bin/bash
#
# This script update the branch 
# master from branch source, copying into
# it just the generated blog files.
#
# Of course, you have to commit and push after
# running this script in order to update the 
# repository on github.
#
# Customize it is needed.

git checkout source -- html && 
find html \( -name "*.html" -o -type d -name "css" -o -type d -name "images" \)  \
| xargs cp -r -t . && git rm -rf html && echo -e "\nDone!\n"

