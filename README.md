# Tech-Talons-Discord-Bot
Self-programmed discord bot made for Tennessee Tech's Ultimate Frisbee team.<br>
Goal: Automate and simplify tasks for members so that information can be easily accessed by the assistance of the Discord Bot. Increase engagement among members. Supply tips and information for those struggling on certain topics associated with Ultimate Frisbee.

---

## Table of Contents

---

### Setup
1. Create and Invite your bot
   - Click this link https://discordpy.readthedocs.io/en/stable/discord.html to help create your bot and invite it to your desired .
2. Download Necessary Packages
   - This discord bot is written in Python. Click here https://www.python.org/downloads/ to download the latest version of Python.
     - Check installation by typing version --python in your terminal
   - In your terminal, install the discord package by typing pip install discord.py
   - Enable requests by typing in your terminal pip install requests
3. Set Up Bot Token
   - Click here https://discord.com/developers/applications/ to open Discord Developer Portal and log in
   - Go to bot settings and look for **Token**
   - Click the **Copy** button to get your token
   - Then enter your bot token in apikeys.py where the **BOT_TOKEN** is declared
4. Using the Bot
   - When typing a command, use the prelimitor **'!'** and then the command name
   - For any questions on what commands to use, type **!help**
---

### Features
<h4>Tournament Schedule</h4>
Captains can add tournaments to a list for members to view at anytime, giving players the choice to RSVP for a tournament. Captains can then pull the list of members who RSVP'd for a tournament in order to see who all is going
- Add Tournaments: !add_tournament "Tournament Name" "Start Date" "End Date" "Location" "Arrival on Field Time" "Field Address" "Lodging Address" 
- Delete Tournaments: !delete_tournament Tournament Name
- Edit Tournaments: !edit_tournament "Tournament Name" "Start Date" "End Date" "Location" "Arrival on Field Time" "Field Address" "Lodging Address" 
- View Tournaments: !tournaments
- RSVP for Tournament: !rsvp_tournament Tournament Name
- unRSVP from Tournament: !unrsvp_tournament Tournament Name
- View RSVP List for Specific Tournament: !view_rsvp_list Tournament Name
<h4>Library of Information</h4>
- View Offical Ultimate Frisbee Rulebook: !rulebook
