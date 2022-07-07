import discord

class LMRunError(discord.ApplicationCommandError):
    pass


class InvalidPropertyName(LMRunError):
    def __init__(self, argument):
        self.argument = argument
        super().__init__('Property "{}" does not exist.'.format(argument))


class NotInTeamChannel(LMRunError):
    def __init__(self, argument1, argument2):
        self.argument1 = argument1
        self.argument2 = argument2
        super().__init__(f'{argument1} is not equal to {argument2}')


class AlreadyVisted(LMRunError):
    def __init__(self, argument):
        self.argument = argument
        super().__init__(f'You have already visited and answered {argument}, correctly!')


class TooManyTeams(LMRunError):
    pass

class NotSetup(LMRunError):
    pass

class NotEnoughTeams(LMRunError):
    pass


class MonopolyRunAdministratorRoleNotFound(LMRunError):
    pass


class DatabaseTableNotFound(LMRunError):
    pass