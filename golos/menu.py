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
			
golosmenu =		{"label": 'GOLOS', "message": {		"Russian": 'Вы вошли в подменю токена GOLOS', 
													"English": 'You have entered the GOLOS token submenu'}}
golosreg =		{"label": 'Reg', "message": {		"Russian": 'Чтобы зарегистрировать аккаунт введите логин', 
													"English": 'To register an account, enter your login'}}
golosclaim =	{"label": 'Claim', "message": {		"Russian": 'Вы вошли в подменю авто claim', 
													"English": 'You have entered the auto claim submenu'}}
golosclaimnow =	{"label": 'ClaimNow', "message": {	"Russian": 'Снимаем дивиденды', 
													"English": 'Take dividends'}}
golosclaimdel =	{"label": 'Delete', "message": {	"Russian": 'Введите логин', 
													"English": 'Enter login'}}
			
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
								{"label": golosmenu["label"], "message": golosmenu["message"], "to_level": 'golos'},
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

		##### GOLOS #####
				
		"golos": {
					"action": 	[
								{"label": sign["label"], "message": sign["message"], "to_level": 'golossign'},
								{"label": wallet["label"], "message": wallet["message"], "to_level": 'goloswallet'},
								{"label": info["label"], "message": info["message"], "to_level": 'golosinfo', "row": True},
								{"label": golosclaim["label"], "message": golosclaim["message"], "to_level": 'golosclaim'},
								{"label": golosreg["label"], "message": golosreg["message"], "to_level": 'golosreg'},
								{"label": delprofile["label"], "message": delprofile["message"], "to_level": 'golosdelYN', "row": True},
								{"label": back["label"], "message": back["message"], "to_level": 'menu'},
								],
				},
				
		"golossign": {
					"action": 	[
								{"label": back["label"], "message": back["message"], "to_level": 'golos'},
								],
				},
				
		"goloslogin": {
					"action": 	[
								{"label": back["label"], "message": back["message"], "to_level": 'golos'},
								],
				},
				
		"goloswallet": {
					"action": 	[
								{"label": back["label"], "message": back["message"], "to_level": 'golos'},
								],
				},
				
		"golosinfo": {
					"action": 	[
								{"label": golosclaimnow["label"], "message": golosclaimnow["message"], "to_level": 'golos'},
								{"label": back["label"], "message": back["message"], "to_level": 'golos'},
								],
				},
				
		"golosclaim": {
					"action": 	[
								{"label": login["label"], "message": login["message"], "to_level": 'golosclaimlogin'},
								{"label": info["label"], "message": info["message"], "to_level": 'golosclaiminfo'},
								{"label": golosclaimdel["label"], "message": golosclaimdel["message"], "to_level": 'golosclaimdel'},
								{"label": back["label"], "message": back["message"], "to_level": 'golos'},
								],
				},
				
		"golosclaimlogin": {
					"action": 	[
								{"label": back["label"], "message": back["message"], "to_level": 'golosclaim'},
								],
				},
				
		"golosclaimwif": {
					"action": 	[
								{"label": back["label"], "message": back["message"], "to_level": 'golosclaim'},
								],
				},
				
		"golosclaiminfo": {
					"action": 	[
								{"label": back["label"], "message": back["message"], "to_level": 'golosclaim'},
								],
				},
				
		"golosreg": {
					"action": 	[
								{"label": back["label"], "message": back["message"], "to_level": 'golos'},
								],
				},
				
		"golosregYN": {
					"action": 	[
								{"label": 'Yes', "message": ok["message"], "to_level": 'golos'},	#golosreg
								{"label": 'No', "message": ok["message"], "to_level": 'golos'},
								],
				},
				
		"golosclaimdel": {
					"action": 	[
								{"label": back["label"], "message": back["message"], "to_level": 'golosclaim'},
								],
				},
				
		"golosdelYN": {
					"action": 	[
								{"label": 'Yes', "message": ok["message"], "to_level": 'golos'},
								{"label": 'No', "message": ok["message"], "to_level": 'golos'},
								],
				},
				
		}
		
	

