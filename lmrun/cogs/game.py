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


#############
# Functions #
#############

async def is_guild_setup(guild_id):
    # Get guild record from the database
    async with async_session() as session:
        guild_query = await session.execute(select(Guilds).where(Guilds.id == guild_id))
        guild = guild_query.scalars().first()

    # Check if guild exist
    if guild is None:
        raise NotSetup()


async def get_location(guild_id):
    async with async_session() as session:
        location_query = await session.execute(select(Guilds).where(Guilds.id == guild_id).options(selectinload(Guilds.location)))
        location = location_query.scalars().first().location

    return location


########################
# Property Select Menu #
########################
class PropertySelect(discord.ui.Select):

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
            property_query = await session.execute(select(Properties).where(Properties.id == self.values))
            property = property_query.scalars().first()

        await interaction.response.send_message(f':question: The question for {property.name} is: {property.question}')


#################
# Location View #
#################
class PropertyView(discord.ui.View):

    # Initialize the view
    def __init__(self, options, timeout=180):
        print(options)
        super().__init__(timeout=timeout)
        self.add_item(PropertySelect(options))


##############
# Game Class #
##############
class Game(discord.Cog):

    ####################
    # Initialize Class #
    ####################
    def __init__(self, bot):
        self.bot = bot

    @discord.application_command()
    async def goto(self, interaction):
        """ Goto a property """

        await is_guild_setup(interaction.guild.id)
        location = await get_location(interaction.guild.id)
        options = []

        async with async_session() as session:
            properties = await session.execute(select(Properties).where(Properties.location == location).options(selectinload(Properties.property)))
            for property in properties:
                options.append(discord.SelectOption(value=str(property.id), label=property.name, description=f"{property.property.name} - {property.property.value}"))

        await interaction.send("Chose a location set!", view=PropertyView(options))


#########
# Setup #
#########
def setup(bot):
    bot.add_cog(Game(bot))
