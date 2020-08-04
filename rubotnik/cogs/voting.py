from discord.ext import commands
from collections import Counter
import asyncio
import time

#config
VOTE_TIME = 180
VOTE_SYMBOL = ":duck:"

#global list of active votes
VOTES = []

class Vote:

    def __init__(self, channel_id, params):
        self.topic = params[0]
        self.votes = []
        self.channel_id = channel_id
        self.users = []
        self.end_time = time.time() + VOTE_TIME
        self.choices = {}
        self.result = str

        #remove already used topic param and add all other parameters to options dict
        params.pop(0)
        for num, choice in enumerate(params, start=1):
          self.choices.update( { num: choice} )

    def place_vote(self, user_id, vote_choice):
        #Validate vote choice
        result = True

        if vote_choice == None:
            result = "You must choose an option."
        elif vote_choice.isdigit() == False:
            result = "Please vote with numbers. Example: !Vote 1."
        elif int(vote_choice) not in self.choices:
            result = "No such choice."
        elif user_id in self.users:
            result = "You have already voted. ಠ_ಠ" 
        
        #if passed validation add selection and append user to list of voters
        if result == True:
            self.votes.append(int(vote_choice))
            self.users.append(user_id)

        return result

    async def run(self):
        #Add vote to global list of live votes and sleep while vote runs
        VOTES.append(self)
        await asyncio.sleep(VOTE_TIME)

        #Count results and find highest vote count for a choice
        results = Counter(self.votes)
        if len(results) == 0:
            highest_vote_count = None
        else:
            highest_vote_count = results.most_common(1)[0][1]            
        
        #build list of winning choices
        winners = []
        for entry, votes in results.items():
            if votes == highest_vote_count:
                winners.append(entry)

        #Build win_string based on possible outcomes of no winner, tie, single winning vote
        if len(winners) == 0:
            win_string = "No Winner :face_palm:"
        elif len(winners) > 1:
            #build list of ties
            win_string = ''
            for x in winners:
                win_string += " " + self.choices[x] + ","
            #remove final comma
            win_string = win_string[:-1]
            #put together final win_string
            win_string = f"Tie between{win_string}... :face_palm:"
        elif len(winners) == 1:
            win_string = "**Winner:** " + self.choices[winners[0]]

        #build string of each choice and number of votes
        cprint = ''
        for k,v in self.choices.items():
            cprint += f"#{str(k)} - {v} {VOTE_SYMBOL * results[k]} \n"
        cprint = cprint.rstrip("\n")

        #Build final results string for output. Textwrap.dedent() failed so here is this ugly multiline string to keep formatting
        self.results = f"""\
-------------------------------------------------------
**{self.topic}**
------------------- **Voting results:** -----------------
{cprint}
-------------------------------------------------------
{win_string}"""

        #remove self for active list of votes
        VOTES.remove(self)
            
    @staticmethod
    def validation(channel_id, params):
        #load all channels with active vote
        live_votes = (v.channel_id for v in VOTES)

        #Set as valid vote, update results if error is discovered
        result = True
        if len(params) < 3:
            result = "You need a minimum of a topic an two choices: !vote create Topic|x|y"
        elif channel_id in live_votes:
            result = "There is already a vote in progress for this channel."
        
        return result

class Voting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def votecreate(self, ctx, *arg):
        params = ' '.join(str(i) for i in arg).split("|")

        #Check for valid vote and return upon failure
        result = Vote.validation(ctx.channel.id, params)
        if result != True:
          await ctx.send(result) 
          return

        #create vote
        new_vote = Vote(ctx.channel.id, params)
        
        #clean up voting options and send message of vote starting
        options = "".join(f"#{k} {v} \n" for k,v in new_vote.choices.items())
        await ctx.send(f"Vote Started: {new_vote.topic} \n {options}")

        #start vote and await completion
        await new_vote.run()

        #display results
        await ctx.send(new_vote.results)
    
    @commands.command()
    async def vote(self, ctx, arg):

        #search global list for matching live vote in channel. Return on failure
        v = next((x for x in VOTES if x.channel_id == ctx.channel.id), False)
        if v == False:
            await ctx.send("There is no vote") 
            return
        
        #attempt to place vote, return error message on failure
        result = v.place_vote(ctx.author.id, arg)
        if result != True:
            await ctx.send(result)
            return

        #delete user voting message
        await ctx.message.delete()

        #update user vote is placed
        await ctx.send(f"{ctx.author.nick} voted {arg}.")

def setup(bot):
    bot.add_cog(Voting(bot))