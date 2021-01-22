#!/bin/sh
cd ~/Documents/Github/min-bot

echo "adding..."\n

git add .

echo "--------------------"

echo "commiting..."\n

DATE=$(date)
git commit -m "Changes have been made on $DATE"

echo "--------------------"

echo "pushhing..."\n

git push -u


echo "--------------------"

echo "Done.."
