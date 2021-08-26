import discord
from datetime import datetime
from discord.ext import commands

from core import checks
from core.models import PermissionLevel

DEPS_DATA = {
    "mr": {
        "category_id": 875240777146593320,
        "pretty_name": "Marketing Department",
        "reminders": None,
        "role_id": 875249700352176159,
        "send_message_to_user": True
    },
    "hr": {
        "category_id": 875241988788715540,
        "pretty_name": "Human Resources",
        "reminders": None,
        "role_id": 875248684114268170,
        "send_message_to_user": True
    },
    "mod": {
        "category_id": 875242122280849449,
        "pretty_name": "Moderation",
        "reminders": None,
        "role_id": 875248828712886272,
        "send_message_to_user": True
    },


class Transfer(commands.Cog, name="Transfer the thread to other departments"):
    def __init__(self, bot):
        self.bot = bot
        
        
       
    @commands.command()
    @checks.thread_only()
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def transfer(self, ctx, *, to: str=None):
        """Command that transfers thread to other departments."""
        if to is None:
            embed = discord.Embed(title=f"Department Transfer", description=f"Please pick a department to transfer to.\n\n`hr` - Human Resources\n`mod` - Moderation\n`mr` - Marketing",
                                  color=discord.Color.red(), timestamp=datetime.utcnow())
            return await ctx.send(embed=embed)
        to = to.lower()
        data = None
        try:
            data = DEPS_DATA[to]
        except:
            embed = discord.Embed(title=f"Department Transfer",description=f"You have provided invalid dept code.\n\n`hr` - Human Resources\n`mod` - Moderation\n`mr` - Marketing",
                                  color=discord.Color.red(), timestamp=datetime.utcnow())
            await ctx.send(embed=embed)
            return
        
        if data["send_message_to_user"]:
            mes = "You are being transferred to **`"
            mes += data["pretty_name"]
            mes += "`**."
            
            if data["reminders"] is not None:
                mes += "**__Reminders__**\n"
                mes += data["reminders"]

            msg = ctx.message
            msg.content = mes
            
            await ctx.thread.reply(msg, anonymous = True)
        
        await ctx.channel.edit(category=self.bot.get_channel(data["category_id"]), sync_permissions=True) 
        await ctx.send("<@&%s>" % str(data["role_id"]))
        
def setup(bot):
    bot.add_cog(Transfer(bot))
