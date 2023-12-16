#import discord library to create a discord bot 
import discord
#import os so that I can interact with the linux OS and environment variables in the ec2 instance
import os
#import random so that a random choice or number is generated
import random
#retrieves metadata from the instance by importing from the ec2_metadata
from ec2_metadata import ec2_metadata
#imports variables from a different file named '.env' by using load_dotenv to load and import
from dotenv import load_dotenv

#a list containing 3 strings that are 'jokes'
jokes = [
	"I went to buy some camo pants but couldn't find any.",
	"Why was six afraid of seven? Because seven eight nine.",
	"When life gives you melons, you might be dyslexic.",
]
#to load the .env file that contains the discord bot token
load_dotenv()
#function to create the discord bot client
client = discord.Bot()
#retrieves token from .env file to convert into a string
token = str(os.getenv('TOKEN'))

#this is an event that is initiated when the discord bot connects to the discord server and prints the info below once logged in
@client.event
async def on_ready():
	print("Logged in as a bot {0.user}".format(client))
	print(f'EC2 Region: {ec2_metadata.region}')
	print(f'EC2 Instance ID: {ec2_metadata.instance_id}')
	print(f'Public IP Address: {ec2_metadata.public_ipv4}')

#an event that is initated when a message is sent into the discord channel
@client.event
async def on_message(message):
	username = str(message.author).split("#")[0]
	channel = str(message.channel.name)
	user_message = str(message.content)

	#if statement so the bot doesn't respond to itself
	if message.author == client.user:
		return

	#if statement if user sends message into the "discord-bots" channel
	if channel == "discord-bots":
		#try and else blocks are used for errors for the bot along with the appropriate responses
		try:
			#if, elif, else statements with prompts and responses
			if user_message.lower() == "hello" or user_message.lower() == "hi":
				await message.channel.send(f'Wassup {username}')
				return
			
			elif user_message.lower() == "hello world":
				await message.channel.send(f'Hello {username}')

			elif user_message.lower() == "bye":
				await message.channel.send(f'See ya {username}')

			elif user_message.lower() == "tell me a joke":
				#appends randomized joke from list
				random_joke = random.choice(jokes)
				await message.channel.send(random_joke)

			elif user_message.lower() == "tell me about my server":
				#added new line by using \n after each section for easier user readability
				await message.channel.send(f'EC2 Region: {ec2_metadata.region}\nEC2 Instance ID: {ec2_metadata.instance_id}\nIP Address: {ec2_metadata.public_ipv4}')

			else:
				#else statement for other inputs that don't meet conditions above along with response
				await message.channel.send(f"Sorry, I don't have a repsonse for that.")
		#if try functions fail, then this block becomes true along with appropriate error response
		except Exception as e:
			await message.channel.send(f"Error: {e}")				  

#allows bot to run and connect to discord using the discord token							  
client.run(token)