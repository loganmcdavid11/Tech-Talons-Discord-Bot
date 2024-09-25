# Tech Talons Discord Bot

A custom-built Discord bot for Tennessee Tech's Ultimate Frisbee team. 

Please note that this bot is still under development.

**Goal:** To automate and simplify tasks for team members, allowing easy access to information through the bot. Increase member engagement and provide tips and resources for those seeking help with Ultimate Frisbee topics.

---

## Table of Contents
- [Setup](#setup)
- [Features](#features)
  - [Tournament Schedule](#tournament-schedule)
  - [Library of Information](#library-of-information)

---

### Setup

#### Create and Invite Your Bot
- Follow this [guide](https://discordpy.readthedocs.io/en/stable/discord.html) to create your bot and invite it to your desired server.

#### Download Necessary Packages
- This bot is written in Python. Download the latest version of Python [here](https://www.python.org/downloads/).
- Check installation by typing `python --version` in your terminal.
- Install the Discord package by running `pip install discord.py`
- Enable HTTP requests by running `pip install requests`
  
#### Set Up Bot Token
- Click [here](https://discord.com/developers/applications/) to open the Discord Developer Portal and log in.
- Navigate to the **Bot** settings and locate the **Token** section.
- Click the **Copy** button to retrieve your bot token.
- Enter the token in `apikeys.py`, where **BOT_TOKEN** is declared.

#### Using the Bot
- To start the bot, type in your terminal `python3 main.py`
- When typing a command, use the prefix **'!'** followed by the command name.
- For a list of available commands, type `!help`.

---

### Features

#### Tournament Schedule
Captains can add tournaments for members to view at any time, allowing players to RSVP. Captains can also view the list of members who have RSVP'd for each tournament.

- **Add a Tournament:** `!add_tournament "Tournament Name" "Start Date" "End Date" "Location" "Arrival on Field Time" "Field Address" "Lodging Address"`
- **Delete a Tournament:** `!delete_tournament Tournament Name`
- **Edit Tournaments:** `!edit_tournament "Tournament Name" "Start Date" "End Date" "Location" "Arrival on Field Time" "Field Address" "Lodging Address"`
- **View Tournaments:** `!tournaments`
- **RSVP for Tournament:** `!rsvp_tournament Tournament Name`
- **unRSVP from Tournament:** `!unrsvp_tournament Tournament Name`
- **View RSVP List for Specific Tournament:** `!view_rsvp_list Tournament Name`
- **Tournament Packing List:** `!tournament_packing_list`
#### Library of Information
- **View Offical Ultimate Frisbee Rulebook:** `!rulebook`
