
<div align="center">
    <img src="https://img.shields.io/badge/Made%20with-Python-1f425f.svg?style=for-the-badge">
    <img alt="Discord" src="https://img.shields.io/discord/994610780819443822?label=Discord&style=for-the-badge">
    <img src="https://img.shields.io/github/contributors/bxdavies/lmrun?style=for-the-badge">
    <img src="https://img.shields.io/github/forks/bxdavies/lmrun.svg?style=for-the-badge">
    <img src="https://img.shields.io/github/stars/bxdavies/lmrun.svg?style=for-the-badge">
    <img src="https://img.shields.io/github/issues/bxdavies/lmrun.svg?style=for-the-badge">
    <img src="https://img.shields.io/github/license/bxdavies/lmrun.svg?style=for-the-badge">
</div>
<br />
<div align="center">
  <a href="https://github.com/bxdavies/lmrun">
    <img src="images/logo.jpeg" alt="Logo" width="80" height="80">
  </a>

<h2 align="center">LMRun</h2>

  <p align="center">
    A game based on the Scout and Girl Guide event <a href= "https://monopoly-run.co.uk/">Monopoly Run</a>. 
    <br />
    <a href="https://github.com/bxdavies/lmrun"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://discord.gg/mv99rmjKmB">View Demo</a>
    ·
    <a href="https://github.com/bxdavies/lmrun/issues">Report Bug</a>
    ·
    <a href="https://github.com/bxdavies/lmrun/discussions">Request Feature</a>
    ·
    <a href="https://github.com/bxdavies/lmrun/discussions"> Get Support </a>
  </p>
</div>


<a href="https://pyup.io/repos/github/bxdavies/lmrun/"><img src="https://pyup.io/repos/github/bxdavies/lmrun/shield.svg?token=cd23994b-dbad-49d7-bdd3-c8fd645c628a" alt="Updates" /></a>

## About
LMRun was originally built during the COVID lockdown periods as [Monopoly Run Discord Bot](https://github.com/bxdavies/monopoly-run-discord-bot). The bot was built after seeing Monopoly Run being run for Scouts using a spreadsheet. To improve on this idea I developed this bot.

The game works similar to the real world game in which a team visits a property and answers a question at the property. If they are the first one to answer the question correctly they own the property if they are not then they pay rent to the owner.

## Discord Server
![Discord Banner 2](https://discordapp.com/api/guilds/994610780819443822/widget.png?style=banner2)

## Usage
Add the bot to your Discord server with [this]() link.

1. Start by running `/setup`. This will ask what location set you want to use and how many teams you want. Once the command has completed you should see that the following channels have been created: 
    - #announcements
    - #leader-board
    - #properties
    - #help
    - #team1
    - #team2
    - Any other team channels following the pattern #team and then the team number

A location set is a set of questions and answers for a property for example Brown1 in the London Monopoly Game is Old Kent Road and the question for that property is; which well known supermarket backs onto the corner of old kent Roadand Ossory Road. But if you were to use a different location set than Brown1 might be a different location meaning, it would have a different question and answer.

Recommend team size is 2-4 players. 

2. You now need to assign players to teams by assigning them a team role for example, if I wanted John Doe to be on team2 I wold assign him the role of team2. 
3. When you are ready to start the game run `/start`, this should send a message to the announcements channel and allow teams to send messages in their channels. 
### Channel explanation 
  - #announcements - Is used for game announcements, this includes letting the players know when the game has started and finished, when a team has brought a property, and when a property is up for auction.
  - #leader-board - Is used to display the leader board, the winning team is the team with the most amount of money. 
  - #properties - Is used to display a list of properties, and there details, such as ID, Value and Owner. 
  - #help 
  - #team1 - This channel is specifically only for team 1 to message each other and the bot with. 

## Get started
This section explains how to setup this project to run locally. 

### Prerequisites
- Python > 3.10 
- Database
- PIP
- Discord Developer Account 

### Installation
1. Clone the repo

## Roadmap
- [ ] 
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

## Contact

Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - email@email_client.com

Project Link: [https://github.com/github_username/repo_name](https://github.com/github_username/repo_name)

## Acknowledgments