import discord
import json
import os
import random

class Reactions:
	members = {
		'yann': False,
		'baptou': False
	}

	def toggle(self, member):
		if member not in self.members:
			return "Membres possibles : " + json.dumps(self.members)
		else:
			self.members[member] = not self.members[member]
			return "Done"




TOKEN = "NjA0MzQxNDc1MTEwNTUxNTYy.XTsj9w.1ceKKuvoJXTiOYwpw5m6_3gug-w"

with open("./members.json") as json_file:
	data = json.load(json_file)

client = discord.Client();

reactions = Reactions()


@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if(message.author.id not in data):
		data[message.author.id] = message.author.display_name
		with open('./members.json', 'w') as outfile:
			json.dump(data, outfile)
	elif data[message.author.id] != message.author.display_name:
		data[message.author.id] != message.author.display_name
		with open('./members.json', 'w') as outfile:
			json.dump(data, outfile)

	if reactions.members['baptou'] and (message.author.id == 144537000639332352 or message.author.display_name == "\ud83d\udc3a Noa \ud83d\udc3a"):
		await message.add_reaction("👶")
	elif reactions.members['yann'] and (message.author.id == 192366356803485696 or message.author.display_name == "Bladego Kit Fisto"):
		await message.add_reaction("🤓")

	if message.content.endswith(('mai', 'mais', 'mé', 'mée', 'mées', 'més', 'mè', 'mèe', 'mèes', 'mer', 'mers')):
		await message.channel.send("te")
	elif message.content.startswith(('Avant', 'avant')):
		await message.channel.send("mai te")

	if message.content.lower() == "stp yann":
		fileName = random.choice(os.listdir("./babies"))
		with open("./babies/" + fileName, 'rb') as openedFile:
			await message.channel.send("", file=discord.File(openedFile))

	if message.content.startswith("stp dé"):
		arr = message.content.split()
		randNumber = random.randrange(1,7)
		deValue = int(arr[2])
		if not isinstance(deValue, int) or deValue < 1 or deValue > 6 or len(arr) < 4:
			await message.channel.send(error())
			return
		if randNumber != deValue:
			await message.channel.send(str(randNumber) + " c'est raté !")
		else:
			finalStr = str(randNumber) + " BAM"
			for user in message.mentions:
				finalStr += " " + user.mention
			await message.channel.send(finalStr)

	if message.content.startswith("stp toggle"):
		arr = message.content.split()
		await message.channel.send(reactions.toggle(arr[2]))


	if message.content == "stp help":
		await message.channel.send(getHelp())


def getHelp():
	return """
Photo de bébé qui pleure : stp yann
Jeu du dé : stp dé [Valeur du dé [1-6]] [Défi] [Personnes concernées (@Pseudo)]
	"""

def error():
	return "Erreur mon ptit pote : stp help pour trouver les commandes"

@client.event
async def on_message_edit(before, after):
	beforeArray = before.content.split()
	afterArray = after.content.split()

	if len(beforeArray) != len(afterArray):
		return

	for i in range(len(beforeArray)):
		sim = 0
		if beforeArray[i] != afterArray[i]:
			for c in beforeArray[i]:
				if c in afterArray[i]:
					sim += 1
			if sim >= 3:
				await after.channel.send(before.author.display_name + " : " + beforeArray[i])

@client.event
async def on_ready():
	print('Logged as')
	print(client.user.name)
	print(client.user.id)
	print('--------')
	await client.change_presence(activity=discord.Game(name="fait de la moto")) 


client.run(TOKEN)