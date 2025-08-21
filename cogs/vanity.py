"""
CREATE A BOT INSTANCE FROM DISCORD DEV PAGE AND ENABLE INTENTS FOR THIS TO WORK. 
MADE BY PLAYEDYABTCH - DISCORD.GG/WRD

"""

from discord.ext import commands
import discord

class vanity(commands.Cog): 
    def __init__(self,client):
        self.client = client
        self.trigger = "/wrd" # CUSTOM STATUS TRIGGER
        self.role_ids = [1400693192189411429, 1400634369982468187]  # ROLES TO GRANT WHEN USER HAS CUSTOM STATUS
        self.announce_channel_id = 1400648743791099965 # CHANNEL TO ANNOUNCE REWARD MESSAGE
        self.allowed_guild_id = 1333039067977486346 # GUILD ID 
        self.user_status_cache = {}
        self.user_has_been_granted_roles = {}

    @commands.Cog.listener()
    async def on_presence_update(self, before: discord.Member, after: discord.Member):
        if after.guild.id != self.allowed_guild_id:
            return    

        old_status = self._get_custom_status(before.activities)
        new_status = self._get_custom_status(after.activities)

        before_offline = before.status == discord.Status.offline
        after_offline = after.status == discord.Status.offline
        
        if after_offline and not before_offline:
            if after.id in self.user_status_cache:
                del self.user_status_cache[after.id]
            return
        
        if before_offline and not after_offline:
            user_has_yep_roles = any(after.guild.get_role(rid) in after.roles for rid in self.role_ids)
            if user_has_yep_roles and new_status and self.trigger in new_status:
                self.user_status_cache[after.id] = new_status
                self.user_has_been_granted_roles[after.id] = True
                return

        if self.user_status_cache.get(after.id) == new_status:
            return
        
        self.user_status_cache[after.id] = new_status

        had_trigger_before = self.trigger in (old_status or "")
        has_trigger_now = self.trigger in (new_status or "")

        channel = after.guild.get_channel(self.announce_channel_id)

        if has_trigger_now and not had_trigger_before:
            if not self.user_has_been_granted_roles.get(after.id, False):
                roles_to_add = [after.guild.get_role(rid) for rid in self.role_ids]
                roles_to_add = [r for r in roles_to_add if r and r not in after.roles]
                if roles_to_add:
                    await after.add_roles(*roles_to_add, reason="Matched /wrd custom status") # FOR AUDIT LOGS, REASON FOR ADDING ROLES
                    self.user_has_been_granted_roles[after.id] = True
                    if channel:
                        await channel.send(f"{after.mention} thank you for repping **/wrd** you now have stream/cam/pic perms!") # CUSTOM REWARD MESSAGE

        elif not has_trigger_now and had_trigger_before:
            roles_to_remove = [after.guild.get_role(rid) for rid in self.role_ids]
            roles_to_remove = [r for r in roles_to_remove if r and r in after.roles]
            if roles_to_remove:
                await after.remove_roles(*roles_to_remove, reason="Removed /wrd from status") # FOR AUDIT LOGS, REASON FOR REMOVING ROLES
                self.user_has_been_granted_roles[after.id] = False

    def _get_custom_status(self, activities):
        for activity in activities:
            if isinstance(activity, discord.CustomActivity):
                return activity.name
        return None
    
async def setup(client):
    await client.add_cog(vanity(client)) # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD
