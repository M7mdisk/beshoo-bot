#!/bin/sh
cd ~/Documents/Github/min-bot

git add .

echo "--------------------\n"

DATE=$(date)

git commit -m "Changes have been made on $DATE"

echo "--------------------\n"

git push -u


echo "--------------------\n"

echo "Done.."
