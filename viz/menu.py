# -*- coding: utf-8 -*-

import json
from pprint import pprint

botmenu =		{"label": 'Menu', "message": {		"Russian": 'Вы вошли в меню', 
													"English": 'You are in the menu'}}
help = 			{"label": 'Help', "message": {		"Russian": 'Вы вошли в подменю помощи', 
													"English": 'You are in the help menu'}}
helpintro =		{"label": 'Intro', "message": {		"Russian": 'Введение', 
													"English": 'Intro'}}
helpreg =		{"label": 'Reg', "message": {		"Russian": 'Регистрация', 
													"English": 'Registration'}}
setting = 		{"label": 'Setting', "message": {	"Russian": 'Вы вошли в подменю настроек', 
													"English": 'You have entered the settings submenu'}}
language = 		{"label": 'Language', "message": {	"Russian": 'Выберите язык', 
													"English": 'Choose language'}}
report = 		{"label": 'Report', "message": {	"Russian": 'Выберите параметры отчета', 
													"English": 'Choose type report'}}

sign =			{"label": 'Sign', "message": {		"Russian": 'Введите приватный постинг ключ', 
													"English": 'Enter private posting key'}}
wallet =		{"label": 'Wallet', "message": {	"Russian": 'Введите ваш кошелек', 
													"English": 'Enter your wallet'}}
login =			{"label": 'Login', "message": {		"Russian": 'Введите ваш логин', 
													"English": 'Enter your login'}}
info =			{"label": 'Info', "message": {		"Russian": 'Выводим текущую информацию', 
													"English": 'Display current information'}}
delprofile =	{"label": 'Del', "message": {		"Russian": 'Вы уверены, что хотите отключить ваш аккаунт?', 
													"English": 'Are you sure you want to disable your account?'}}
claimnow =		{"label": 'ClaimNow', "message": {	"Russian": 'Снимаем дивиденды', 
													"English": 'Take dividends'}}
			
vizmenu =		{"label": 'VIZ', "message": {		"Russian": 'Вы вошли в подменю токена VIZ', 
													"English": 'You have entered the VIZ token submenu'}}
vizreg =		{"label": 'Reg', "message": {		"Russian": 'Чтобы зарегистрировать аккаунт введите логин', 
													"English": 'To register an account, enter your login'}}
vizsign =		{"label": 'Sign', "message": {		"Russian": 'Введите приватный регулярный ключ', 
													"English": 'Enter private regular key'}}

back = 		{"label": 'Back', "message": {"Russian": 'Возвращаемся в меню', "English": 'Go back to the menu'}}
ok = 		{"message": {"Russian": 'Окай', "English": 'Ok'}}
			

menu = {
		"setdefault": {
					"action": 	[
								{"label": botmenu["label"], "message": botmenu["message"], "to_level": 'menu'},
								{"label": setting["label"], "message": setting["message"], "to_level": 'setting', "row": True},
								{"label": help["label"], "message": help["message"], "to_level": 'help'},
								],
				},
		"start": {
					"action": 	[
								{"label": botmenu["label"], "message": botmenu["message"], "to_level": 'menu'},
								{"label": setting["label"], "message": setting["message"], "to_level": 'setting', "row": True},
								{"label": help["label"], "message": help["message"], "to_level": 'help'},
								],
				},
		"menu": {
					"action": 	[
								{"label": vizmenu["label"], "message": vizmenu["message"], "to_level": 'viz'},
								{"label": back["label"], "message": back["message"], "to_level": 'start'},
								],
				},
		"setting": {
					"action": 	[
								{"label": language["label"], "message": language["message"], "to_level": 'language'},
								{"label": report["label"], "message": report["message"], "to_level": 'report'},
								{"label": back["label"], "message": back["message"], "to_level": 'start'},
								],
				},

		"language": {
					"action": 	[
								{"label": 'Russian', "message": ok["message"], "to_level": 'setting'},
								{"label": 'English', "message": ok["message"], "to_level": 'setting'},
								{"label": back["label"], "message": back["message"], "to_level": 'setting'},
								],
				},
				
		"report": {
					"action": 	[
								{"label": 'On', "message": ok["message"], "to_level": 'setting'},
								{"label": 'Off', "message": ok["message"], "to_level": 'setting'},
								{"label": back["label"], "message": back["message"], "to_level": 'setting'},
								],
				},
				
		"help": {
					"action": 	[
								{"label": helpintro["label"], "message": helpintro["message"], "to_level": 'start'},
								{"label": helpreg["label"], "message": helpreg["message"], "to_level": 'start'},
								{"label": back["label"], "message": back["message"], "to_level": 'start'},
								],
				},

		##### VIZ #####
				
		"viz": {
					"action": 	[
								{"label": vizsign["label"], "message": vizsign["message"], "to_level": 'vizsign'},
								{"label": wallet["label"], "message": wallet["message"], "to_level": 'vizwallet'},
								{"label": info["label"], "message": info["message"], "to_level": 'vizinfo'},
								{"label": vizreg["label"], "message": vizreg["message"], "to_level": 'vizreg'},
								{"label": delprofile["label"], "message": delprofile["message"], "to_level": 'vizdelYN', "row": True},
								{"label": back["label"], "message": back["message"], "to_level": 'menu'},
								],
				},
				
		"vizsign": {
					"action": 	[
								{"label": back["label"], "message": back["message"], "to_level": 'viz'},
								],
				},
				
		"vizlogin": {
					"action": 	[
								{"label": back["label"], "message": back["message"], "to_level": 'viz'},
								],
				},
				
		"vizwallet": {
					"action": 	[
								{"label": back["label"], "message": back["message"], "to_level": 'viz'},
								],
				},
				
		"vizinfo": {
					"action": 	[
								{"label": claimnow["label"], "message": claimnow["message"], "to_level": 'viz'},
								{"label": back["label"], "message": back["message"], "to_level": 'viz'},
								],
				},
				
		"vizreg": {
					"action": 	[
								{"label": back["label"], "message": back["message"], "to_level": 'viz'},
								],
				},
				
		"vizregYN": {
					"action": 	[
								{"label": 'Yes', "message": ok["message"], "to_level": 'vizreg'},
								{"label": 'No', "message": ok["message"], "to_level": 'viz'},
								],
				},
				
		"vizdelYN": {
					"action": 	[
								{"label": 'Yes', "message": ok["message"], "to_level": 'viz'},
								{"label": 'No', "message": ok["message"], "to_level": 'viz'},
								],
				},
				
		}
		
	

