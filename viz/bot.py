# -*- coding: utf-8 -*-

import json
from pprint import pprint
from time import sleep, time

from ttgbase.api import Api, Menu
import menu

from tvizbase.api import Api as VizApi
from lib.viz import Viz

from storage import token, maska, viz_reg



class Tip23(Viz):
	
	def __init__(self):
	
		self.token = token
		self.maska = maska
		self.viz_reg_bot = viz_reg["account"]
		self.viz_reg_wif = viz_reg["wif"]
		
		# Подключаем фразы бота
		import msg as bot_msg
		self.bot_msg = bot_msg
		
		self.tg = Api(self.token, report=True, PROXY=False)
		self.prepare_commands()
		
		self.viz = VizApi()
		
		self.bot_menu = Menu(menu.menu, self.commands, self.tg)
		
	##### ##### TG COMMANDS ##### #####
	
	def prepare_commands(self):
	
		self.tg.commands["private_text"] = self.private_text
		self.tg.commands["private_entities"] = self.private_entities
		self.tg.commands["chat_text"] = self.chat_text
		self.tg.commands["chat_entities"] = self.chat_entities
		self.tg.commands["chat_reply"] = self.chat_reply
			
		self.commands = {
					"help:Intro": self.help_intro, 
					"help:Reg": self.help_reg,
					
					"vizsign": self.vizsign,
					"vizlogin": self.vizlogin,
					"vizwallet": self.vizwallet,
					"viz:Info": self.vizinfo,
					"vizinfo:ClaimNow": self.vizclaimnow,
					"vizreg": self.vizreg,
					"vizregYN:Yes": self.vizregyes,
					"vizdelYN:Yes": self.vizdelyes,
					
					"language:Russian": self.language,
					"language:English": self.language,
					"report:On": self.report,
					"report:Off": self.report,
					
					}
					
	##### ##### CHAT ##### #####
	
	def private_text(self, message):
		self.bot_menu.resolve(message)
		
	def private_entities(self, message):
		self.bot_menu.resolve(message)
		pass
		
	def chat_text(self, message):
		#print(message["chat"]["id"], message["text"])
		#tg.send_message(message["chat"]["id"], 'get text')
		pass
	
	def chat_entities(self, message):
	
		user_id, chat_id, lng = self.get_params_chat(message)
		cmd = message["text"]
		
		cmd_all = ['/viz+', '/viz-']
		if (user_id in self.bot_menu.users_tg) and (cmd in cmd_all):
			db = self.bot_menu.users_tg[user_id]
			print(self.maska, 'CMD', chat_id, user_id, cmd)
			
			if cmd in ['/viz+', '/viz-']:
				target_account, target_chat, asset = 'vizaccount', 'vizchat', 'VIZ'
				
			if cmd in ['/viz+']:
				initiator = db.get(target_account, None)
				if initiator:
					account, wif = initiator.split(':')
					db.setdefault(target_chat, [])
					if chat_id not in db[target_chat]:
						if cmd == '/viz+':
							tx = self.viz.get_accounts([account])[0]
						try:
							msg = ' '.join([' +' + str(int(tx["TIP"])), asset])
						except:
							msg = ' error data'
							
						db[target_chat].append(chat_id)
						self.tg.send_message(chat_id, self.bot_msg.InvestorBecome[lng] + msg, delete=True)
						self.bot_menu.save()
					else:
						self.tg.send_message(chat_id, self.bot_msg.InvestorAlready[lng], delete=True)
				else:
					self.tg.send_message(chat_id, self.bot_msg.MustConnectAccount[lng], delete=True)
					
			if cmd in ['/viz-']:
				chat_list = db.get(target_chat, [])
				if chat_id in chat_list:
					db[target_chat].remove(chat_id)
					self.tg.send_message(chat_id, self.bot_msg.InvestorWithdraw[lng] + asset, delete=True)
					self.bot_menu.save()

					
	def chat_reply(self, message):
		user_id, chat_id, lng = self.get_params_chat(message)
		
		text = message["text"]
		user_name = '@' + str(message["from"].get("username", ''))
		message_id = str(message["message_id"])
		
		title = str(message["chat"]["title"])
			
		reply_id = str(message["reply_to_message"]["from"]["id"])
		reply_username = '@' + str(message["reply_to_message"]["from"].get("username", ''))
		reply_text = str(message["reply_to_message"].get("text", ''))
		is_bot = str(message["reply_to_message"]["from"]["is_bot"])
		
		k_like, amount, target_main = text.count('+', 0, 5), 0, None
		
		if 'viz' == text[:3].lower():
			target_main = 'viz'
			try:
				amount = int(text.split()[0].lower().replace('viz', ''))
			except:
				amount = 1
		
		flag_for_del = True if k_like > 0 and len(text) <= 5 else False
		if flag_for_del:
			payload = [chat_id, message_id, self.tg.DEL_DELAY]
			self.tg.delete_message(payload)

		#if (k_like > 0) and (user_id != reply_id) and (str(is_bot) == 'False'):				# Если есть хоть один +, не самоап и не бот
		if (k_like > 0 or amount > 0) and (str(is_bot) == 'False'):								# TEST for TEST Если есть хоть один +, самоап и не бот
			print(self.maska, user_id, reply_id, k_like, amount)
			if user_id in self.bot_menu.users_tg and reply_id in self.bot_menu.users_tg:		# Если юзеры в базе
				
				flag = False																	# Отслеживаем в целом инвестора
				reports = []
				
				target_list = [target_main] if target_main else ['viz']
				for target in target_list:
					
					state_acc, target_chat, wallet_acc = target + 'account', target + 'chat', target + 'wallet'

					chat_list = self.bot_menu.users_tg[user_id].get(target_chat, [])
					if chat_id in chat_list:
					
						flag = True
						
						asset_account = self.bot_menu.users_tg[user_id].get(state_acc, None)
						asset_account_for_donate = self.bot_menu.users_tg[reply_id].get(wallet_acc, None)
						if asset_account and asset_account_for_donate:										# Если оба в базе
							account, wif = asset_account.split(':')
							account_for_donate = asset_account_for_donate
							
							report = None
							lines, comment = text.split(), ''
							if len(lines) >= 2: comment = ' '.join(lines[1:])
							
							if 'viz' == target:
								report = self.viz_donate(account, k_like, title, reply_text, account_for_donate, wif, amount=amount, comment=comment)
								
							if report:
								reports.append(report)
								
						elif asset_account and (not asset_account_for_donate):								# Если нет кому донатить
							msg = self.bot_msg.NoProfileForDonate[lng] + ' ' + target.upper()
							self.tg.send_message(chat_id, msg, delete=True)

				for amount, report in reports:
					# report
					msg = ''.join([' +', amount, report])
					self.tg.send_message(chat_id, reply_username + msg, delete=True)
					if self.bot_menu.users_tg[user_id].get("report", True):
						self.tg.send_message(user_id, 'donate to ' + reply_username + msg)
					if self.bot_menu.users_tg[reply_id].get("report", True):
						self.tg.send_message(reply_id, 'received from ' + user_name + msg)
							
						
				if not flag:
					self.tg.send_message(chat_id, self.bot_msg.InvestorNot[lng], delete=True)
					
	##### ##### HELP ##### #####
		
	def help_intro(self, message):
		msg = 'https://golos.id/ru--blokcheijn/@ksantoprotein/tip23bot-telegramm-bot-dlya-laikov-avtokleminga-i-igr'
		self.tg.send_message(message["chat"]["id"], msg)
		
	def help_reg(self, message):
		msg = 'https://golos.id/ru--blokcheijn/@ksantoprotein/tip23bot-registraciya'
		self.tg.send_message(message["chat"]["id"], msg)
		
		
	##### ##### GET ##### #####
	
	def get_language(self, user_id):
		if user_id in self.bot_menu.users_tg:
			lng = self.bot_menu.users_tg[user_id].get("language", 'Russian')
		else:
			lng = 'Russian'
		return lng
		
	def get_chats(self, chat_list):
		chats = []
		for chat_id in chat_list:
			tx = self.tg.getChat(str(chat_id))
			if tx:
				chat = ''.join(['@', tx.get("username", ''), ':', tx.get("title", '')])
				chats.append(chat)
			else:
				print('error in chat', chat_id)
				chats.append('hidden')
		return chats
		
	def get_params_message(self, message, type):
		user_id = str(message["chat"]["id"])
		lng = self.get_language(user_id)
		keyboard = self.bot_menu.state[type]["keyboard"]
		db = self.bot_menu.users_tg[user_id]		
		return([user_id, lng, keyboard, db])
		
	def get_params_chat(self, message):
		user_id = str(message["from"]["id"])
		chat_id = str(message["chat"]["id"])
		lng = self.get_language(user_id)
		
		#db = self.bot_menu.users_tg[user_id]
		return([user_id, chat_id, lng])
		
	def get_url_from_reply_text(self, reply_text, sign):
		lines = reply_text.split()
		authors = []
		for line in lines:
			if 'https://' == line[:8]:
				url = line
				response = self.golos.rpc.http.get(url, timeout=3)
				if response.ok:
				
					text = str(response.text)
					if sign + ':' in text:
						for i in range(len(text)):
							if sign + ':' == text[i:i+len(sign + ':')]:
								raw = text[i:].split(':')[1]
								author = []
								if raw[0] in list('abcdefghijklmnopqrstuvwxyz'):
									author.append(raw[0])
									for litter in raw[1:]:
										if litter in list('abcdefghijklmnopqrstuvwxyz0123456789.-'):
											author.append(litter)
										else:
											break
								authors.append([''.join(author), url])

		if len(authors) > 0: 
			print(sign, authors[0])
			return authors[0]
		return([False, False])
				
	##### ##### ##### ##### #####
	
	def language(self, message):
		lng = message["text"]
		user_id = str(message["chat"]["id"])
		if lng in ['Russian', 'English']:
			self.bot_menu.users_tg[user_id]["language"] = lng

	def report(self, message):
		type_report = True if message["text"] == 'On' else False
		user_id = str(message["chat"]["id"])
		self.bot_menu.users_tg[user_id].setdefault("report", True)
		self.bot_menu.users_tg[user_id]["report"] = type_report


bot = Tip23()
bot.tg.run()

while True:
	sleep(60*10)
	#admin = input()
	#if admin == 'exit':
	#	break
	#else:
	#	print(bot.maska)
