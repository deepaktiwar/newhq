  
'''
using discord.py version 1.0.0a
'''
import discord
import asyncio
import re
import multiprocessing
import threading
import concurrent

BOT_OWNER_ROLE = 'Runner' # change to what you need
#BOT_OWNER_ROLE_ID = "597332392637890571", 
"569420128794443776", 
"607613349491900436" 
  
 

 
oot_channel_id_list = ["620842231229841421",  #gnew
"620471669869248512",   #iq
"628290139495464990",   #ukt
"613735885460209694",   #ga
"569420128794443776"    #unt

]


answer_pattern = re.compile(r'(not|n)?([1-3]{1})(\?)?(cnf)?(\?)?$', re.IGNORECASE)

apgscore = 100
nomarkscore = 50
markscore = 10

async def update_scores(content, answer_scores):
    global answer_pattern

    m = answer_pattern.match(content)
    if m is None:
        return False

    ind = int(m[2])-1

    if m[1] is None:
        if m[3] is None:
            if m[4] is None:
                answer_scores[ind] += nomarkscore
            else: # apg
                if m[5] is None:
                    answer_scores[ind] += apgscore
                else:
                    answer_scores[ind] += markscore

        else: # 1? ...
            answer_scores[ind] += markscore

    else: # contains not or n
        if m[3] is None:
            answer_scores[ind] -= nomarkscore
        else:
            answer_scores[ind] -= markscore

    return True

class SelfBot(discord.Client):

    def __init__(self, update_event, answer_scores):
        super().__init__()
        global oot_channel_id_list
        #global wrong
        self.oot_channel_id_list = oot_channel_id_list
        self.update_event = update_event
        self.answer_scores = answer_scores

    async def on_ready(self):
        print("======================")
        print("Moonlite Trivia Self Bot")
        print("Connected to discord.")
        print("User: " + self.user.name)
        print("ID: " + str(self.user.id))

    # @bot.event
    # async def on_message(message):
    #    if message.content.startswith('-debug'):
    #         await message.channel.send('d')

        def is_scores_updated(message):
            if message.guild == None or \
                str(message.channel.id) not in self.oot_channel_id_list:
                return False

            content = message.content.replace(' ', '').replace("'", "")
            m = answer_pattern.match(content)
            if m is None:
                return False

            ind = int(m[2])-1

            if m[1] is None:
                if m[3] is None:
                    if m[4] is None:
                        self.answer_scores[ind] += nomarkscore
                    else: # apg
                        if m[5] is None:
                            self.answer_scores[ind] += apgscore
                        else:
                            self.answer_scores[ind] += markscore

                else: # 1? ...
                    self.answer_scores[ind] += markscore

            else: # contains not or n
                if m[3] is None:
                    self.answer_scores[ind] -= nomarkscore
                else:
                    self.answer_scores[ind] -= markscore

            return True

        while True:
            await self.wait_for('message', check=is_scores_updated)
            self.update_event.set()

