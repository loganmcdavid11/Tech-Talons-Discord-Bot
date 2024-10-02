# Tech Talons Discord Bot

A custom-built Discord bot for Tennessee Tech's Ultimate Frisbee team. 

Please note that this bot is still under development.

**Goal:** To automate and simplify tasks for team members, allowing easy access to information through the bot. Increase member engagement and provide tips and resources for those seeking help with Ultimate Frisbee topics.

---

## Table of Contents
- [Setup](#setup)
- [Features](#features)
  - [Help Commands](#help-commands)
  - [Tournament Schedule](#tournament-schedule)
  - [Purple vs. Gold Scrimmage](#purple-vs-gold-scrimmage)
  - [Channel Related Commands](#channel-related-commands)
  - [Library](#library)

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
#### Help Commands
- **List of Helpful Commands**: `!help`
- **List of Helpful Captain Commands**: `!help_captain`

#### Tournament Schedule
##### Member Permissions: 
- Players can view upcoming tournaments as well as rsvp / unrsvp for specific upcoming tournaments
- Players can view a packing list in order to be well prepared for a tournament
##### Admin Permissions:
- Captains can add and delete tournaments to a list, as well as modify the tournament
- Captains can view an rsvp list for each upcoming tournament
##### Commands:
- **Add a Tournament:** `!add_tournament "Tournament Name" "Start Date" "End Date" "Location" "Arrival on Field Time" "Field Address" "Lodging Address"`
- **Delete a Tournament:** `!delete_tournament <Tournament Name>`
- **Edit Tournaments:** `!edit_tournament "Tournament Name" "Start Date" "End Date" "Location" "Arrival on Field Time" "Field Address" "Lodging Address"`
- **View Tournaments:** `!tournaments`
- **RSVP for Tournament:** `!rsvp_tournament <Tournament Name>`
- **unRSVP from Tournament:** `!unrsvp_tournament <Tournament Name>`
- **View RSVP List for Specific Tournament:** `!view_tournament_rsvp_list <Tournament Name>`
- **Tournament Packing List:** `!tournament_packing_list`
- **List of Tournament Commands:** `!tournament_commands`
- **List of Tournament Commands for Captains:** `!tournament_commands_captain`
#### Purple vs. Gold Scrimmage
##### Member Permissions: 
- Players can rsvp / unrsvp from an organized scrimmage called *Purple vs. Gold* as either a handler, cutter, or "hybrid"
##### Admin Permissions: 
- Captains can view the list of RSVP's in order to see the total as well as who is what position
- Captains can randomly sort teams, dividing positions evenly. Captains can then approve the team, granting purple or gold role depending on which team you are on
##### Commands:
- **RSVP for Scrimmage:** `!rsvp_scrimmage <position name>`
  - `<position name>` = *handler*, *cutter*, or *hybrid*
- **unRSVP from Scrimmage:** `!unrsvp_scrimmage <position name>`
  - `<position name>` = *handler*, *cutter*, or *hybrid*
- **View RSVP List for Scrimmage:** `!view_scrimmage_rsvp_list`
- **Randomly Sort Teams:** `!sort_teams`
- **Approve Sorted Teams:** `!approve_teams`
- **Reset Teams:** `!reset_teams`
- **List of Scrimmage Commands:** `!scrimmage_commands`
- **List of Scrimmage Commands for Captains:** `!scrimmage_commands_captain`
#### Channel Related Commands
##### Permissions:
- Members can assign themselves the "Cutter" "Handler" or both of the roles as well as remove it
- Members can assign themselves the "Tournament" role as well as remove it
- Members can assign themselves the "Team Purple" or "Team Gold" role as well as remove it
##### Commands
- **Choose a Position:** `!choose_position <position name>`
  - `<position name>` = *handler*, *cutter*, or *handler cutter*
- **Remove a Possition:** `!remove_position <position name>`
  - `<position name>` = *handler*, *cutter* or *handler cutter*
- **Add Tournament Role:** `!add_tournament_role
- **Remove Tournament Role:** `remove_tournament_role`
- **Add to Team Purple or Team Gold:** `!add_purple_gold <team name>`
  - `<team name>` = *purple* or *gold*
- **Remove from Team Purple or Team Gold:** `remove_purple_gold <team name>`
  - `<team name>` = *purple* or *gold*
- **List of Channel Commands:** `!channel_commands`
#### Library
##### Permissions:
- Members can view important information such as the rules or the playbook
##### Commands
- **View Offical Ultimate Frisbee Rulebook:** `!rulebook`
- **View Talons Official Playbook:** `!playbook`
