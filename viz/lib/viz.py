# -*- coding: utf-8 -*-
# Depended Library

import json
from pprint import pprint
from time import sleep, time

class Viz():

	##### ##### DONATE ##### #####
	
	def viz_donate(self, initiator, k_like, title, reply_text, receiver, wif, **kwargs):
	
		payload = self.viz.get_accounts([initiator])[0]
		comment = kwargs.get("comment", '')
		try:
			TIP = payload["TIP"]
			amount = kwargs.get("amount", 0)
			if amount == 0: amount = round(k_like * TIP / 100, 3)
			if (TIP > 0) and (TIP >= amount > 0):
				balance = int(TIP - amount)
				todo = ''
				
				#author_from_permlink, permlink = self.get_permlink_from_reply_text(reply_text)
				author_from_url, url = self.get_url_from_reply_text(reply_text, 'VIZ')
				
				if url:
					receiver, todo = author_from_url, ' to ' + author_from_url
					memo = url + ' tip23bot ' + comment
				else:
					memo = comment + ' tip23bot ' + reply_text[:250]
						
				tx = self.viz.tip(initiator, receiver, amount, wif, memo=memo)		
				if tx:
					pool = ''.join(['(', str(balance), ')'])
					msg = [str(amount), ' VIZ, ' + pool + todo]
					return msg
			else:
				print('ERROR tip', initiator, k_like, '=>', receiver)
		except:
			print('ERROR viz_donate', initiator, k_like, '=>', receiver)
			
		return False
		
	##### ##### VIZ ##### #####
	
	#VIZ => Sign:Wallet:Info:Reg:Del
					
	def vizsign(self, message):
		user_id, lng, keyboard, db = self.get_params_message(message, 'vizsign')
		wif = message["text"]
		
		### Проверка приватника
		try:
			public_key = self.viz.key.get_public_from_private(wif)
			accounts = self.viz.get_key_references(public_key)
			if accounts:
				account = accounts[0]
				self.viz_change_db(db, 'vizaccount', [account, wif])
				msg = account + self.bot_msg.AccountAppend[lng]
			else:
				# Принудительный переход на ветку vizlogin
				db["payload"]["vizkey"] = {"private": wif, "public": public_key}
				keyboard = self.goto_level(db, 'vizlogin')
				msg = self.bot_msg.InputLogin[lng]
		except:
			msg = self.bot_msg.KeyNotPrivate[lng]
			
		self.tg.send_message(user_id, msg, reply_markup=keyboard)
		
	def vizlogin(self, message):
		user_id, lng, keyboard, db = self.get_params_message(message, 'vizlogin')
		account = message["text"].lower()
		
		public_key = db["payload"]["vizkey"]["public"]
		wif = db["payload"]["vizkey"]["private"]
	
		### Проверка ключа
		if self.viz.check_posting_key(account, public_key):
			db["payload"].pop("vizkey")
			self.viz_change_db(db, 'vizaccount', [account, wif])
			msg = account + self.bot_msg.AccountAppend[lng]
		else:
			msg = self.bot_msg.KeyNotIdentified[lng]
			
		self.tg.send_message(user_id, msg, reply_markup=keyboard)

	def vizwallet(self, message):
		user_id, lng, keyboard, db = self.get_params_message(message, 'vizwallet')
		wallet = message["text"].lower()
		
 		### Проверка логина
		if self.viz.check_login(wallet):
			if self.viz.check_account(wallet):
				self.viz_change_db(db, 'vizwallet', wallet)
				msg = wallet + self.bot_msg.AccountAppend[lng]
			else:
				msg = wallet + self.bot_msg.NotExists[lng]
		else:
			msg = self.bot_msg.InvalidLogin[lng] + wallet
			
		self.tg.send_message(user_id, msg, reply_markup=keyboard)
		
	def vizinfo(self, message):
		user_id, lng, keyboard, db = self.get_params_message(message, 'vizinfo')
	
		vizaccount = db.get("vizaccount", None)
		if vizaccount:
			account, wif = vizaccount.split(':')
			wallet = db["vizwallet"]
			
			#chats = self.get_chats(db.get("vizchat", []))
			
			tx = self.viz.get_accounts([account])[0]
			try:
				VIZ, VP, TIP, POWER = [' '.join([str(int(tx[cmd])), cmd]) for cmd in ['VIZ', 'VP', 'TIP', 'POWER']]
				claim_idleness, CLAIM = str(round(tx["POWER"] / 100, 2)) + '%', TIP.replace('TIP', 'CLAIM')
				msg = '\n'.join([
								' '.join([account, wif[:5] + '***']),
								', '.join([VIZ, VP]),
								' '.join([CLAIM, '<=', claim_idleness]),
								' '.join(['for donate: ', TIP]),
								' '.join(['Wallet:', wallet]),
								#''.join(['Groups:\n'] + [chat + '\n' for chat in chats]),
								])
			except:
				msg = '\n'.join([' '.join([account, wif[:5] + '***']), 'error data'])
		
		else:
			wallet = db.get("vizwallet", None)
			if wallet:
				tx = self.viz.get_accounts([wallet])[0]
				try:
					VIZ, VP, TIP = [' '.join([str(int(tx[cmd])), cmd]) for cmd in ['VIZ', 'VP', 'TIP']]
					msg = '\n'.join([
									' '.join(['Wallet:', wallet]),
									', '.join([VIZ, VP]),
									' '.join(['for donate: ', TIP]),
									])
				except:
					msg = '\n'.join([' '.join([wallet, '***']), 'error data'])
			else:
				msg = self.bot_msg.ProfileMissing[lng]
			
		self.tg.send_message(user_id, msg, reply_markup=keyboard)
		
	def vizclaimnow(self, message):
		user_id, lng, keyboard, db = self.get_params_message(message, 'viz')
	
		msg = 'error, not try again'
		vizaccount = db.get("vizaccount", None)
		if vizaccount:
			account, wif = vizaccount.split(':')
			wallet = db["vizwallet"]
			
			tx = self.viz.get_accounts([account])[0]
			
			CLAIM = int(tx["TIP"])
			if CLAIM > 0:
				tx = self.viz.award(account, wallet, tx["POWER"], wif, memo='claim')
				if tx:
					msg = ', '.join(['CLAIMNOW', account, str(CLAIM) + ' VIZ', '=>', wallet])
					print(self.maska, msg)
					
		self.tg.send_message(user_id, msg, reply_markup=keyboard)
		
	def vizreg(self, message):
		user_id, lng, keyboard, db = self.get_params_message(message, 'vizreg')
		
		account = message["text"].lower()
		
		### Проверка регистрации
		reg = db.get("vizreg", None)
		if not reg:
			### Проверка логина
			if self.viz.check_login(account):
				if self.viz.check_account(account):
					msg = account + self.bot_msg.AlreadyExists[lng]
				else:
					db["level"] = "vizregYN"
					keyboard = self.bot_menu.state["vizregYN"]["keyboard"]

					seed = str(user_id) + str(time())
					password = 'P' + self.viz.key.get_keys(account, seed)["private"]["active"]
					parole = self.viz.key.get_keys(account, password)
					keys = '\n'.join([role + ':\n' + parole["private"][role] for role in ["regular", "active", "memo", "master"]])
					
					msg = self.bot_msg.ToRegister[lng] + account + '\n' + keys
					
					db["payload"]["vizreg"] = {"account": account, "password": password}
				
			else:
				msg = self.bot_msg.InvalidLogin[lng] + account
		else:
			parole = self.viz.key.get_keys(reg["account"], reg["password"])
			user_keys = '\n'.join([role + ':\n' + parole["private"][role] for role in ["regular", "active", "memo", "master"]])
			msg = self.bot_msg.AlreadyRegistered[lng] + reg["account"] + '\n' + user_keys
			
		self.tg.send_message(user_id, msg, reply_markup=keyboard)
		
	def vizregyes(self, message):
		user_id, lng, keyboard, db = self.get_params_message(message, 'viz')
	
		account = db["payload"]["vizreg"]["account"]
		password = db["payload"]["vizreg"]["password"]
		
		print(self.maska, user_id, account, 'registry VIZ')
		
		tx = self.viz.account_create(account, password, self.viz_reg_bot, self.viz_reg_wif, delegation=True)
		
		if tx:
			self.viz.delegate_vesting_shares(account, 0, self.viz_reg_bot, self.viz_reg_wif)	# Отзыв СВ сразу
			
			vizaccount = db.get("vizaccount", None)
			if not vizaccount:
				parole = self.viz.key.get_keys(account, password)
				wif = parole["private"]["regular"]
				self.viz_change_db(db, 'vizaccount', [account, wif])
				
			db["payload"].pop("vizreg")
			self.viz_change_db(db, 'vizreg', [account, password])
			msg = account + self.bot_msg.Registered[lng] + '\n'
		else:
			msg = account + self.bot_msg.FailedRegister[lng]
			
		self.tg.send_message(user_id, msg, reply_markup=keyboard)
					
	def vizdelyes(self, message):
		user_id, lng, keyboard, db = self.get_params_message(message, 'viz')
	
		vizaccount = db.get("vizaccount", None)
		wallet = db.get("vizwallet", None)
		
		if vizaccount or wallet:
			print(self.maska, user_id, vizaccount, 'vizdelete')
			self.viz_change_db(db, 'vizdelete', '')
			msg = self.bot_msg.ProfileDeleted[lng]
		else:
			msg = self.bot_msg.NoProfile[lng]
		
		self.tg.send_message(user_id, msg, reply_markup=keyboard)
					
	##### ##### ##### ##### #####
	
	def viz_change_db(self, db, type, payload):
	
		if type == 'vizaccount':	#54321 вывести отдельно с проверкой дубля акка в БД общей
			account, wif = payload
			acc = ':'.join([account, wif])
			db["vizaccount"] = acc
			db["vizwallet"] = account
			
		if type == 'vizwallet':
			wallet = payload
			db["vizwallet"] = wallet			
	
		if type == 'vizdelete':
			for cmd in ['vizaccount', 'vizwallet', 'vizchat']:
				if cmd in db: db.pop(cmd)
			
		if type == 'vizreg':
			account, password = payload
			db["vizreg"] = {"account": account, "password": password}
			
		self.bot_menu.save()
		
	def goto_level(self, db, type):
	
		keyboard = self.bot_menu.state[type]["keyboard"]
		db["level"] = type
		self.bot_menu.save()
		return keyboard
			
	##### ##### ##### ##### #####
