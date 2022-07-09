#############
# Libraries #
#############
import discord
from sqlalchemy import select, desc
import re
from discord.ext import tasks
from sqlalchemy.orm import selectinload

###########
# Modules #
###########
from ..database import *
from . errors import NotSetup, TooManyTeams


############################
# Location Set Select Menu #
############################
class LocationSetSelect(discord.ui.Select):

    # Initialize the select menu
    def __init__(self, options):

        super().__init__(
            placeholder="Select...",
            min_values=1,
            max_values=1,
            options=options
        )

    # Callback
    async def callback(self, interaction):  # the function called when the user is done selecting options
        async with async_session() as session:
            location_query = await session.execute(select(Locations).where(Locations.id == self.values))

        location = location_query.scalars().first()

        await interaction.response.send_modal(SetupModal(location=location))


#################
# Location View #
#################
class LocationView(discord.ui.View):

    # Initialize the view
    def __init__(self, options, timeout=180):
        print(options)
        super().__init__(timeout=timeout)
        self.add_item(LocationSetSelect(options))


###############
# Setup Modal #
###############
class SetupModal(discord.ui.Modal):

    # Initialize the modal
    def __init__(self, location):
        self.location = location
        self.number_of_teams = 0
        super().__init__(title="Setup")

        self.add_item(discord.ui.InputText(label="Number of teams:", value="2", min_length=1, max_length=2, required=True))

    # Callback
    async def callback(self, interaction: discord.Interaction):

        # Defer the response as it can take more than 3 seconds to complete
        await interaction.response.defer(ephemeral=True)

        # Assign value from modal to variable
        self.number_of_teams = int(self.children[0].value)

        # Check if guild is already setup
        async with async_session() as session:
            guild_query = await session.execute(select(Guilds).where(Guilds.id == interaction.guild.id))
            guild = guild_query.scalars().first()

        if guild is not None:
            await interaction.followup.send(':no_entry: You have already run setup!')
            return None

        # Create a record in the guild table
        async with async_session() as session:
            guild_record = Guilds(id=interaction.guild.id, name=interaction.guild.name, teams=self.number_of_teams, location_id=self.location.id)
            session.add(guild_record)
            await session.commit()

        # Create a list of teams
        teams = []
        for i in range(self.number_of_teams):
            teams.append(f'team{i+1}')

        # Create Monopoly Run category and role
        lmrun_administrator_role = await interaction.guild.create_role(name='LMRun Administrator')
        lmrun_category = await interaction.guild.create_category('LMRun')

        # Create team roles
        roles = []
        for team in teams:
            team_role = await interaction.guild.create_role(name=f'{team}')
            roles.append(team_role)  # Append role to lisRoles for setting channel permissions

        # Create announcements channel and set permissions
        announcements_channel = await interaction.guild.create_text_channel('announcements', category=lmrun_category)
        await announcements_channel.set_permissions(interaction.guild.default_role, send_messages=False, read_messages=False)

        # Create leader board channel and set permissions
        leader_board_channel = await interaction.guild.create_text_channel('leader-board', category=lmrun_category)
        await leader_board_channel.set_permissions(interaction.guild.default_role, send_messages=False, read_messages=False)

        # Create properties channel and set permissions
        properties_channel = await interaction.guild.create_text_channel('properties', category=lmrun_category)
        await properties_channel.set_permissions(interaction.guild.default_role, send_messages=False, read_messages=False)

        # Create help channel and set permissions
        help_channel = await interaction.guild.create_text_channel('help', category=lmrun_category)
        await help_channel.set_permissions(interaction.guild.default_role, send_messages=False, read_messages=False)
        msg = await help_channel.send('If you need help click the 👍 button below...')
        await msg.add_reaction('👍')

        # Allow teams to view the announcements, leader board, properties and help channels
        for team_role in roles:
            for category in interaction.guild.categories:
                if 'LMRun' in category.name:
                    for channel in category.text_channels:
                        await channel.set_permissions(team_role, send_messages=False, read_messages=True, view_channel=True)

        # Create team channels and set permissions
        for team, team_role in zip(teams, roles):  # Loop through both lists at the same time
            channel = await interaction.guild.create_text_channel(f'{team}', category=lmrun_category)
            await channel.set_permissions(interaction.guild.default_role, send_messages=False, read_messages=False)
            await channel.set_permissions(team_role, send_messages=False, read_messages=True, view_channel=True)

        # Allow monopoly run administrators to view and send messages in all channels
        for channel in lmrun_category.channels:
            await channel.set_permissions(lmrun_administrator_role, send_messages=True, read_messages=True, view_channel=True)

        # Create records in the game table
        async with async_session() as session:
            for team in teams:
                game_record = Games(guild_id=interaction.guild.id, team=team)
                session.add(game_record)

            await session.commit()

        # Send a message saying what we have done
        embed = discord.Embed(title="Setup LMRun up with the following settings: ")
        embed.add_field(name="Location set:", value=self.location.name)
        embed.add_field(name="Number of teams:", value=self.number_of_teams)
        await interaction.followup.send(embed=embed)


