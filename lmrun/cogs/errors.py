import discord


class LMRunError(discord.ApplicationCommandError):
    pass


class NotInTeamChannel(LMRunError):
    def __init__(self, team_role, channel):
        self.team_role = team_role
        self.channel = channel
        super().__init__(f'You must used this command in your team channel. Your team is {team_role} therefore you should be using this command in the channel #{team_role} not in #{channel}')


class AlreadyVisited(LMRunError):
    def __init__(self, property):
        self.property = property
        super().__init__(f'You have already visited and answered {property}, correctly!')


class TooManyTeams(LMRunError):
    pass


class NotSetup(LMRunError):
    pass


class LMRunAdministratorRoleNotFound(LMRunError):
    pass


class NoTeamRole(LMRunError):
    pass


class TooManyTeamRoles(LMRunError):
    pass
