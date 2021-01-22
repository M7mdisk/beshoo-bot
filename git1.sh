#!/bin/sh
cd ~/Documents/Github/min-bot

echo "adding..."

git add .

echo "--------------------"

echo "commiting..."

DATE=$(date)
git commit -m "Changes have been made on $DATE"

echo "--------------------"

echo "pushing..."

git push -u


echo "--------------------"

echo "Done.."