###############
# Remove View #
###############
class RemoveView(discord.ui.View):

    # Cancel button
    @discord.ui.button(label="Cancel", row=0, style=discord.ButtonStyle.success)
    async def cancel_button_callback(self, button, interaction):
        await interaction.response.send_message("Remove canceled!")

    # Delete button
    @discord.ui.button(label="Delete", row=1, style=discord.ButtonStyle.danger)
    async def deleteButtonCallback(self, button, interaction):

        # Defer the response as it can take more than 3 seconds to complete
        await interaction.response.defer(ephemeral=True)

        async with async_session() as session:
            guild_query = await session.execute(select(Guilds).where(Guilds.id == interaction.guild.id))
            guild = guild_query.scalars().first()

        if guild is None:
            raise NotSetup()

        # Delete all channels in the category Monopoly Run
        for category in interaction.guild.categories:
            if 'LMRun' in category.name:
                for channel in category.text_channels:
                    await channel.delete()
                await category.delete()

        # Create a list of roles
        roles = ["LMRun Administrator"]
        for i in range(guild.teams):
            roles.append(f'team{i+1}')

        # Delete roles
        for role in interaction.guild.roles:
            if role.name in roles:
                await role.delete()

        # Remove teams from the games table
        async with async_session() as session:
            games_query = await session.execute(select(Games).where(Games.guild_id == interaction.guild.id))
            games = games_query.scalars().all()

            for game in games:
                session.delete(game)

            await session.commit()
            await session.delete(guild)
            await session.commit()

        await interaction.followup.send("Removed LMRun")

    async def on_error(self, error, item, interaction) -> None:
        if isinstance(error, NotSetup):
            await interaction.followup.send(":no_entry: Guild does not exist in the database! Have you run `/setup` ?")


