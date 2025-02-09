import hikari
import hikari.channels
import arc

class Sandbox:
    users: list[hikari.User]
    channels: list[hikari.PartialChannel]
    childEnvironments: list["Sandbox"]
    commands: list[arc.command.SlashCommand]

    def get_user(self, user_id: str):
        for user in self.users:
            if user.id == user_id:
                return user
        
        result = None
        for env in self.childEnvironments:
            result = env.get_user(user_id)
            if result is not None:
                return result
        
        return None
