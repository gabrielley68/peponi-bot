import discord
import json
import os
import random
import time

class Reactions:
	members = {
		'yann': False,
		'baptou': False,
		'camion': False
	}

	def toggle(self, member):
		if member not in self.members:
			return "Membres possibles : " + json.dumps(self.members)
		else:
			self.members[member] = not self.members[member]
			return "Done"


TOKEN = "NjA0MzQxNDc1MTEwNTUxNTYy.XURCCg.Q9w5wXUP4bVfs0D64W8ulKRdmog"

with open("./members.json") as json_file:
	data = json.load(json_file)

client = discord.Client();

reactions = Reactions()

#Liste forcément utile d'insulte à compléter
insultes = ["pute", "nique", "suce", "connard", "fils de tracteur", "shlag", "shlag à bite", "j'tencule", "va chier", "negro"]

compteurWowBaptou = 0

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

	#yann
	if reactions.members['yann'] and (message.author.id == 144537000639332352 or message.author.name == "\ud83d\udc3a Noa \ud83d\udc3a"):
		await message.add_reaction("👶")
	# spécial pour blade
	elif message.author.id == 192366356803485696 or message.author.name == "Blade" or message.author.name == "Pepito":
		if reactions.members['baptou']:
			await message.add_reaction("🤓")
		if message.content.isupper():
			with open("./assets/calme_stp.jpg", 'rb') as calmeStpImg:
				await message.channel.send("", file=discord.File(calmeStpImg))
	#petite camille
	elif message.author.id == "" or message.author.name == "LeMilKa":
		if reactions.members['camion']:
			await message.add_reaction("<:camille:598907012478271722>") #emoji camille
	#adodo
	elif message.author.id == 287353218613116928 or message.author.name == "\ud83c\udf48LAVIECBON La bonne source \ud83c\udf48":
		if message.content.endswith("?"):
			await message.channel.send(random.choice(insultes))

	if message.content.endswith(('mai', 'mais', 'mé', 'mée', 'mées', 'més', 'mè', 'mèe', 'mèes', 'mer', 'mers')):
		await message.channel.send("te")
	elif message.content.startswith(('Avant', 'avant')):
		await message.channel.send("mai te")

	elif "chaud" in message.content.lower():
		with open("./assets/chef_martin.jpg", 'rb') as chefMartinImg:
			await message.channel.send("c'est chaud", file=discord.File(chefMartinImg))

	if "gibus" in message.content.lower():
		await message.channel.send("Gibus")

	if message.content.endswith(("inge", "inges")):
		await message.channel.send("qui fait de la moto")

	if message.content.startswith("stp"):

		if message.content.lower() == "stp yann":
			fileName = random.choice(os.listdir("./assets/babies"))
			with open("./assets/babies/" + fileName, 'rb') as openedFile:
				await message.channel.send("", file=discord.File(openedFile))

		elif message.content.startswith("stp dé"):
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

		elif message.content.startswith("stp toggle"):
			arr = message.content.split()
			await message.channel.send(reactions.toggle(arr[2]))

		elif message.content == "stp help":
			await message.channel.send(getHelp())

		elif message.content == "stp name":
			await message.channel.send(message.author.name)

		else:
			await message.channel.send(error())


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


#Affiche l'id de l'emoji ajouté (utile pour trouver l'id des emoji custom)
@client.event
async def on_reaction_add(reaction, user):
	print(reaction.emoji.id)

@client.event
async def on_user_update(before, after):
	if after.name == "Blade" or after.id == 192366356803485696:
		if before.activity != after.activity:
			if after.activity.name == "World of Warcraft":
				compteurWowBaptou = time.time()
			elif before.activity.name == "World of Warcraft":
				# channel général
				channel = client.get_channel(544251275349327873)
				timeSpend = int((time.time() - compteurWowBaptou) / 60)
				await channel.send("Bien joué Baptiste, tu as joué " + str(timeSpend) + " minutes")


@client.event
async def on_ready():
	print('Logged as')
	print(client.user.name)
	print(client.user.id)
	print('--------')
	await client.change_presence(activity=discord.Game(name="fait de la moto")) 


client.run(TOKEN)