class Administration(discord.Cog):

    # Initialize
    def __init__(self, bot):
        self.bot = bot
        self.update_properties_channel = Administration.update_properties_channel
        self.update_leader_board = Administration.update_leader_board

    # Setup command
    @discord.slash_command()
    async def setup(self, interaction):
        """Setup the server for playing Local Monopoly Run"""
        options = []

        async with async_session() as session:
            location_query = await session.execute(select(Locations))
            locations = location_query.scalars().all()
            for location in locations:
                options.append(discord.SelectOption(value=str(location.id), label=location.name, description=location.description))

        await interaction.send("Chose a location set!", view=LocationView(options))

    # Remove command
    @discord.slash_command()
    async def remove(self, interaction):
        """Remove LMRun channels, roles and data"""
        await interaction.send("Remove LMRun and all associated data?", view=RemoveView())

    # Add command
    @discord.slash_command()
    async def add(self, interaction):
        """ Add an extra team to the current game """

        # Get guild record from the database
        async with async_session() as session:
            guild_query = await session.execute(select(Guilds).where(Guilds.id == interaction.guild.id))
            guild = guild_query.scalars().first()

        # Check if guild exist
        if guild is None:
            raise NotSetup()

        number_of_teams = guild.teams

        if number_of_teams == 99:
            raise TooManyTeams()

        # Get the LMRun Category
        lmrun_category = discord.utils.get(interaction.guild.categories, name='LMRun')

        # Define a variable with the new team to add
        new_team_name = f'team{number_of_teams + 1}'

        # Create team Role
        new_team_role = await interaction.guild.create_role(name=new_team_name)

        lmrun_administrator_role = discord.utils.get(interaction.guild.roles, name='LMRun Administrator')

        # Create team channel and set permissions
        team_channel = await interaction.guild.create_text_channel(new_team_name, category=lmrun_category)
        await team_channel.set_permissions(interaction.guild.default_role, send_messages=False, read_messages=False)
        await team_channel.set_permissions(new_team_role, send_messages=False, read_messages=True, view_channel=True)
        await team_channel.set_permissions(lmrun_administrator_role, send_messages=True, read_messages=True, view_channel=True)

        # Set permissions on announcements, leader board, properties and help channel
        announcements_channel = discord.utils.get(interaction.guild.channels, name='announcements', category=lmrun_category)
        leader_board_channel = discord.utils.get(interaction.guild.channels, name='leader-board', category=lmrun_category)
        properties_channel = discord.utils.get(interaction.guild.channels, name='properties', category=lmrun_category)
        help_channel = discord.utils.get(interaction.guild.channels, name='help', category=lmrun_category)

        await announcements_channel.set_permissions(new_team_role, send_messages=False, read_messages=True, view_channel=True)
        await leader_board_channel.set_permissions(new_team_role, send_messages=False, read_messages=True, view_channel=True)
        await properties_channel.set_permissions(new_team_role, send_messages=False, read_messages=True, view_channel=True)
        await help_channel.set_permissions(new_team_role, send_messages=False, read_messages=True, view_channel=True)

        async with async_session() as session:
            game_record = Games(guild_id=interaction.guild.id, team=new_team_name)
            session.add(game_record)
            guild.teams = number_of_teams + 1
            await session.commit()

        await interaction.response.send_message(f":white_check_mark: Successfully added {new_team_name}!")

    # Start command
    @discord.slash_command()
    async def start(self, interaction):
        """Start the game"""
        # Get guild record from the database
        async with async_session() as session:
            guild_query = await session.execute(select(Guilds).where(Guilds.id == interaction.guild.id))
            guild = guild_query.scalars().first()

        # Check if guild exist
        if guild is None:
            raise NotSetup()

        # Get the LMRun Category
        lmrun_category = discord.utils.get(interaction.guild.categories, name='LMRun')

        # Start update_properties_channel Loop and update_leader_board Loop
        self.update_properties_channel.start(self, interaction)
        self.update_leader_board.start(self, interaction)

        # Get the number of teams the guild currently has
        number_of_teams = guild.teams

        # Declare lisTeams based on number of teams
        teams = []
        for i in range(number_of_teams):
            teams.append(f'team{i+1}')

        # Update send permissions on team channels
        for team in teams:
            team_role = discord.utils.get(interaction.guild.roles, name=f'{team}')
            team_channel = discord.utils.get(interaction.guild.channels, name=f'{team}')
            await team_channel.set_permissions(team_role, send_messages=True, view_channel=True)

        # Get Announcement Channel and send a message
        announcement_channel = discord.utils.get(interaction.guild.channels, name='announcements', category_id=lmrun_category.id)
        await announcement_channel.send('Game Start!')

        # Respond to slash command
        await interaction.response.send_message(f"Game Started!")

    # Stop command
    @discord.slash_command()
    async def stop(self, interaction):
        """End the current game"""

        # Get guild record from the database
        async with async_session() as session:
            guild_query = await session.execute(select(Guilds).where(Guilds.id == interaction.guild.id))
            guild = guild_query.scalars().first()

        # Check if guild exist
        if guild is None:
            raise NotSetup()

        # Get the LMRun Category
        lmrun_category = discord.utils.get(interaction.guild.categories, name='LMRun')

        # Start update_properties_channel Loop and update_leader_board Loop
        self.update_properties_channel.stop()
        self.update_leader_board.stop()

        # Get the number of teams the guild currently has
        number_of_teams = guild.teams

        # Declare lisTeams based on number of teams
        teams = []
        for i in range(number_of_teams):
            teams.append(f'team{i+1}')

        # Update send permissions on team channels
        for team in teams:
            team_role = discord.utils.get(interaction.guild.roles, name=f'{team}')
            team_channel = discord.utils.get(interaction.guild.channels, name=f'{team}')
            await team_channel.set_permissions(team_role, send_messages=False, view_channel=True)

        # Get Announcement Channel and send a message
        announcement_channel = discord.utils.get(interaction.guild.channels, name='announcements', category_id=lmrun_category.id)
        await announcement_channel.send('Game Over!')

        # Respond to slash command
        await interaction.response.send_message(f"Game Finished!")

    # Update properties channel task
    @tasks.loop(minutes=2, count=None)
    async def update_properties_channel(self, interaction):

        print("Am i running?")
        # Get which set of questions the guild is using
        async with async_session() as session:
            location_query = await session.execute(select(Guilds).where(Guilds.id == interaction.guild.id).options(selectinload(Guilds.location)))
            location = location_query.scalars().first().location

        # Create Embeds
        brown_properties_embed = discord.embeds.Embed(
            title='Brown Properties',
            color=discord.Colour.from_rgb(139, 69, 19)
        )
        light_blue_properties_embed = discord.embeds.Embed(
            title='Light Blue Properties',
            color=discord.Colour.from_rgb(135, 206, 235)
        )
        pink_properties_embed = discord.embeds.Embed(
            title='Pink Properties',
            color=discord.Colour.from_rgb(218, 112, 214)
        )
        orange_properties_embed = discord.embeds.Embed(
            title='Orange Properties',
            color=discord.Colour.from_rgb(255, 165, 0)
        )
        red_properties_embed = discord.embeds.Embed(
            title='Red Properties',
            color=discord.Colour.from_rgb(255, 0, 0)
        )
        yellow_properties_embed = discord.embeds.Embed(
            title='Yellow Properties',
            color=discord.Colour.from_rgb(255, 255, 0)
        )
        green_properties_embed = discord.embeds.Embed(
            title='Green Properties',
            color=discord.Colour.from_rgb(0, 179, 0)
        )
        dark_blue_properties_embed = discord.embeds.Embed(
            title='Dark Blue Properties',
            color=discord.Colour.from_rgb(0, 0, 255)
        )
        black_properties_embed = discord.embeds.Embed(
            title='Train Stations',
            color=discord.Colour.from_rgb(255, 255, 255)
        )

        # Get id, value and location from database and add to the relevant embeds
        async with async_session() as session:
            properties_query = await session.execute(select(Properties).where(Properties.location == location).options(selectinload(Properties.property)))
            properties = properties_query.scalars().all()

            for property in properties:

                property_name = getattr(Games, f"{property.property.name}_status")

                async with async_session() as session:

                    status_query = await session.execute(select(PropertyStatus).where(PropertyStatus.value == "Owned"))
                    status = status_query.scalars().first()

                    owner_query = await session.execute(select(Games).where(Games.guild_id == interaction.guild.id, property_name == status))
                    owner = owner_query.scalars().first()
                    if owner is not None:
                        owner = owner.team

                # Add fields to Embed
                if re.sub('[0-9]+', '', property.property.name) == 'brown':
                    brown_properties_embed.add_field(name=property.name, value=f'ID: {property.property.name} \n Value: {property.property.value} \n Owner: {owner}')
                elif re.sub('[0-9]+', '', property.property.name) == 'lightblue':
                    light_blue_properties_embed.add_field(name=property.name, value=f'ID: {property.property.name} \n Value: {property.property.value}  \n Owner: {owner}')
                elif re.sub('[0-9]+', '', property.property.name) == 'pink':
                    pink_properties_embed.add_field(name=property.name, value=f'ID: {property.property.name} \n Value: {property.property.value} \n Owner: {owner}')
                elif re.sub('[0-9]+', '', property.property.name) == 'orange':
                    orange_properties_embed.add_field(name=property.name, value=f'ID: {property.property.name} \n Value: {property.property.value} \n Owner: {owner}')
                elif re.sub('[0-9]+', '', property.property.name) == 'red':
                    red_properties_embed.add_field(name=property.name, value=f'ID: {property.property.name} \n Value: {property.property.value} \n Owner: {owner}')
                elif re.sub('[0-9]+', '', property.property.name) == 'yellow':
                    yellow_properties_embed.add_field(name=property.name, value=f'ID: {property.property.name} \n Value: {property.property.value} \n Owner: {owner}')
                elif re.sub('[0-9]+', '', property.property.name) == 'green':
                    green_properties_embed.add_field(name=property.name, value=f'ID: {property.property.name} \n Value: {property.property.value} \n Owner: {owner}')
                elif re.sub('[0-9]+', '', property.property.name) == 'darkblue':
                    dark_blue_properties_embed.add_field(name=property.name, value=f'ID: {property.property.name} \n Value: {property.property.value} \n Owner: {owner}')
                elif re.sub('[0-9]+', '', property.property.name) == 'black':
                    black_properties_embed.add_field(name=property.name, value=f'ID: {property.property.name} \n Value: {property.property.value} \n Owner: {owner}')

        # Get the properties channel
        catMonopolyRun = discord.utils.get(interaction.guild.categories, name='LMRun')
        properties_channel = discord.utils.get(interaction.guild.channels, name='properties', category_id=catMonopolyRun.id)

        # Remove last messages
        await properties_channel.purge(limit=10)

        # Send the embeds
        await properties_channel.send(embed=brown_properties_embed)
        await properties_channel.send(embed=light_blue_properties_embed)
        await properties_channel.send(embed=pink_properties_embed)
        await properties_channel.send(embed=orange_properties_embed)
        await properties_channel.send(embed=black_properties_embed)
        await properties_channel.send(embed=red_properties_embed)
        await properties_channel.send(embed=yellow_properties_embed)
        await properties_channel.send(embed=green_properties_embed)
        await properties_channel.send(embed=dark_blue_properties_embed)

    # Update leader board task
    @tasks.loop(minutes=2.1, count=None)
    async def update_leader_board(self, interaction):

        async with async_session() as session:
            teams_query = await session.execute(select(Games).where(Games.guild_id == interaction.guild.id).order_by(desc(Games.money)))
            teams = teams_query.scalars().all()

        leader_board_embed = discord.embeds.Embed(
            title='Leader board!',
            color=discord.Colour.orange()
        )
        i = 1

        for team in teams:

            # Add to embed #
            leader_board_embed.add_field(name=f'{i}. {team.team}', value=f'Money: {team.money}', inline=False)
            i = i + 1

        # Get the properties channel #
        catMonopolyRun = discord.utils.get(interaction.guild.categories, name='LMRun')
        leader_board_channel = discord.utils.get(interaction.guild.channels, name='leader-board', category_id=catMonopolyRun.id)

        # Remove last message #
        await leader_board_channel.purge(limit=2)

        # Send the embed #
        await leader_board_channel.send(embed=leader_board_embed)


# Setup
def setup(bot):
    bot.add_cog(Administration(bot))
