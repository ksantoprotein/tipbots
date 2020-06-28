# -*- coding: utf-8 -*-
# Depended Library

import json
from pprint import pprint
from time import sleep, time

class Golos():

	##### ##### DONATE ##### #####
	
	def golos_donate(self, initiator, k_like, title, reply_text, receiver, wif, **kwargs):
	
		payload = self.golos.get_accounts([initiator])[0]
		comment = kwargs.get("comment", '')
		try:
			TIP = payload["TIP"]
			amount = kwargs.get("amount", 0)
			if amount == 0: amount = round(k_like * TIP / 100, 3)
			if (TIP > 0) and (TIP >= amount > 0):
				balance = int(TIP - amount)
				todo = ''
				
				author_from_permlink, permlink = self.get_permlink_from_reply_text(reply_text)
				author_from_url, url = self.get_url_from_reply_text(reply_text)
				
				if permlink:
					receiver, todo = author_from_permlink, ' to ' + author_from_permlink
					memo = {
							"app": 'golos-id',
							"version": 1,
							"target": {"author": author_from_permlink, "permlink": permlink},				
							"comment": 'tip23bot ' + comment,
							}
				elif url:
					receiver, todo = author_from_url, ' to ' + author_from_url
					memo = {
							"app": 'www',
							"version": 1,
							"target": {"author": author_from_url, "permlink": url},				
							"comment": url + ' tip23bot ' + comment,
							}
				else:
					comment = reply_text[:250]
					memo = {
							"app": 'tip23',
							"version": 1,
							"target": {"title": title},				
							"comment": comment,
							}
						
				tx = self.golos.donate(initiator, receiver, amount, wif, memo=memo)		
				if tx:
					pool = ''.join(['(', str(balance), ')'])
					msg = [str(amount), ' GOLOS, ' + pool + todo]
					return msg
			else:
				print('ERROR tip', initiator, k_like, '=>', receiver)
		except:
			print('ERROR golos_donate', initiator, k_like, '=>', receiver)
			
		return False
		
	def get_permlink_from_reply_text(self, reply_text):
		lines = reply_text.split()
		#print(lines)
		for line in lines:
			if ('golos.in' in reply_text) or ('golos.id' in line) or ('golos.today' in line):
				return self.golos.resolve_url(line)
		return([False, False])
				
	def get_url_from_reply_text(self, reply_text):
		lines = reply_text.split()
		authors = []
		for line in lines:
			if 'https://' == line[:8]:
				url = line
				response = self.golos.rpc.http.get(url, timeout=3)
				if response.ok:
					for res in response.text.split('\n'):
						for metka in res.split():
							if 'GOLOS:' in metka:
								raw = metka.split('GOLOS:')[1]
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
			print(authors[0])
			return authors[0]
		return([False, False])
				
	##### ##### GOLOS ##### #####
	
	#GOLOS => Sign:Wallet:Info:Claim:Reg:Del
					
	def golossign(self, message):
		user_id, lng, keyboard, db = self.get_params_message(message, 'golossign')
		wif = message["text"]
		
		### Проверка приватника
		try:
			public_key = self.golos.key.get_public_from_private(wif)
			accounts = self.golos.get_key_references(public_key)
			if accounts:
				account = accounts[0]
				self.change_db(db, 'golosaccount', [account, wif])
				msg = account + self.bot_msg.AccountAppend[lng]
			else:
				# Принудительный переход на ветку goloslogin
				db["payload"]["goloskey"] = {"private": wif, "public": public_key}
				keyboard = self.goto_level(db, 'goloslogin')
				msg = self.bot_msg.InputLogin[lng]
		except:
			msg = self.bot_msg.KeyNotPrivate[lng]
			
		self.tg.send_message(user_id, msg, reply_markup=keyboard)
		
	def goloslogin(self, message):
		user_id, lng, keyboard, db = self.get_params_message(message, 'goloslogin')
		account = message["text"].lower()
		
		public_key = db["payload"]["goloskey"]["public"]
		wif = db["payload"]["goloskey"]["private"]
	
		### Проверка ключа
		if self.golos.check_posting_key(account, public_key):
			db["payload"].pop("goloskey")
			self.change_db(db, 'golosaccount', [account, wif])
			msg = account + self.bot_msg.AccountAppend[lng]
		else:
			msg = self.bot_msg.KeyNotIdentified[lng]
			
		self.tg.send_message(user_id, msg, reply_markup=keyboard)

	def goloswallet(self, message):
		user_id, lng, keyboard, db = self.get_params_message(message, 'goloswallet')
		wallet = message["text"].lower()
		
 		### Проверка логина
		if self.golos.check_login(wallet):
			if self.golos.check_account(wallet):
				self.change_db(db, 'goloswallet', wallet)
				msg = wallet + self.bot_msg.AccountAppend[lng]
			else:
				msg = wallet + self.bot_msg.NotExists[lng]
		else:
			msg = self.bot_msg.InvalidLogin[lng] + wallet
			
		self.tg.send_message(user_id, msg, reply_markup=keyboard)
		
	def golosinfo(self, message):
		user_id, lng, keyboard, db = self.get_params_message(message, 'golosinfo')
	
		golosaccount = db.get("golosaccount", None)
		if golosaccount:
			account, wif = golosaccount.split(':')
			wallet = db["goloswallet"]
			
			#chats = self.get_chats(db.get("goloschat", []))
			
			tx = self.golos.get_accounts([account])[0]
			try:
				GOLOS, GBG, GP, CLAIM, TIP = [' '.join([str(int(tx[cmd])), cmd]) for cmd in ['GOLOS', 'GBG', 'GP', 'CLAIM', 'TIP']]
				claim_idleness = str(tx["claim_idleness"]) + '%'
				db["payload"]["claim"] = int(tx["CLAIM"])
				msg = '\n'.join([
								' '.join([account, wif[:5] + '***']),
								', '.join([GOLOS, GBG, GP]),
								' '.join([CLAIM, '<=', claim_idleness]),
								' '.join(['for donate: ', TIP]),
								' '.join(['Wallet:', wallet]),
								#''.join(['Groups:\n'] + [chat + '\n' for chat in chats]),
								])
			except:
				db["payload"]["claim"] = 0
				msg = '\n'.join([' '.join([account, wif[:5] + '***']), 'error data'])
		
		else:
			wallet = db.get("goloswallet", None)
			if wallet:
				tx = self.golos.get_accounts([wallet])[0]
				try:
					GOLOS, GBG, GP, CLAIM, TIP = [' '.join([str(int(tx[cmd])), cmd]) for cmd in ['GOLOS', 'GBG', 'GP', 'CLAIM', 'TIP']]
					claim_idleness = str(tx["claim_idleness"]) + '%'
					msg = '\n'.join([
									' '.join(['Wallet:', wallet]),
									', '.join([GOLOS, GBG, GP]),
									' '.join([CLAIM, '<=', claim_idleness]),
									' '.join(['for donate: ', TIP]),
									])
				except:
					msg = '\n'.join([' '.join([wallet, '***']), 'error data'])
			else:
				msg = self.bot_msg.ProfileMissing[lng]
			
		self.tg.send_message(user_id, msg, reply_markup=keyboard)
		

	def golosclaimnow(self, message):
		user_id, lng, keyboard, db = self.get_params_message(message, 'golos')
	
		msg = 'error, not try again'
		golosaccount = db.get("golosaccount", None)
		if golosaccount:
			account, wif = golosaccount.split(':')
			wallet = db["goloswallet"]
			
			CLAIM = db["payload"].get("claim", 0)
			if CLAIM > 0:
				tx = self.golos.claim(account, wallet, wif, balance=CLAIM)
				if tx:
					msg = ', '.join(['CLAIMNOW', account, str(CLAIM) + ' GOLOS', '=>', wallet])
					print(self.maska, msg)
					db["payload"]["claim"] = 0
					
		self.tg.send_message(user_id, msg, reply_markup=keyboard)

		
	def golosreg(self, message):
		user_id, lng, keyboard, db = self.get_params_message(message, 'golosreg')
		
		account = message["text"].lower()
		
		### Проверка регистрации
		reg = db.get("golosreg", None)
		if not reg:
			### Проверка логина
			if self.golos.check_login(account):
				if self.golos.check_account(account):
					msg = account + self.bot_msg.AlreadyExists[lng]
				else:
					db["level"] = "golosregYN"
					keyboard = self.bot_menu.state["golosregYN"]["keyboard"]

					seed = str(user_id) + str(time())
					password = 'P' + self.golos.key.get_keys(account, seed)["private"]["active"]
					parole = self.golos.key.get_keys(account, password)
					keys = '\n'.join([role + ':\n' + parole["private"][role] for role in ["posting", "active", "memo", "owner"]])
					
					msg = self.bot_msg.ToRegister[lng] + account + '\n' + keys
					
					db["payload"]["golosreg"] = {"account": account, "password": password}
				
			else:
				msg = self.bot_msg.InvalidLogin[lng] + account
		else:
			parole = self.golos.key.get_keys(reg["account"], reg["password"])
			user_keys = '\n'.join([role + ':\n' + parole["private"][role] for role in ["posting", "active", "memo", "owner"]])
			msg = self.bot_msg.AlreadyRegistered[lng] + reg["account"] + '\n' + user_keys
			
		self.tg.send_message(user_id, msg, reply_markup=keyboard)
		

	def golosregyes(self, message):
		user_id, lng, keyboard, db = self.get_params_message(message, 'golos')
	
		account = db["payload"]["golosreg"]["account"]
		password = db["payload"]["golosreg"]["password"]
		
		print(self.maska, user_id, account, 'registry GOLOS')
		
		
		#tx = self.golos.account_create(account, password, self.golos_reg_bot, self.golos_reg_wif, fee=self.golos_reg_fee, referral=self.golos_reg_bot)
		tx = self.golos.account_create_with_delegation(account, password, self.golos_reg_bot, self.golos_reg_wif, fee=self.golos_reg_fee, referral=self.golos_reg_bot)
		
		if tx:
			#self.golos.delegate_vesting_shares(account, 0, self.golos_reg_bot, self.golos_reg_wif)	# Отзыв СГ сразу
			
			golosaccount = db.get("golosaccount", None)
			if not golosaccount:
				parole = self.golos.key.get_keys(account, password)
				wif = parole["private"]["posting"]
				self.change_db(db, 'golosaccount', [account, wif])
				
			db["payload"].pop("golosreg")
			self.change_db(db, 'golosreg', [account, password])
			msg = account + self.bot_msg.Registered[lng] + '\n'
		else:
			msg = account + self.bot_msg.FailedRegister[lng]
			
		self.tg.send_message(user_id, msg, reply_markup=keyboard)
		
		
	def golosdelyes(self, message):
		user_id, lng, keyboard, db = self.get_params_message(message, 'golos')
	
		golosaccount = db.get("golosaccount", None)
		wallet = db.get("goloswallet", None)
		
		if golosaccount or wallet:
			print(self.maska, user_id, golosaccount, 'golosdelete')
			self.change_db(db, 'golosdelete', '')
			msg = self.bot_msg.ProfileDeleted[lng]
		else:
			msg = self.bot_msg.NoProfile[lng]
		
		self.tg.send_message(user_id, msg, reply_markup=keyboard)
					
	##### ##### CLAIM ##### #####
	
	#CLAIM => Login:Info:Del
	
	def golosclaimlogin(self, message):
		user_id, lng, keyboard, db = self.get_params_message(message, 'golosclaimlogin')
		account = message["text"].lower()
		
		wallet = db.get("goloswallet", None)
		if wallet:
			### Проверка логина
			for_claim = [login.split(':')[0] for login in db.get("golosclaim", [])]
			if account not in for_claim:
				if self.golos.check_login(account):
					if self.golos.check_account(account):
						db["payload"]["golosclaimlogin"] = account
						keyboard = self.goto_level(db, 'golosclaimwif')
						msg = self.bot_msg.InputWif[lng]
					else:
						msg = account + self.bot_msg.NotExists[lng]
				else:
					msg = self.bot_msg.InvalidLogin[lng] + account
			else:
				msg = account + self.bot_msg.AlreadyExists[lng]
		else:
			msg = self.bot_msg.ProfileMissing[lng]
			
		self.tg.send_message(user_id, msg, reply_markup=keyboard)
		
	def golosclaimwif(self, message):
		user_id, lng, keyboard, db = self.get_params_message(message, 'golosclaimwif')
		wif = message["text"]

		account = db["payload"]["golosclaimlogin"]
	
		### Проверка приватника
		try:
			public_key = self.golos.key.get_public_from_private(wif)
			### Проверка ключа
			if self.golos.check_posting_key(account, public_key):
				db["payload"].pop("golosclaimlogin")
				self.change_db(db, 'golosclaim', [account, wif])
				keyboard = self.goto_level(db, 'golosclaimlogin')
				msg = account + self.bot_msg.AccountAppend[lng]
			else:
				msg = self.bot_msg.KeyNotIdentified[lng]
		except:
			msg = self.bot_msg.KeyNotPrivate[lng]
			
		self.tg.send_message(user_id, msg, reply_markup=keyboard)
		
	def golosclaiminfo(self, message):
		user_id, lng, keyboard, db = self.get_params_message(message, 'golosclaiminfo')
	
		accounts = db.get("golosclaim", [])
		info = [account.split(':')[0] for account in accounts]
		
		msg = '\n'.join(['for claim:'] + sorted(info))
		
		self.tg.send_message(user_id, msg, reply_markup=keyboard)	

	def golosclaimdel(self, message):
		user_id, lng, keyboard, db = self.get_params_message(message, 'golosclaimdel')
		account = message["text"].lower()
	
		accounts = db.get("golosclaim", [])
		logins = [account.split(':')[0] for account in accounts]
		if account in logins:
			i = logins.index(account)
			db["golosclaim"].pop(i)
			self.change_db(db, 'golosclaimdel', account)
			self.del_claim(account)	# => class Claim
			msg = account + self.bot_msg.LoginDeleted[lng]
		else:
			msg = account + self.bot_msg.NotExists[lng]
		
		self.tg.send_message(user_id, msg, reply_markup=keyboard)

	##### ##### ##### ##### #####
	
	def change_db(self, db, type, payload):
	
		if type == 'golosaccount':	#54321 вывести отдельно с проверкой дубля акка в БД общей
			account, wif = payload
			acc = ':'.join([account, wif])
			db["golosaccount"] = acc
			db["goloswallet"] = account
			db.setdefault("golosclaim", [])
			db["golosclaim"].append(acc)
			
		if type == 'goloswallet':
			wallet = payload
			db["goloswallet"] = wallet			
	
		if type == 'golosdelete':
			accounts = db.get("golosclaim", [])
			for account in accounts:
				self.del_claim(account.split(':')[0])	# => class Claim
			for cmd in ['golosaccount', 'goloswallet', 'goloschat', 'golosclaim']:
				if cmd in db: db.pop(cmd)
			
		if type == 'golosclaim':
			account, wif = payload
			acc = ':'.join([account, wif])
			db.setdefault("golosclaim", [])
			db["golosclaim"].append(acc)
			
		if type == 'golosreg':
			account, password = payload
			db["golosreg"] = {"account": account, "password": password}
			
		if type == 'golosclaimdel':
			pass
			
		self.bot_menu.save()
		
	def goto_level(self, db, type):
	
		keyboard = self.bot_menu.state[type]["keyboard"]
		db["level"] = type
		self.bot_menu.save()
		return keyboard
			
	##### ##### ##### ##### #####
	
