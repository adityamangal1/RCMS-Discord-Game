import discord
import re
from util.verify_util import verify_start_game
from util.insert import insert_new_temp,pick_chit,start_game,ans_mantri
import os
from random import shuffle

client = discord.Client()

character = ['RAJA','CHOR','MANTRI','SIPAHI']

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('&start '):
    msg = message.content.split('&start ',1)[1]
    msg = msg.split(' ')
    print(msg)
    msg_un = msg
    msg_un.append('<@!{}>'.format(message.author.id))
    if not len(set(msg_un)) == 4:
      await message.channel.send('We need total 4 players')
      return
    for i in  range(3):
      if re.findall('<@!.*?>', msg[i]):
        msg[i] = msg[i][3:-1]
        
      else:
        await message.channel.send('invalid input......')
        return

    sts = verify_start_game(message.author.id,msg[0],msg[1],msg[2])
    
    if sts == False:
        await message.channel.send('somthing went wrong...')
    
    elif sts != True:
        await message.channel.send('<@!{}> is alerady in a game...'.format(sts))
    
    else:
        sts_in = insert_new_temp(message.author.id,msg[0],msg[1],msg[2])
        if not sts_in:
            await message.channel.send('somthing  went wrong...')
        else:
            embed=discord.Embed(title="RCMS", description="<@!{}> :crossed_swords: <@!{}> :crossed_swords: <@!{}> :crossed_swords: <@!{}>".format(msg[0],msg[1],msg[2],message.author.id), color=0xFF5733)
            embed.add_field(value="&pick a chit <@!{}>".format(message.author.id), name="accept the invitation", inline=False)
            await message.channel.send(embed=embed)

  elif message.content.startswith('&pick a chit '):
    msg = message.content.split('&pick a chit ',1)[1]
    if re.findall('<@!.*?>', msg):
      msg = msg[3:-1]
    else:
      await message.channel.send('invalid input......')
      return
    rs_p = pick_chit(message.author.id,msg)
    if rs_p == None:
      await message.channel.send('Somthing Went wrong...')
      return
    elif rs_p == 'accpted':
      await message.channel.send('accpeted waiting for others...')
    elif rs_p == False:
      await message.channel.send('Already in game...')
    elif rs_p == msg:
      await message.channel.send('No game found...')
    elif rs_p == 'no game':
      await message.channel.send('you are not in that game...')
    elif rs_p == True:
      chara = character[:]
      shuffle(chara)
      rs_g = start_game(chara,msg)
      if rs_g == None:
        await message.channel.send('Somthing Went wrong...')
      else:
        user = await client.fetch_user(int(rs_g[0]['usr']))
        await user.send(f"You are {rs_g[0]['chr']}, Have fun...")
        user = await client.fetch_user(int(rs_g[1]['usr']))
        await user.send(f"You are {rs_g[1]['chr']}")
        user = await client.fetch_user(int(rs_g[2]['usr']))
        await user.send(f"You are {rs_g[2]['chr']}")
        user = await client.fetch_user(int(rs_g[3]['usr']))
        await user.send(f"You are {rs_g[3]['chr']}")
        mantri = chara.index('MANTRI')
        await message.channel.send('Your character has been sent to your DM....')
        await message.channel.send(f"<@!{rs_g[mantri]['usr']}> is mantri \nfind the thief: &thief <tag the thief>")

  elif message.content.startswith('&thief '):
    msg = message.content.split('&thief ',1)[1]
    if re.findall('<@!.*?>', msg):
      msg = msg[3:-1]
    else:
      await message.channel.send('invalid input......')
      return
    resp = ans_mantri(message.author.id,msg)
    if resp == None:
      await message.channel.send('Somthing went wrong......')
    elif resp == False:
      await message.channel.send('you can not use this')
    elif resp[0] == False:
      await message.channel.send('opps that person was innocent ')
      await message.channel.send(f"<@!{resp[5]}> was the CHOR")
      await message.channel.send(f"<@!{resp[1]['usr']}>{resp[1]['chr']} \n<@!{resp[2]['usr']}>{resp[2]['chr']} \n <@!{resp[3]['usr']}>{resp[3]['chr']} \n <@!{resp[4]['usr']}>{resp[4]['chr']} \n")
    elif resp[0] == True:
      await message.channel.send('Congo you caught the CHOR ')
      await message.channel.send(f"<@!{resp[5]}> was the CHOR")
      await message.channel.send(f"<@!{resp[1]['usr']}>{resp[1]['chr']} \n<@!{resp[2]['usr']}>{resp[2]['chr']} \n <@!{resp[3]['usr']}>{resp[3]['chr']} \n <@!{resp[4]['usr']}>{resp[4]['chr']} \n")


      

client.run(os.environ['botToken'])