class Bot(discord.Client):

    def __init__(self, answer_scores):
        super().__init__()
        self.bot_channel_id_list = []
        self.embed_msg = None
        self.embed_channel_id = None
        #global wrong
        self.answer_scores = answer_scores

        # embed creation
        self.embed=discord.Embed(title= "__**CONFETTI TRIVIA**__", description="**Confetti Deep searching.....**", color=0xFFOOFF)
        self.embed.set_author(name ='',url=' ',icon_url='https://cdn.discordapp.com/attachments/592598263996088320/618292227633971230/images.png')
        self.embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/594012615164821523/610794247313948672/videotogif_2019.08.05_22.43.53.gif")
        
        
        self.embed.add_field(name="**__ANSWER 1__**", value="~~0.0~~", inline=False)
        
        self.embed.add_field(name="**__ANSWER 2__**", value="~~0.0~~", inline=False)
        
        self.embed.add_field(name="**__ANSWER 3__**", value="~~0.0~~", inline=False)
        
        
        self.embed.set_footer(text=f"made❤ by ⎝⧹𝗗𝗿. BOSS™╱⎠ & ⎝𝑹𝑨𝑱𝑨⎠"                , \
            icon_url="https://cdn.discordapp.com/attachments/626453661413015552/628458541065306133/IMG_20190912_144400.jpg")

        #await self.bot.add_reaction(embed,':spy:')


    async def clear_results(self):
        for i in range(len(self.answer_scores)):
            self.answer_scores[i]=0

    async def update_embeds(self):
      #  global wrong

         

        one_check = ""
        two_check = ""
        three_check = ""
        
        
        lst_scores = list(self.answer_scores)
        

        highest = max(lst_scores)
        lowest = min(lst_scores)
        answer = lst_scores.index(highest)+1
        #global wrong             

        if highest > 0:
            if answer == 1:
                one_check = ":one::white_check_mark:"
            else:
                one_check = ""

            if answer == 2:
                two_check = ":two::white_check_mark:"
            else:
                two_check = ""

            if answer == 3:
                three_check = ":three::white_check_mark:"
            else:
                three_check = ""

            

        #if lowest < 0:
            #if answer == 1:
                #one_cross = ":x:"
            #if answer == 2:
                #two_cross = ":x:"
            #if answer == 3:
                #three_cross = ":x:"            
 
        self.embed.set_field_at(0, name="**__ANSWER  1__**", value="**{0}**{1}".format(lst_scores[0], one_check))
        
        self.embed.set_field_at(1, name="**__ANSWER  2__**", value="**{0}**{1}".format(lst_scores[1], two_check))
        
        self.embed.set_field_at(2, name="**__ANSWER  3__**", value="**{0}**{1}".format(lst_scores[2], three_check),)


        if self.embed_msg is not None:
            await self.embed_msg.edit(embed=self.embed)

    async def on_ready(self):
        print("==============")
        print("Moonlite Trivia")
        print("Connected to discord.")
        print("User: " + self.user.name)
        print("ID: " + str(self.user.id))

        await self.clear_results()
        await self.update_embeds()
        #await self.change_presence(activity=discord.Game(name='with '+str(len(set(self.get_all_members())))+' users'))
        await self.change_presence(activity=discord.Activity(type=1,name='with CONFETTI ANSWER'))

    async def on_message(self, message):

        # if message is private
        if message.author == self.user or message.guild == None:
            return

        if message.content.lower() == "ci":
            await message.delete()
            if BOT_OWNER_ROLE in [role.name for role in message.author.roles]:
                self.embed_msg = None
                await self.clear_results()
                await self.update_embeds()
                self.embed_msg = \
                    await message.channel.send('',embed=self.embed)
                #await self.embed_msg.add_reaction("✔️")
                self.embed_channel_id = message.channel.id
            else:
                await message.channel.send("**Lol** You Not Have permission To Use This **cmd!** :stuck_out_tongue_winking_eye:")
            return

        if message.content.startswith('*elp'):
          await message.delete()
          if BOT_OWNER_ROLE in [role.name for role in message.author.roles]:
           embed = discord.Embed(title="**__HELP COMMANDS__**", description="**__HOW RUN BOT__**", color=0x00ff00)
           embed.add_field(name="**__SUPPORT GAME__** ", value="**Loco\nSwag-iq\nConfett-India\nHQ Trivia**", inline=False)
           embed.add_field(name="**__WHEN QUESTION COME PUT COMMAND__**", value=" * **__is COMMAND WORK FOR ALL SUPPORT GAME__**", inline=False)
           await message.channel.send(embed=embed)
          

        # process votes
        if message.channel.id == self.embed_channel_id:
            content = message.content.replace(' ', '').replace("'", "")
            updated = await update_scores(content, self.answer_scores)
            if updated:
                await self.update_embeds()

def bot_with_cyclic_update_process(update_event, answer_scores):

    def cyclic_update(bot, update_event):
        f = asyncio.run_coroutine_threadsafe(bot.update_embeds(), bot.loop)
        while True:
            update_event.wait()
            update_event.clear()
            f.cancel()
            f = asyncio.run_coroutine_threadsafe(bot.update_embeds(), bot.loop)
            #res = f.result()

    bot = Bot(answer_scores)

    upd_thread = threading.Thread(target=cyclic_update, args=(bot, update_event))
    upd_thread.start()

    loop = asyncio.get_event_loop()
    loop.create_task(bot.start('NjE4Mzk2MTAyMTE0NDEwNTA2.XZgM9g.EuBYGi_tif-EVHJ1G_n0jaQTOlM'))
    loop.run_forever()


def selfbot_process(update_event, answer_scores):

    selfbot = SelfBot(update_event, answer_scores)

    loop = asyncio.get_event_loop()
    loop.create_task(selfbot.start('NjE3MjY2NTM3MjE2MzQ0MDY0.XWoodg.LsPWb9TxttRTcTSZIPM16S3QOKA',
                                   bot=False))
    loop.run_forever()

if __name__ == '__main__':

    # running bot and selfbot in separate OS processes

    # shared event for embed update
    update_event = multiprocessing.Event()

    # shared array with answer results
    answer_scores = multiprocessing.Array(typecode_or_type='i', size_or_initializer=3)

    p_bot = multiprocessing.Process(target=bot_with_cyclic_update_process, args=(update_event, answer_scores))
    p_selfbot = multiprocessing.Process(target=selfbot_process, args=(update_event, answer_scores))

    p_bot.start()
    p_selfbot.start()

    p_bot.join()
    p_selfbot.join()




 
 