class Claim():

	file_claim = 'claim.json'

	def del_claim(self, login):
		if login in self.state_claim:
			self.state_claim.pop(login)
			self.save_claim()

	def load_claim(self):
		try:
			with open(self.file_claim, 'r', encoding='utf8') as f:
				self.state_claim = json.load(f)
		except:
			# not exist
			self.state_claim = {}
			self.save_claim()
	
	def save_claim(self):
		with open(self.file_claim, 'w', encoding='utf8') as f:
			json.dump(self.state_claim, f, ensure_ascii=False)
		
	def check_claim(self):
	
		self.load_claim()
		new_claims = []
		n = 10	#54321
		
		for user_id, db in self.bot_menu.users_tg.items():
			wallet = db.get("goloswallet", None)
			if wallet:
				
				accounts = db.get("golosclaim", [])
				for account in accounts:
					login, wif = account.split(':')
					if login not in self.state_claim:
						new_claims.append([login, wif, wallet, 0, user_id])					#добавляем новеньких
					else:
						bd = self.state_claim[login]
						if wallet != bd["wallet"]: bd["wallet"] = wallet					#смена кошелька если требуется
						if user_id != bd["user_id"]: bd["user_id"] = user_id				#смена user_id если требуется
						if (bd["claim_idleness"] >= 50) or (int(time()) - bd["timestamp"]) > 60*60*12:
							if bd["error"] < 5:	#54321
								new_claims.append([login, bd["wif"], bd["wallet"], bd["error"], bd["user_id"]])	#добавляем стареньких
							else:
								pass
								#сделать удаление из общего стейта с оповещением
					
		for login, wif, wallet, error, user_id in new_claims[:n]:
			db = self.bot_menu.users_tg[user_id]		
			tx = self.golos.get_accounts([login])[0]
			try:
				GOLOS, GBG, GP, CLAIM, TIP, claim_idleness = [tx[cmd] for cmd in ['GOLOS', 'GBG', 'GP', 'CLAIM', 'TIP', 'claim_idleness']]
				timestamp = int(time())
				if CLAIM > 0:
					tx = self.golos.claim(login, wallet, wif, balance=CLAIM)
					if tx:
						msg = ', '.join(['CLAIM', login, str(CLAIM) + ' GOLOS', '=>', wallet])
						print(self.maska, msg)
						claim_idleness = 0
						
						report = db.get("report", True)
						if report: self.tg.send_message(user_id, msg)
					else:
						print('ERROR claim', login)	#54321 сохранять в логах
						error += 1
				else:
					print('not CLAIM', login, CLAIM, str(claim_idleness) + '%')
					if claim_idleness > 50: error += 1
					
				self.state_claim[login] = {	"wif": wif, "wallet": wallet, "claim_idleness": claim_idleness, "timestamp": timestamp, 
											"error": error, "user_id": user_id,}
				self.save_claim()
				
			except:
				print('ERROR check_claim', login)
			
			
	##### ##### ##### ##### #####
