# 🤖 Beshoo Bot ![website](https://img.shields.io/website?down_color=red&down_message=Sleep&label=Status&up_color=Green&up_message=Awake&url=https%3A%2F%2Fdashboard.heroku.com%2Fapps%2Fbeshoo)
Beshoo is a multi-purpouse discord bot built with discord.py

The goal of the bot was simply to learn more about how to work with requests, APIs and python in general.
## Features 
* Fully modular
  * Easily remove/add any command by deleting/creating the cog or the command from `run.py`
* Admin commands like `kick`, `ban` and `mute`.
* Voice channel commands to play any youtube video.
* AI-powered image utilities like `bgremove` and `face` that work on any picture.
* fun commands like `meme`, `quote`, `dog`, `cat` and many more!
* Utility commands like `weather`, `def`.

## Usage
to invite the bot to your server use the button below

## Installation
Want to make the bot your own? follow these steps

### Locally

requirments: Python 3.7+

Simply:
```
git clone https://github.com/M7mdisk/beshoo-bot.git
cd beshoo-bot
```
install the dependencies

`pip install -r requirments.txt`

or if you want to use a virtual environment

`pipenv install`

Rename the `.env.example` file to `.env` and replace the Xs by your tokens.

Finally, run the bot.

`python3 run.py`

and you're good to go!

### Heroku
- coming soon.

## Commands

* `!help [command]`  Displays the help message. ¯\_(ツ)_/¯.
### Image proccessing
  * `!face`  Detect faces in the picture and give further info about them .
  * `!bgremove`  Remove Background from image!
### Random
  * `!meme`  Generate Random memes..
  * `!def <word>`  Defines any word you type..
  * `!advice`  Generate random lief advice.
  * `!echo [args...]`  Reapeat whatever you type after !echo.
  * `!annoy [user] [num=10]`  Annoy Whoever you mention, ecept the Ebic owner of the bot.
  * `!server`  Display basic server info.
  * `![weather|طقس] <city> [lang=en]`  Shows the weather of the Country you entered.
  * `!ping`  Check the bot's ping.
  * `!avatar [avamember]`  Show the users Avatar.
  * `!slap [members]... [reason=no reason]`  Slap any user you want to punish :3.
  * `!cat`  Generate random cat images/gif.
  * `!dog`  Generate random dog images/gif.
### Tic Tac Toe
  * `!tictactoe <p1> <p2>`  Starts a game between two users.
  * `!place <pos>`  Place a mark on the playing table.
  * `!endgame`  End the game before it finishs.
### Voice
  * `!join`  Join the voice channel.
  * `!play <url>`  Download the URL and play the music.
  * `!leave`  Leave the voice channel.
### Admin
  * `!kick [user] [reason]` Kick user.
  * `!ban [user] [reason]` ban user.
  * `!mute [user] [time]` mute user for a period of time.
  * `!clear [amount=10]` Clear number of messages in a channel.
  * `!dm <@user> [content]` Sends a message to a user in his DMs through the bot

## Contributions

Please feel free to do a PR and we would be happy to check it out! there is no template but prefereably you should add the command to the correct cog or create a new one if it fits
