#!/bin/sh
cd ~/Documents/Github/min-bot

git add .

DATE=$(date)

git commit -m "Changes have been made on $DATE"

git push -u

echo "Done.."
