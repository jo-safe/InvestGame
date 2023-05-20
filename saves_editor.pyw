import os
import re
import win32clipboard as clb
import wx
from wx.adv import Sound
from wx.lib.mixins.listctrl import TextEditMixin as TEList

VERSION="v_1.4.1"

INDUSTRIAL_VALUES=['None', 
				   'Major Banks', 
				   'Regional Banks', 
				   'Investment Services', 
				   'Computer Hardware', 
				   'Oil & Gas Operations', 
				   'Auto & Truck Manufacturers', 
				   'Telecommunications services', 
				   'Discount Stores', 
				   'Semiconductors', 
				   'Diversified Insurance', 
				   'Software & Programming', 
				   'Computer Services', 
				   'Life & Health Insurance', 
				   'Medical Equipment & Supplies', 
				   'Food Processing', 
				   'Broadcasting & Cable', 
				   'Household/Personal Care', 
				   'Managed Health Care', 
				   'Pharmaceuticals', 
				   'Conglomerates', 
				   'Beverages', 
				   'Iron & Steel', 
				   'Drug Retail', 
				   'Communications Equipment', 
				   'Aerospace & Defense', 
				   'Diversified Chemicals', 
				   'Consumer Financial Services', 
				   'Electric Utilities', 
				   'Home Improvement Retail', 
				   'Construction Services', 
				   'Electronics', 
				   'Biotechs', 
				   'Trading Companies', 
				   'Healthcare Services', 
				   'Air Courier', 
				   'Heavy Equipment', 
				   'Property & Casualty Insurance', 
				   'Diversified Metals & Mining', 
				   'Airline', 
				   'Railroads', 
				   'Business & Personal Services', 
				   'Oil Services & Equipment', 
				   'Tobacco', 
				   'Real Estate', 
				   'Restaurants', 
				   'Consumer Electronics', 
				   'Auto & Truck Parts', 
				   'Apparel/Accessories', 
				   'Food Retail', 
				   'Computer Storage Devices', 
				   'Internet & Catalog Retail', 
				   'Electrical Equipment', 
				   'Business Products & Supplies', 
				   'Construction Materials', 
				   'Precision Healthcare Equipment', 
				   'Natural Gas Utilities', 
				   'Advertising', 
				   'Other Transportation', 
				   'Apparel/Footwear Retail', 
				   'Hotels & Motels', 
				   'Specialized Chemicals', 
				   'Other Industrial Equipment', 
				   'Household Appliances', 
				   'Printing & Publishing', 
				   'Specialty Stores', 
				   'Insurance Brokers', 
				   'Paper & Paper Products', 
				   'Casinos & Gaming', 
				   'Furniture & Fixtures', 
				   'Department Stores', 
				   'Diversified Utilities', 
				   'Environmental & Waste', 
				   'Computer & Electronics Retail', 
				   'Aluminum', 'Recreational Products', 
				   'Security Systems', 
				   'Containers & Packaging', 
				   'Rental & Leasing', 
				   'Trucking', 
				   'Thrifts & Mortgage Finance', 
				   'Forest Products']

SECTOR_VALUES=['None',
			   'Metals', 
			   'Energies', 
			   'Grains', 
			   'Meats', 
			   'Softs']

COUNTRIES=['Австралия',
		   'Австрия',
		   'Азербайджан',
		   'Албания',
		   'Алжир',
		   'Ангола',
		   'Андорра',
		   'Антигуа и Барбуда',
		   'Аргентина',
		   'Армения',
		   'Афганистан',
		   'Багамы',
		   'Бангладеш',
		   'Барбадос',
		   'Бахрейн',
		   'Белоруссия',
		   'Белиз',
		   'Бельгия',
		   'Бенин',
		   'Бермудские острова',
		   'Болгария',
		   'Боливия',
		   'Босния и Герцеговина',
		   'Ботсвана',
		   'Бразилия',
		   'Бруней',
		   'Буркина-Фасо',
		   'Бурунди',
		   'Бутан',
		   'Вануату',
		   'Великобритания',
		   'Венгрия',
		   'Венесуэла',
		   'Восточный Тимор',
		   'Вьетнам',
		   'Габон',
		   'Гаити',
		   'Гайана',
		   'Гамбия',
		   'Гана',
		   'Гватемала',
		   'Гвинея',
		   'Гвинея-Бисау',
		   'Германия',
		   'Гондурас',
		   'Гренада',
		   'Греция',
		   'Грузия',
		   'Дания',
		   'Джибути',
		   'Доминика',
		   'Доминиканская Республика',
		   'Египет',
		   'Замбия',
		   'Зимбабве',
		   'Израиль',
		   'Индия',
		   'Индонезия',
		   'Иордания',
		   'Ирак',
		   'Иран',
		   'Ирландия',
		   'Исландия',
		   'Испания',
		   'Италия',
		   'Йемен',
		   'Кабо-Верде',
		   'Казахстан',
		   'Камбоджа',
		   'Камерун',
		   'Канада',
		   'Катар',
		   'Кения',
		   'Кипр',
		   'Киргизия',
		   'Кирибати',
		   'Китай',
		   'Колумбия',
		   'Коморы',
		   'Конго',
		   'ДР Конго',
		   'КНДР',
		   'Корея',
		   'Коста-Рика',
		   'Кот-д’Ивуар',
		   'Куба',
		   'Кувейт',
		   'Лаос',
		   'Латвия',
		   'Лесото',
		   'Либерия',
		   'Ливан',
		   'Ливия',
		   'Литва',
		   'Лихтенштейн',
		   'Люксембург',
		   'Маврикий',
		   'Мавритания',
		   'Мадагаскар',
		   'Малави',
		   'Малайзия',
		   'Мали',
		   'Мальдивы',
		   'Мальта',
		   'Марокко',
		   'Маршалловы Острова',
		   'Мексика',
		   'Микронезия',
		   'Мозамбик',
		   'Молдавия',
		   'Монако',
		   'Монголия',
		   'Мьянма',
		   'Намибия',
		   'Науру',
		   'Непал',
		   'Нигер',
		   'Нигерия',
		   'Нидерланды',
		   'Никарагуа',
		   'Новая Зеландия',
		   'Норвегия',
		   'ОАЭ',
		   'Оман',
		   'Пакистан',
		   'Палау',
		   'Панама',
		   'Папуа — Новая Гвинея',
		   'Парагвай',
		   'Перу',
		   'Польша',
		   'Португалия',
		   'Россия',
		   'Руанда',
		   'Румыния',
		   'Сальвадор',
		   'Самоа',
		   'Сан-Марино',
		   'Сан-Томе и Принсипи',
		   'Саудовская Аравия',
		   'Северная Македония',
		   'Сейшелы',
		   'Сенегал',
		   'Сент-Винсент и Гренадины',
		   'Сент-Китс и Невис',
		   'Сент-Люсия',
		   'Сербия',
		   'Сингапур',
		   'Сирия',
		   'Словакия',
		   'Словения',
		   'США',
		   'Соломоновы Острова',
		   'Сомали',
		   'Судан',
		   'Суринам',
		   'Сьерра-Леоне',
		   'Таджикистан',
		   'Таиланд',
		   'Танзания',
		   'Того',
		   'Тонга',
		   'Тринидад и Тобаго',
		   'Тувалу',
		   'Тунис',
		   'Туркмения',
		   'Турция',
		   'Уганда',
		   'Узбекистан',
		   'Украина',
		   'Уругвай',
		   'Фиджи',
		   'Филиппины',
		   'Финляндия',
		   'Франция',
		   'Хорватия',
		   'ЦАР',
		   'Чад',
		   'Черногория',
		   'Чехия',
		   'Чили',
		   'Швейцария',
		   'Швеция',
		   'Шри-Ланка',
		   'Эквадор',
		   'Экваториальная Гвинея',
		   'Эритрея',
		   'Эсватини',
		   'Эстония',
		   'Эфиопия',
		   'ЮАР',
		   'Южный Судан',
		   'Ямайка',
		   'Япония']

COMMODITIES={}

COMPANIES={}


class window(wx.Frame):
	def __init__(self, parent, title):
		super().__init__(parent=None, title="InvestGame Data Editor (" + VERSION + ")", pos=(100, 100), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)

		self.mainSizer=wx.BoxSizer()
		self.panel=panel(self)

		self.menuBar = wx.MenuBar()
		self.fileMenu = wx.Menu()

		self.itemCreate = self.fileMenu.Append(wx.ID_ANY, "Создать...\tCtrl+N", "Создать файл")
		self.itemOpen = self.fileMenu.Append(wx.ID_ANY, "Открыть...\tCtrl+O", "Открыть файл")
		self.itemSave = self.fileMenu.Append(wx.ID_ANY, "Сохранить...\tCtrl+S", "Сохранить файл")
		self.itemSaveAs = self.fileMenu.Append(wx.ID_ANY, "Сохранить как...\tCtrl+Shift+S", "Сохранить файл как")
		self.itemUpdate = self.fileMenu.Append(wx.ID_ANY, "Обновить\tF5", "Обновить данные")
		self.itemErrorsSearch = self.fileMenu.Append(wx.ID_ANY, "Поиск ошибок\tF9", "Поиск ошибок")
		self.itemProjectInfo = self.fileMenu.Append(wx.ID_ANY, "Информация о сохранении", "")
		self.itemVersionInfo = self.fileMenu.Append(wx.ID_ANY, "Версии", "")

		self.menuBar.Append(self.fileMenu, "&File")
		self.Bind(wx.EVT_MENU, self.onCreate, self.itemCreate)
		self.Bind(wx.EVT_MENU, self.onOpen, self.itemOpen)
		self.Bind(wx.EVT_MENU, self.onSave, self.itemSave)
		self.Bind(wx.EVT_MENU, self.onSaveAs, self.itemSaveAs)
		self.Bind(wx.EVT_MENU, self.onUpdate, self.itemUpdate)
		self.Bind(wx.EVT_MENU, self.onErrorsSearch, self.itemErrorsSearch)
		self.Bind(wx.EVT_MENU, self.showProjectInfo, self.itemProjectInfo)
		self.Bind(wx.EVT_MENU, self.showVersionInfo, self.itemVersionInfo)
		self.SetMenuBar(self.menuBar)
		
		self.mainSizer.Add(self.panel, flag=wx.EXPAND)

		self.SetSizerAndFit(self.mainSizer)

		self.Bind(wx.EVT_CLOSE, self.onClose, self)



	def onErrorsSearch(self, event):
		count=len(self.panel.stocks)*5 + len(self.panel.commodities)*3 + len(self.panel.globalNews) + len(self.panel.corporationNews) + len(self.panel.localNews)*2
		progressDialog=wx.ProgressDialog("Поиск ошибок...", "Подготовка...", count)
		
		self.panel.saveListData()
		errorsList=[]
		progressValue=0

		stocksTickers=[]
		commoditiesTickers=[]
		for item in self.panel.stocks:
			stocksTickers.append(item.ticker)
			progressValue+=1
			progressDialog.Update(progressValue)
		for item in self.panel.commodities:
			commoditiesTickers.append(item.ticker)
			progressValue+=1
			progressDialog.Update(progressValue)

		
		for item in self.panel.stocks:
			if not item.country in COUNTRIES:
				errorsList.append(str(progressValue))
				errorsList.append("Акция")
				errorsList.append(item.ticker)
				errorsList.append(item.company)
				errorsList.append("Неверно указана страна: \"" + item.country + "\"")
			progressValue+=1
			progressDialog.Update(progressValue, "Проверка страны акции \"" + item.company + "\"")
		
		for item in self.panel.stocks:
			if not item.industry in INDUSTRIAL_VALUES:
				errorsList.append(str(progressValue))
				errorsList.append("Акция")
				errorsList.append(item.ticker)
				errorsList.append(item.company)
				errorsList.append("Неверно указана индустрия: \"" + item.industry + "\"")
			progressValue+=1
			progressDialog.Update(progressValue, "Проверка индустрии акции \"" + item.company + "\"")
		
		for item in self.panel.stocks:
			for key, value in item.uses.items():
				if not key in stocksTickers or not key in commoditiesTickers:
					errorsList.append(str(progressValue))
					errorsList.append("Акция")
					errorsList.append(item.ticker)
					errorsList.append(item.company)
					errorsList.append("Неверно указан продукт использования: \"" + key + "\"")
				progressValue+=1
				progressDialog.Update(progressValue, "Проверка зависимостей акции \"" + item.company + "\"")
			for key, value in item.produces.items():
				if not key in stocksTickers or not key in commoditiesTickers:
					errorsList.append(str(progressValue))
					errorsList.append("Акция")
					errorsList.append(item.ticker)
					errorsList.append(item.company)
					errorsList.append("Неверно указан продукт потребления: \"" + key + "\"")
				progressValue+=1
				progressDialog.Update(progressValue, "Проверка зависимостей акции \"" + item.company + "\"")

		
		for item in self.panel.commodities:
			if not item.sector in SECTOR_VALUES:
				errorsList.append(str(progressValue))
				errorsList.append("Товар")
				errorsList.append(item.ticker)
				errorsList.append(item.name)
				errorsList.append("Неверно указан сектор: \"" + item.sector + "\"")
			progressValue+=1
			progressDialog.Update(progressValue, "Проверка сектора товара \"" + item.name + "\"")
		
		for item in self.panel.commodities:
			for key, value in item.influence.items():
				if not key in COUNTRIES:
					errorsList.append(str(progressValue))
					errorsList.append("Товар")
					errorsList.append(item.ticker)
					errorsList.append(item.name)
					errorsList.append("Неверно указана страна зависимости: \"" + key + "\"")
				progressValue+=1
				progressDialog.Update(progressValue, "Проверка зависимостей товара \"" + item.name + "\"")
		

		for item in self.panel.globalNews:
			for key, value in item.influence.items():
				if not key in stocksTickers or not key in commoditiesTickers:
					errorsList.append(str(progressValue))
					errorsList.append("Глобальная новость")
					errorsList.append(str(item.id))
					errorsList.append("")
					errorsList.append("Неверно указан товар/акция зависимости: \"" + key + "\"")
				progressValue+=1
				progressDialog.Update(progressValue, "Проверка зависимостей глобальной новости \"" + item.id + "\"")
		

		for item in self.panel.corporationNews:
			if not item.ticker in stocksTickers:
				errorsList.append(str(progressValue))
				errorsList.append("Корпоративная новость")
				errorsList.append(str(item.id))
				errorsList.append("")
				errorsList.append("Неверно указана акция: \"" + key + "\"")
			progressValue+=1
			progressDialog.Update(progressValue, "Проверка привязки корпоративной новости \"" + item.id + "\"")
		

		for item in self.panel.localNews:
			for key, value in item.influence.items():
				if not key in stocksTickers or not key in commoditiesTickers:
					errorsList.append(str(progressValue))
					errorsList.append("Локальная новость")
					errorsList.append(str(item.id))
					errorsList.append("")
					errorsList.append("Неверно указан товар/акция зависимости: \"" + key + "\"")
				progressValue+=1
				progressDialog.Update(progressValue, "Проверка зависимостей локальной новости \"" + item.id + "\"")

		if len(errorsList)==0:
			wx.MessageBox("Ошибки не обнаружены", "Ошибки не обнаружены", style=wx.OK, parent=self)
			return
		else:
			errorsWindow=self.ErrorsWindow(self, data=errorsList)
			errorsWindow.Show()
			
				

	class ErrorsWindow(wx.Frame):
		def __init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE, name=wx.FrameNameStr, data=[]):
			super().__init__(parent, id=id, title="Ошибки", pos=pos, size=size, style=style, name=name)

			self.panel=wx.Panel(self)

			self.errorsList=wx.ListCtrl(self.panel, size=(900, 350), style=wx.LC_REPORT)
			self.btContinue=wx.Button(self.panel, label="Продолжить")
			self.btSaveLog=wx.Button(self.panel, label="Сохранить log-файл")
			
			self.errorsList.InsertColumn(0, "Строка", width=60)
			self.errorsList.InsertColumn(1, "Тип", width=120)
			self.errorsList.InsertColumn(2, "Элемент", width=80)
			self.errorsList.InsertColumn(3, "Полное имя", width=200)
			self.errorsList.InsertColumn(4, "Комментарий", width=460)

			for index in range(len(data)):
				if index%5==0:
					self.errorsList.InsertItem(index//5, "")
				self.errorsList.SetItem(index//5, index%5, data[index])

			self.sizer=wx.GridBagSizer()
			self.sizer.Add(self.errorsList, pos=(0, 0), span=(1, 2))
			self.sizer.Add(self.btContinue, pos=(1, 0))
			self.sizer.Add(self.btSaveLog, pos=(1, 1))

			self.panel.SetSizerAndFit(self.sizer)


			self.boxSizer=wx.BoxSizer()
			self.boxSizer.Add(self.panel)
		
			self.SetSizerAndFit(self.boxSizer)


			self.Bind(wx.EVT_BUTTON, self.Continue, self.btContinue)
			self.Bind(wx.EVT_BUTTON, lambda event: self.saveLog(event, data=data), self.btSaveLog)


		def saveLog(self, event=None, data=[]):
			savesString=""
			for index in range(len(data)):
				if index%5==0:
					savesString+="\n"
				savesString+=data[index] + "\t"

			try:
				open(self.GetParent().panel.currentPath + ".log", "w", encoding="utf-8").write(savesString[1:])
			except BaseException as e:
				wx.MessageBox("Ошибка сохранения log-файла", "Ошибка сохранения log-файла", style=wx.OK, parent=self)


		def Continue(self, event=None):
			self.Destroy()


	def onUpdate(self, event):
		self.panel.saveListData()
		self.panel.updateCommoditiesAndCompanies()



	def onClose(self, event):
		if not self.panel.isSaved:
			dlg = wx.MessageDialog(self, 'Сохранить текущий документ?', style=wx.CANCEL | wx.YES_NO | wx.STAY_ON_TOP)
			res = dlg.ShowModal()
			if res==wx.ID_YES:
				if not self.onSave():
					return
			elif res==wx.ID_CANCEL:
				return
		self.Destroy()


	def changeTitle(self):
		title=self.GetTitle()[0:32]
		title+= "     " + self.panel.currentPath.split("\\")[-1]
		if not self.panel.isSaved:
			title+="*"
		self.SetTitle(title)


	def getSavesString(self, path):
		assets=""
		for asset in self.panel.stocks:
			assets+=asset.toString()+"\n"
		for asset in self.panel.commodities:
			assets+=asset.toString()+"\n"
		for asset in self.panel.globalNews:
			assets+=asset.toString()+"\n"
		for asset in self.panel.localNews:
			assets+=asset.toString()+"\n"
		for asset in self.panel.corporationNews:
			assets+=asset.toString()+"\n"
		assets += "dc\t" + self.panel.currencyEdit.GetValue() + "\ndd\t" + self.panel.dateEdit.GetValue() + "\n"
		return assets

	def onCreate(self, event=None):
		if not self.panel.isSaved:
			dlg = wx.MessageDialog(self, 'Сохранить текущий документ?', style=wx.CANCEL | wx.YES_NO | wx.STAY_ON_TOP)
			res = dlg.ShowModal()
			if res==wx.YES:
				self.onSave()
			elif res==wx.CANCEL:
				return
		self.panel.setDefaults()


	def onOpen(self, event=None):
		if not self.panel.isSaved:
			dlg = wx.MessageDialog(self, 'Сохранить текущий документ?', style=wx.CANCEL | wx.YES_NO | wx.STAY_ON_TOP)
			res = dlg.ShowModal()
			if res==wx.YES:
				self.onSave()
			elif res==wx.CANCEL:
				return
		with wx.FileDialog(self, "Открыть файл...", wildcard="Данные игры (*.mydata)|*.mydata", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
			if fileDialog.ShowModal() == wx.ID_CANCEL:
				 return 
			self.panel.setDefaults()
			self.panel.currentPath = fileDialog.GetPath()
			self.panel.isPathed=True
		self.panel.mainList.ClearAll()
		try:
			self.panel.readFromFile()
		except:
			wx.MessageBox('Ошибка чтения файла ' + self.panel.currentPath, "Ошибка", style=wx.OK | wx.ICON_ERROR, parent=self)
			return
		self.panel.loadList()
		self.panel.isSaved=True
		self.changeTitle()


	def onSave(self, event=None):
		self.panel.saveListData()
		if not self.panel.isPathed:
			with wx.FileDialog(self, "Сохранить документ...", wildcard="Данные игры (*.mydata)|*.mydata",style=wx.FD_SAVE) as fileDialog:
				fileDialog.ShowModal()
				if fileDialog.GetPath()!="":
					self.panel.currentPath=fileDialog.GetPath()
					self.panel.isPathed=True
				else:
					return False
		savesString=""
		flag=False
		try:
			savesString=self.getSavesString(self.panel.currentPath)
		except:
			wx.MessageBox('Ошибка генерации файла сохранения', "Ошибка", style=wx.OK | wx.ICON_ERROR, parent=self)
		try:
			open(self.panel.currentPath + "~", "w", encoding="utf-8").write(savesString[:-1])
		except:
			wx.MessageBox('Ошибка сохранения в файл ' + self.panel.currentPath, "Ошибка", style=wx.OK | wx.ICON_ERROR, parent=self)
			os.remove(self.panel.currentPath + "~")
			return
		os.remove(self.panel.currentPath + "~")
		open(self.panel.currentPath, "w", encoding="utf-8").write(savesString[:-1])
		self.panel.isSaved=True
		self.changeTitle()
		return True


	def onSaveAs(self, event=None):
		self.panel.isPathed=False
		self.onSave(event)


	def showProjectInfo(self, event):
		basicInfo="Количество глобальных новостей: {0:d}\n \
				   Количество локальных новостей: {1:d}\n \
				   Количество корпоративных новостей: {2:d}\n \
				   Количество компаний (акций): {3:d}\n \
				   Количество товаров: {4:d}\n \
				   Денежная сумма при старте: {5:s}\n \
				   Начальная дата: {6:s}".format(
					   len(self.panel.globalNews),
					   len(self.panel.localNews),
					   len(self.panel.corporationNews),
					   len(self.panel.stocks),
					   len(self.panel.commodities),
					   self.panel.currencyEdit.GetValue(),
					   self.panel.dateEdit.GetValue())
		wx.MessageBox(basicInfo, "Общая информация о проекте", style=wx.OK | wx.ICON_ERROR, parent=self)


	def showVersionInfo(self, event):
		try:
			versionInfosWindow(self, data=open("version.info", "r", encoding="utf-8").read()).Show()
		except:
			wx.MessageBox("Ошибка", "Ошибка", style=wx.OK | wx.ICON_EXCLAMATION)


class versionInfosWindow(wx.Frame):
	def __init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE, name=wx.FrameNameStr, data=""):
		super().__init__(parent, id=id, title="Версии", pos=pos, size=size, style=style, name=name)
		self.GetParent().Enable(False)
		self.sizer=wx.BoxSizer()
		self.panel=wx.Panel(self, pos=(0, 0), size=(400, 500))
		self.panel.versionInfosText=wx.TextCtrl(self.panel, value=data, pos=(10, 10), size=(380, 440), style=wx.TE_READONLY|wx.TE_MULTILINE)
		self.panel.buttonContinue=wx.Button(self.panel, label="Continue", pos=(10, 470))
		self.sizer.Add(self.panel)
		self.SetSizerAndFit(self.sizer)

		self.Bind(wx.EVT_BUTTON, self.btContinue, self.panel.buttonContinue)
		self.Bind(wx.EVT_CLOSE, self.btContinue, self)

	def btContinue(self, event):
		self.GetParent().Enable(True)
		self.Destroy()


class panel(wx.Panel):
	def __init__(self, parent):
		super().__init__(parent=parent)
		
		self.globalNews = []
		self.localNews = []
		self.corporationNews = []
		self.stocks = []
		self.commodities = []
		self.Date="0"
		self.Currency="0"

		self.currentPath = ""
		self.isPathed = False
		self.isSaved=True
		self.previousAssetType="Global News"
		self.reservedNewsIds=[]

		self.SetBackgroundColour('#F3F3F3')

		self.buttonAdd = wx.Button(self, label="Добавить")
		self.buttonEdit = wx.Button(self, label="Редактировать")
		self.buttonDelete = wx.Button(self, label="Удалить")
		#self.buttonView = wx.Button(self, label="Просмотр")
		self.mainList = wx.ListCtrl(self, size=(1050, 600), style=wx.LC_REPORT)
		self.typeChooser = wx.ComboBox(self, size=(150, -1), choices=["Global News", "Local News", "Corporation News", "Stocks", "Commodities"], style=wx.CB_READONLY)
		self.typeChooser.SetSelection(0)
		self.sumText = wx.StaticText(self, label="Всего: 0", style=wx.ALIGN_RIGHT)
		self.selectedCountText = wx.StaticText(self, label="Выделенно: 0", style=wx.ALIGN_RIGHT)
		self.selectedNumberText = wx.StaticText(self, label="Индекс выделенного: -", style=wx.ALIGN_RIGHT)
		self.dateEdit = FloatTextCtrl(self)
		self.dateEdit.SetHint("default date")
		self.currencyEdit = FloatTextCtrl(self)
		self.currencyEdit.SetHint("default currency")
		self.loadList()
		

		self.Bind(wx.EVT_BUTTON, self.addItem, self.buttonAdd)
		self.Bind(wx.EVT_BUTTON, self.deleteItem, self.buttonDelete)
		self.Bind(wx.EVT_BUTTON, self.editItem, self.buttonEdit)
		#self.Bind(wx.EVT_BUTTON, self.viewList, self.buttonView)
		self.Bind(wx.EVT_COMBOBOX, self.loadListEVT, self.typeChooser)
		self.mainList.Bind(wx.EVT_RIGHT_DOWN, self.onRightClickList, self.mainList)
		self.mainList.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.editItem, self.mainList)
		self.mainList.Bind(wx.EVT_LIST_KEY_DOWN, self.anyKeyPressByListItem, self.mainList)
		self.mainList.Bind(wx.EVT_LIST_ITEM_SELECTED, self.showCountSelectedItems, self.mainList)
		self.mainList.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.showCountSelectedItems, self.mainList)

		self.mainSizer = wx.GridBagSizer(10, 10)
		self.mainSizer.Add(self.buttonAdd, pos=(0, 0), span=(2, 1), flag=wx.EXPAND)
		self.mainSizer.Add(self.buttonEdit, pos=(2, 0), span=(2, 1), flag=wx.EXPAND)
		self.mainSizer.Add(self.buttonDelete, pos=(4, 0), span=(2, 1), flag=wx.EXPAND)
		#self.mainSizer.Add(self.buttonView, pos=(7, 0), span=(1, 1), flag=wx.EXPAND)
		self.mainSizer.Add(self.typeChooser, pos=(6, 0), span=(1, 1))
		self.mainSizer.Add(self.mainList, pos=(0, 1), span=(12, 10))
		self.mainSizer.Add(self.dateEdit, pos=(12, 3), span=(1, 1), flag=wx.EXPAND)
		self.mainSizer.Add(self.currencyEdit, pos=(12, 2), span=(1, 1), flag=wx.EXPAND)
		self.mainSizer.Add(self.sumText, pos=(12, 4), span=(1, 1), flag=wx.EXPAND)
		self.mainSizer.Add(self.selectedCountText, pos=(12, 6), span=(1, 1), flag=wx.EXPAND)
		self.mainSizer.Add(self.selectedNumberText, pos=(12, 8), span=(1, 1), flag=wx.EXPAND)

		self.SetSizerAndFit(self.mainSizer)


	def viewList(self, event):
		editingType=self.typeChooser.GetString(self.typeChooser.GetSelection())
		data=""
		if editingType=="Stocks":
			data=self.stocks
		elif editingType=="Commodities":
			data=self.commodities
		elif editingType=="Global News":
			data=self.globalNews
		elif editingType=="Local News":
			data=self.localNews
		elif editingType=="Corporation News":
			data=self.corporationNews
		viewWindow=ExtandedViewWindow(parent=wx.GetTopLevelParent(self), editingType=editingType, data=data)
		viewWindow.Show(True)
		self.Enable(False)
		self.GetParent().Enable(False)
		


	def updateCommoditiesAndCompanies(self):
		global COMMODITIES
		global COMPANIES
		COMMODITIES={}
		COMPANIES={}
		for item in self.stocks:
			if item.ticker=="":
				continue
			COMPANIES[item.ticker]=item.company
		for item in self.commodities:
			if item.ticker=="":
				continue
			COMMODITIES[item.ticker]=item.name
		something=None
		COMMODITIES=dict(sorted(COMMODITIES.items(), key=lambda x: x[1]))
		COMPANIES=dict(sorted(COMPANIES.items(), key=lambda x: x[1]))



	def showCountSelectedItems(self, event):
		count=self.mainList.GetSelectedItemCount()
		self.selectedCountText.SetLabel("Выделенно: " + str(count))
		if count==0:
			self.selectedNumberText.SetLabel("Номер выделенного: -")
			return
		self.selectedNumberText.SetLabel("Номер выделенного: " + str(self.mainList.GetFirstSelected()))


	def selectAllItemsAtMainList(self):
		for index in range(self.mainList.GetItemCount()):
			self.mainList.Select(index)



	def anyKeyPressByListItem(self, event=None):
		if event.GetKeyCode()==wx.WXK_DELETE:
			self.deleteItem(event)
		elif event.GetKeyCode()==wx.WXK_NUMPAD_ENTER or event.GetKeyCode()==wx.WXK_RETURN:
			self.editItem(event)
		elif event.GetKeyCode() == 65:
			self.selectAllItemsAtMainList()
		elif event.GetKeyCode() == 67:
			self.copyItem(event)
		elif event.GetKeyCode() == 86:
			self.pasteItem(event)


	def onRightClickList(self, event=None):
		menu=wx.Menu()
		itemAdd=menu.Append(wx.ID_ANY, "Add")
		itemDel=menu.Append(wx.ID_ANY, "Delete")
		itemEdit=menu.Append(wx.ID_ANY, "Edit")
		itemCopy=menu.Append(wx.ID_ANY, "Copy")
		itemPaste=menu.Append(wx.ID_ANY, "Paste")
		itemSpecialPaste=menu.Append(wx.ID_ANY, "Special paste")
		itemSpecialPastePlus=menu.Append(wx.ID_ANY, "Special paste+")
		self.Bind(wx.EVT_MENU, self.addItem, itemAdd)
		self.Bind(wx.EVT_MENU, self.deleteItem, itemDel)
		self.Bind(wx.EVT_MENU, self.editItem, itemEdit)
		self.Bind(wx.EVT_MENU, self.copyItem, itemCopy)
		self.Bind(wx.EVT_MENU, self.pasteItem, itemPaste)
		self.Bind(wx.EVT_MENU, self.specialPaste, itemSpecialPaste)
		self.Bind(wx.EVT_MENU, self.specialPastePlus, itemSpecialPastePlus)
		self.PopupMenu(menu)

	
	def saveListData(self):
		if self.previousAssetType=="Stocks":
			self.stocks=[]
			for line in range(0, self.mainList.GetItemCount()):
				t=[]
				for col in range(0, self.mainList.GetColumnCount()):
					t.append(self.mainList.GetItemText(line, col))
				self.stocks.append(Stock(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7]))
		elif self.previousAssetType=="Commodities":
			self.commodities=[]
			for line in range(0, self.mainList.GetItemCount()):
				t=[]
				for col in range(0, self.mainList.GetColumnCount()):
					t.append(self.mainList.GetItemText(line, col))
				self.commodities.append(Commodity(t[0], t[1], t[2], t[3], t[4], t[5]))
		elif self.previousAssetType=="Global News":
			self.globalNews=[]
			for line in range(0, self.mainList.GetItemCount()):
				t=[]
				for col in range(0, self.mainList.GetColumnCount()):
					t.append(self.mainList.GetItemText(line, col))
				self.globalNews.append(GlobalNews(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7]))
		elif self.previousAssetType=="Local News":
			self.localNews=[]
			for line in range(0, self.mainList.GetItemCount()):
				t=[]
				for col in range(0, self.mainList.GetColumnCount()):
					t.append(self.mainList.GetItemText(line, col))
				self.localNews.append(LocalNews(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8]))
		elif self.previousAssetType=="Corporation News":
			self.corporationNews=[]
			for line in range(0, self.mainList.GetItemCount()):
				t=[]
				for col in range(0, self.mainList.GetColumnCount()):
					t.append(self.mainList.GetItemText(line, col))
				self.corporationNews.append(CorporationNews(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7]))
		
	

	def readFromFile(self, path=None):
		if path==None: path=self.currentPath
		assets = open(path, 'r', encoding="utf-8").read().split("\n")
		for asset in assets:
			items = asset.split("\t")
			if items[0]=="s":
				self.stocks.append(panel.generateStock(items[1:]))
				continue
			if items[0]=="c":
				self.commodities.append(panel.generateCommodity(items[1:]))
				continue
			if items[0]=="gn":
				self.globalNews.append(panel.generateGlobalNews(items[1:]))
				self.reservedNewsIds.append(int(items[1]))
				continue
			if items[0]=="ln":
				self.localNews.append(panel.generateLocalNews(items[1:]))
				self.reservedNewsIds.append(int(items[1]))
				continue
			if items[0]=="cn":
				self.corporationNews.append(panel.generateCorporationNews(items[1:]))
				self.reservedNewsIds.append(int(items[1]))
				continue
			if items[0]=="dd":
				self.Date = items[1]
				continue
			if items[0]=="dc":
				self.Currency = items[1]
				continue
		
	def loadList(self, isClear=True, startIndex=0):
		editingType = self.typeChooser.GetString(self.typeChooser.GetSelection())
		if isClear:
			self.mainList.ClearAll()
		self.currencyEdit.SetValue(self.Currency)
		self.dateEdit.SetValue(self.Date)
		if editingType=="Stocks":
			if isClear:
				self.mainList.InsertColumn(0, "ticker", width=60)
				self.mainList.InsertColumn(1, "country", width=70)
				self.mainList.InsertColumn(2, "company", width=140)
				self.mainList.InsertColumn(3, "industry", width=140)
				self.mainList.InsertColumn(4, "description", width=160)
				self.mainList.InsertColumn(5, "uses", width=185)
				self.mainList.InsertColumn(6, "produces", width=185)
				self.mainList.InsertColumn(7, "startPrice", width=70)
			for item in self.stocks[startIndex:]:
				index = self.stocks.index(item)
				self.mainList.InsertItem(index, item.ticker)
				self.mainList.SetItem(index, 1, item.country)
				self.mainList.SetItem(index, 2, item.company)
				self.mainList.SetItem(index, 3, item.industry)
				self.mainList.SetItem(index, 4, item.description)
				self.mainList.SetItem(index, 5, item.getUsesString())
				self.mainList.SetItem(index, 6, item.getProducesString())
				self.mainList.SetItem(index, 7, item.startPrice)
		elif editingType=="Commodities":
			if isClear:
				self.mainList.InsertColumn(0, "ticker", width=60)
				self.mainList.InsertColumn(1, "name", width=160)
				self.mainList.InsertColumn(2, "sector", width=160)
				self.mainList.InsertColumn(3, "description", width=310)
				self.mainList.InsertColumn(4, "influence", width=235)
				self.mainList.InsertColumn(5, "start price", width=70)
			for item in self.commodities[startIndex:]:
				index = self.commodities.index(item)
				self.mainList.InsertItem(index, item.ticker)
				self.mainList.SetItem(index, 1, item.name)
				self.mainList.SetItem(index, 2, item.sector)
				self.mainList.SetItem(index, 3, item.description)
				self.mainList.SetItem(index, 4, item.getInfluenceString())
				self.mainList.SetItem(index, 5, item.startPrice)
		elif editingType=="Global News":
			if isClear:
				self.mainList.InsertColumn(0, "ID", width=25)
				self.mainList.InsertColumn(1, "duration", width=60)
				self.mainList.InsertColumn(2, "force", width=40)
				self.mainList.InsertColumn(3, "text", width=220)
				self.mainList.InsertColumn(4, "description", width=250)
				self.mainList.InsertColumn(5, "hint", width=190)
				self.mainList.InsertColumn(6, "influence", width=210)
				self.mainList.InsertColumn(7, "next", width=50)
			for item in self.globalNews[startIndex:]:
				index = self.globalNews.index(item)
				self.mainList.InsertItem(index, item.id)
				self.mainList.SetItem(index, 1, item.duration)
				self.mainList.SetItem(index, 2, item.force)
				self.mainList.SetItem(index, 3, item.text)
				self.mainList.SetItem(index, 4, item.description)
				self.mainList.SetItem(index, 5, item.hint)
				self.mainList.SetItem(index, 6, item.getInfluenceString())
				self.mainList.SetItem(index, 7, item.nextNews)
		elif editingType=="Local News":
			if isClear:
				self.mainList.InsertColumn(0, "ID", width=25)
				self.mainList.InsertColumn(1, "duration", width=60)
				self.mainList.InsertColumn(2, "force", width=40)
				self.mainList.InsertColumn(3, "text", width=220)
				self.mainList.InsertColumn(4, "description", width=250)
				self.mainList.InsertColumn(5, "country", width=70)
				self.mainList.InsertColumn(6, "hint", width=190)
				self.mainList.InsertColumn(7, "influence", width=140)
				self.mainList.InsertColumn(8, "next", width=50)
			for item in self.localNews[startIndex:]:
				index = self.localNews.index(item)
				self.mainList.InsertItem(index, item.id)
				self.mainList.SetItem(index, 1, item.duration)
				self.mainList.SetItem(index, 2, item.force)
				self.mainList.SetItem(index, 3, item.text)
				self.mainList.SetItem(index, 4, item.description)
				self.mainList.SetItem(index, 5, item.country)
				self.mainList.SetItem(index, 6, item.hint)
				self.mainList.SetItem(index, 7, item.getInfluenceString())
				self.mainList.SetItem(index, 8, item.nextNews)
		elif editingType=="Corporation News":
			if isClear:
				self.mainList.InsertColumn(0, "ID", width=25)
				self.mainList.InsertColumn(1, "duration", width=60)
				self.mainList.InsertColumn(2, "force", width=40)
				self.mainList.InsertColumn(3, "text", width=235)
				self.mainList.InsertColumn(4, "description", width=345)
				self.mainList.InsertColumn(5, "hint", width=220)
				self.mainList.InsertColumn(6, "company", width=70)
				self.mainList.InsertColumn(7, "next", width=50)
			for item in self.corporationNews[startIndex:]:
				index = self.corporationNews.index(item)
				self.mainList.InsertItem(index, item.id)
				self.mainList.SetItem(index, 1, item.duration)
				self.mainList.SetItem(index, 2, item.force)
				self.mainList.SetItem(index, 3, item.text)
				self.mainList.SetItem(index, 4, item.description)
				self.mainList.SetItem(index, 5, item.hint)
				self.mainList.SetItem(index, 6, item.ticker)
				self.mainList.SetItem(index, 7, item.nextNews)
		
		self.updateCommoditiesAndCompanies()


	def loadListEVT(self, event=None):
		self.saveListData()
		self.previousAssetType=self.typeChooser.GetString(self.typeChooser.GetSelection())
		self.loadList()
				


	def updateItemsCountText(self, editingType=""):
		self.sumText.SetLabel("Всего: " + str(self.mainList.GetItemCount()))


	def addItem(self, event=None):
		itemsCount=self.mainList.GetItemCount()
		editingType=self.typeChooser.GetString(self.typeChooser.GetSelection())
		if editingType=="Global News" or editingType=="Local News" or editingType=="Corporation News":
			index=self.getFreeIndex()
			self.mainList.InsertItem(itemsCount, str(index))
			self.reservedNewsIds.append(index)
		elif editingType=="Stocks" or editingType=="Commodities":
			self.mainList.InsertItem(itemsCount, "")
		else:
			mb=wx.MessageBox("Выберите тип элемента", "Ошибка", wx.OK | wx.ICON_EXCLAMATION, self)
			return
		for i in range(1, self.mainList.GetColumnCount()):
			self.mainList.SetItem(itemsCount, i, "")
		self.isSaved=False
		self.GetParent().changeTitle()

	def deleteItem(self, event=None):
		while self.mainList.GetSelectedItemCount() > 0:
			id=self.mainList.GetFirstSelected()
			text=self.mainList.GetItemText(id)
			self.mainList.DeleteItem(id)
			try: a=int(text)
			except ValueError as e: continue
			self.reservedNewsIds.remove(int(text))
		self.updateItemsCountText(editingType=self.typeChooser.GetString(self.typeChooser.GetSelection()))
		self.isSaved=False
		self.GetParent().changeTitle()

	def editItem(self, event=None):
		if self.mainList.GetFocusedItem()==-1:
			wx.MessageBox('Выберите объект редактирования', "Ошибка", style=wx.OK | wx.ICON_EXCLAMATION, parent=self)
			return
		id=self.mainList.GetFocusedItem()
		input=[]
		for column in range(self.mainList.GetColumnCount()):
			input.append(self.mainList.GetItemText(id, column))
		editorWindow=self.EditorWindow(parent=wx.GetTopLevelParent(self), type=self.typeChooser.GetString(self.typeChooser.GetSelection()), data=input)
		editorWindow.Show(True)
		self.Enable(False)
		self.GetParent().Enable(False)


	def copyItem(self, event):
		clb.OpenClipboard()
		clbText=""
		index=-1
		while True:
			index=self.mainList.GetNextSelected(index)
			if index==-1:
				break

			if self.typeChooser.GetStringSelection()=="Stocks":
				clbText+="s\t"
			elif self.typeChooser.GetStringSelection()=="Commodities":
				clbText+="c\t"
			elif self.typeChooser.GetStringSelection()=="Global News":
				clbText+="gn\t"
			elif self.typeChooser.GetStringSelection()=="Local News":
				clbText+="ln\t"
			elif self.typeChooser.GetStringSelection()=="Corporation News":
				clbText+="cn\t"

			for column in range(self.mainList.GetColumnCount()):
				clbText+=self.mainList.GetItemText(index, column) + "\t"
			clbText+="\n"
		if clbText!="":
			clb.SetClipboardText(clbText, clb.CF_UNICODETEXT)
		clb.CloseClipboard()


	def pasteItem(self, event):
		startIndex=self.mainList.GetItemCount()
		self.saveListData()
		try:
			clb.OpenClipboard()
			input=clb.GetClipboardData().split("\n")
			clb.CloseClipboard()
			minNewsId=0
			for line in input:
				items=line.split("\t")
				if items[0]=="s":
					self.stocks.append(Stock(items[1], items[2], items[3], items[4], items[5], items[6], items[7], items[8]))
				elif items[0]=="c":
					self.commodities.append(Commodity(items[1], items[2], items[3], items[4], items[5], items[6]))
				elif items[0]=="gn":
					while minNewsId in self.reservedNewsIds:
						minNewsId+=1
					self.globalNews.append(GlobalNews(str(minNewsId), items[2], items[3], items[4], items[5], items[6], items[7], items[8]))
					self.reservedNewsIds.append(minNewsId)
					minNewsId+=1
				elif items[0]=="ln":
					while minNewsId in self.reservedNewsIds:
						minNewsId+=1
					self.localNews.append(LocalNews(str(minNewsId), items[2], items[3], items[4], items[5], items[6], items[7], items[8], items[9]))
					self.reservedNewsIds.append(minNewsId)
					minNewsId+=1
				elif items[0]=="cn":
					while minNewsId in self.reservedNewsIds:
						minNewsId+=1
					self.corporationNews.append(CorporationNews(str(minNewsId), items[2], items[3], items[4], items[5], items[6], items[7], items[8]))
					self.reservedNewsIds.append(minNewsId)
					minNewsId+=1
		except:
			wx.MessageBox("Ошибка вставки", "Ошибка", style=wx.OK | wx.ICON_EXCLAMATION, parent=self)
			return
		self.loadList(isClear=False, startIndex=startIndex)
		self.isSaved=False
		self.GetParent().changeTitle()


	def specialPaste(self, event):
		pw=self.pasteWindow(self)
		pw.Show()
		self.Enable(False)
		self.GetParent().Enable(False)

	def specialPaste2(self, column):
		clb.OpenClipboard()
		pastedData=re.split("\n|\t|\r", clb.GetClipboardData())
		clb.CloseClipboard()
		while "" in pastedData:
			pastedData.remove("")
		editingType=self.typeChooser.GetStringSelection()
		index=0
		for item in pastedData:
			self.mainList.InsertItem(index, "")
			for i in range(self.mainList.GetColumnCount()):
				if i==column:
					self.mainList.SetItem(index, i, item)
				else:
					self.mainList.SetItem(index, i, "")
			index+=1
		self.Enable(True)
		self.GetParent().Enable(True)
		self.isSaved=False
		self.GetParent().changeTitle()
			


	def specialPastePlus(self, event):
		pw=self.pastePlusWindow(self)
		pw.Show()
		self.Enable(False)
		self.GetParent().Enable(False)

	def specialPastePlus2(self, data, isClear):
		if data=={}:
			self.Enable(True)
			self.GetParent().Enable(True)
			return
		data_=[]
		itemsCount=10**7
		columnCount=self.mainList.GetColumnCount()
		for index in range(columnCount):
			if not self.mainList.GetColumn(index).GetText() in list(data.keys()):
				data_.append(None)
				continue
			data_.append(data[self.mainList.GetColumn(index).GetText()].split("\n"))
			if len(data_[index])-1<itemsCount:
				itemsCount=len(data_[index])-1
		
		if isClear:
			columns=[]
			for i in range(columnCount):
				columns.append(self.mainList.GetColumn(i).GetText())
			self.mainList.ClearAll()
			type=self.typeChooser.GetStringSelection()
			if type=="Global News":
				self.globalNews=[]
			elif type=="Local News":
				self.localNews=[]
			elif type=="Corporation News":
				self.corporationNews=[]
			elif type=="Stocks":
				self.stocks=[]
			elif type=="Commodities":
				self.commodities=[]

			for column in range(columns):
				self.mainList.InsertColumn(column, columns[column])
		
		listIndex=self.mainList.GetItemCount()
		for index in range(itemsCount):
			self.mainList.InsertItem(listIndex, "")
			for col in range(columnCount):
				if data_[col]==None:
					continue
				self.mainList.SetItem(listIndex, col, data_[col][index])
			listIndex+=1

		self.Enable(True)
		self.GetParent().Enable(True)
		self.isSaved=False
		self.GetParent().changeTitle()

	class pasteWindow(wx.Frame):
		def __init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE, name=wx.FrameNameStr):
			super().__init__(parent, id=id, title="Специальная вставка", pos=(500, 500), size=(300, 150), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER, name=name)

			columns=[]
			Mlist=self.GetParent().mainList
			for col in range(Mlist.GetColumnCount()):
				columns.append(Mlist.GetColumn(col).GetText())

			self.panel=wx.Panel(self, pos=(0, 0), size=(300, 150))
			self.panel.cb=wx.ComboBox(self.panel, choices=columns, pos=(15, 10), size=(220, -1), style=wx.CB_READONLY)
			self.panel.continueButton=wx.Button(self.panel, label="Продолжить", pos=(15, 50))
			self.panel.Bind(wx.EVT_BUTTON, self.btContinue, self.panel.continueButton)
			
			self.Bind(wx.EVT_CLOSE, self.onClose, self)


		def btContinue(self, event):
			self.GetParent().specialPaste2(self.panel.cb.GetSelection())
			self.Destroy()
			

		def onClose(self, event=None):
			self.GetParent().GetParent().panel.Enable(True)
			self.GetParent().GetParent().Enable(True)
			self.Destroy()


	class pastePlusWindow(wx.Frame):
		def __init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE, name=wx.FrameNameStr):
			super().__init__(parent, id=id, title="Специальная вставка", pos=(500, 500), size=(300, 150), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER, name=name)

			self.columns=[]
			Mlist=self.GetParent().mainList
			for col in range(Mlist.GetColumnCount()):
				self.columns.append(Mlist.GetColumn(col).GetText())
				
			self.SetSize(wx.Size(225*len(self.columns)+25, 400))
			self.SetPosition(wx.Point(200, 350))

			self.panel=wx.Panel(self, pos=(0, 0), size=(225*len(self.columns)+25, 500))
			self.pastedTextEdits=[]
			self.pastedTypeCombos=[]

			for index in range(len(self.columns)):
				self.pastedTextEdits.append(wx.TextCtrl(self.panel, pos=((index)*215+15, 15), size=(200, 200), style=wx.TE_MULTILINE))
				self.pastedTypeCombos.append(wx.ComboBox(self.panel, pos=((index)*215+15, 230), choices=self.columns, style=wx.CB_READONLY))
			
			self.buttonContinue=wx.Button(self.panel, label="Продолжить", pos=(15, 275), size=(200, 70))
			self.chooseBox=wx.ComboBox(self.panel, pos=(230, 295), choices=["Добавить элементы", "Заменить выделенные"], style=wx.CB_READONLY, size=(200, 40))
			
			self.panel.Bind(wx.EVT_BUTTON, self.btContinue, self.buttonContinue)
			self.Bind(wx.EVT_CLOSE, self.onClose, self)
			

		def onClose(self, event=None):
			self.GetParent().GetParent().panel.Enable(True)
			self.GetParent().GetParent().Enable(True)
			self.Destroy()

		def btContinue(self, event):
			result={}
			isClear=False
			if self.chooseBox.GetSelection()==1:
				isClear=True
			for index in range(len(self.columns)):
				if self.pastedTypeCombos[index].GetSelection()==-1:
					continue
				result[self.pastedTypeCombos[index].GetStringSelection()]=self.pastedTextEdits[index].GetValue()
			self.GetParent().specialPastePlus2(result, isClear)
			self.Destroy()
			

	def setDefaults(self):
		self.globalNews = []
		self.localNews = []
		self.corporationNews = []
		self.stocks = []
		self.commodities = []
		self.Date="0"
		self.Currency="0"
		self.typeChooser.Select(0)
		self.currentPath = ""
		self.isPathed = False
		self.isSaved=True
		self.previousAssetType="Global News"
		self.reservedNewsIds=[]
		self.loadList()
		self.GetParent().changeTitle()



	def getFreeIndex(self):
		result=0
		while True:
			if result in self.reservedNewsIds:
				result+=1
			else:
				return result


			
	@staticmethod
	def generateGlobalNews(line):
		id_=line[0]
		duration=line[1]
		force=line[2]
		text=line[3]
		description=line[4]
		hint=line[5]
		influence={}
		if line[6].find(":")!=-1:
			for item in line[6].split("\\"):
				key = item.split(":")[0]
				value = item.split(":")[1]
				influence[key] = value
		newNews=line[7]
		return GlobalNews(id_, duration, force, text, description, hint, influence, newNews)
	
	@staticmethod
	def generateLocalNews(line):
		id_=line[0]
		duration=line[1]
		force=line[2]
		text=line[3]
		description=line[4]
		country=line[5]
		hint=line[6]
		influence={}
		if line[7].find(":")!=-1:
			for item in line[7].split("\\"):
				key = item.split(":")[0]
				value = item.split(":")[1]
				influence[key] = value
		newNews=line[8]
		return LocalNews(id_, duration, force, text, description, hint, country, influence, newNews)
	
	@staticmethod
	def generateCorporationNews(line):
		id_=line[0]
		duration=line[1]
		force=line[2]
		text=line[3]
		description=line[4]
		hint=line[5]
		ticker=line[6]
		newNews=line[7]
		return CorporationNews(id_, duration, force, text, description, hint, ticker, newNews)

	@staticmethod
	def generateStock(line):
		ticker=line[0]
		country=line[1]
		company=line[2]
		industry=line[3]
		description=line[4]
		uses={}
		if line[5].find(":")!=-1:
			for item in line[5].split("\\"):
				key = item.split(":")[0]
				value = item.split(":")[1]
				uses[key] = value
		produces={}
		if line[6].find(":")!=-1:
			for item in line[6].split("\\"):
				key = item.split(":")[0]
				value = item.split(":")[1]
				produces[key] = value
		startPrice=line[7]
		return Stock(ticker, country, company, industry, description, uses, produces, startPrice)
	
	@staticmethod
	def generateCommodity(line):
		ticker=line[0]
		name=line[1]
		sector=line[2]
		description=line[3]
		influence={}
		if line[4].find(":")!=-1:
			for item in line[4].split("\\"):
				key = item.split(":")[0]
				value = item.split(":")[1]
				influence[key] = value
		startPrice=line[5]
		return Commodity(ticker, name, sector, description, influence, startPrice)

	
	def catchChangedDataFromEditorWindow(self, asset=None):
		index=self.mainList.GetFocusedItem()
		if isinstance(asset, GlobalNews):
			self.mainList.SetItem(index, 0, asset.id)
			self.mainList.SetItem(index, 1, asset.duration)
			self.mainList.SetItem(index, 2, asset.force)
			self.mainList.SetItem(index, 3, asset.text)
			self.mainList.SetItem(index, 4, asset.description)
			self.mainList.SetItem(index, 5, asset.hint)
			self.mainList.SetItem(index, 6, asset.getInfluenceString())
			self.mainList.SetItem(index, 7, asset.nextNews)
		elif isinstance(asset, LocalNews):
			self.mainList.SetItem(index, 0, asset.id)
			self.mainList.SetItem(index, 1, asset.duration)
			self.mainList.SetItem(index, 2, asset.force)
			self.mainList.SetItem(index, 3, asset.text)
			self.mainList.SetItem(index, 4, asset.description)
			self.mainList.SetItem(index, 5, asset.country)
			self.mainList.SetItem(index, 6, asset.hint)
			self.mainList.SetItem(index, 7, asset.getInfluenceString())
			self.mainList.SetItem(index, 8, asset.nextNews)
		elif isinstance(asset, CorporationNews):
			self.mainList.SetItem(index, 0, asset.id)
			self.mainList.SetItem(index, 1, asset.duration)
			self.mainList.SetItem(index, 2, asset.force)
			self.mainList.SetItem(index, 3, asset.text)
			self.mainList.SetItem(index, 4, asset.description)
			self.mainList.SetItem(index, 5, asset.hint)
			self.mainList.SetItem(index, 6, asset.ticker)
			self.mainList.SetItem(index, 7, asset.nextNews)
		elif isinstance(asset, Stock):
			self.mainList.SetItem(index, 0, asset.ticker)
			self.mainList.SetItem(index, 1, asset.country)
			self.mainList.SetItem(index, 2, asset.company)
			self.mainList.SetItem(index, 3, asset.industry)
			self.mainList.SetItem(index, 4, asset.description)
			self.mainList.SetItem(index, 5, asset.getUsesString())
			self.mainList.SetItem(index, 6, asset.getProducesString())
			self.mainList.SetItem(index, 7, asset.startPrice)
		elif isinstance(asset, Commodity):
			self.mainList.SetItem(index, 0, asset.ticker)
			self.mainList.SetItem(index, 1, asset.name)
			self.mainList.SetItem(index, 2, asset.sector)
			self.mainList.SetItem(index, 3, asset.description)
			self.mainList.SetItem(index, 4, asset.getInfluenceString())
			self.mainList.SetItem(index, 5, asset.startPrice)
		self.isSaved=False
		self.GetParent().changeTitle()


	class EditorWindow(wx.Frame):
		def __init__(self, parent, type, data=[]):
			super().__init__(parent=parent, title=type + " Editor", style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER|wx.STAY_ON_TOP)
			self.SetPosition(wx.Point(self.GetParent().GetSize().x + self.GetParent().GetPosition().x - 400, self.GetParent().GetPosition().y + 50))
			
			self.panel=panel.panelEdit(self, type, data)

			self.mainSizer=wx.BoxSizer()
			self.mainSizer.Add(self.panel, flag=wx.EXPAND)
			self.SetSizerAndFit(self.mainSizer)
			

	class panelEdit(wx.Panel):
		def __init__(self, parent, type, data=[]):
			super().__init__(parent=parent)
			self.editingType=type
			self.SetBackgroundColour('#F3F3F3')
			
			self.buttonApply=wx.Button(self, label="Apply changes")
			self.mainSizer=wx.GridBagSizer(10, 6)
	
			if self.editingType=="Stocks":
				self.tickerEdit=wx.TextCtrl(self, value=data[0], style=wx.TE_PROCESS_ENTER)
				self.tickerEdit.SetHint("Ticker")
				self.countryCombo=wx.ComboBox(self, choices=COUNTRIES, style=wx.CB_READONLY)
				try:
					self.countryCombo.Select(COUNTRIES.index(data[1]))
				except:
					self.countryCombo.Select(0)
				self.companyEdit=wx.TextCtrl(self, value=data[2], style=wx.TE_PROCESS_ENTER)
				self.companyEdit.SetHint("Company")
				self.industrialCombo=wx.ComboBox(self, choices=INDUSTRIAL_VALUES, style=wx.CB_READONLY)
				try:
					self.industrialCombo.Select(INDUSTRIAL_VALUES.index(data[3]))
				except:
					self.industrialCombo.Select(0)
				self.descriptionEdit=wx.TextCtrl(self, size=(200, 150), style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER, value=data[4].replace("§", "\n"))
				self.descriptionEdit.SetHint("Description")
				self.usesHint=wx.StaticText(self, label="Uses:")
				self.usesList=wx.ListCtrl(self, size=(200, 150), style=wx.LC_REPORT)
				self.producesHint=wx.StaticText(self, label="Produces:")
				self.producesList=wx.ListCtrl(self, size=(200, 150), style=wx.LC_REPORT)
				self.startPriceEdit=FloatTextCtrl(self, value=data[7], style=wx.TE_PROCESS_ENTER)
				self.startPriceEdit.SetHint("Start price")
	
				self.mainSizer.Add(self.tickerEdit, pos=(1, 1), span=(1, 1), flag=wx.EXPAND)
				self.mainSizer.Add(self.countryCombo, pos=(2, 1), span=(1, 1))
				self.mainSizer.Add(self.companyEdit, pos=(3, 1), span=(1, 1), flag=wx.EXPAND)
				self.mainSizer.Add(self.startPriceEdit, pos=(4, 1), span=(1, 1), flag=wx.EXPAND)
				self.mainSizer.Add(self.industrialCombo, pos=(5, 1), span=(1, 1))
				self.mainSizer.Add(self.descriptionEdit, pos=(6, 1), span=(2, 2), flag=wx.EXPAND)
				self.mainSizer.Add(self.usesHint, pos=(1, 4), span=(1, 1), flag=wx.ALIGN_RIGHT|wx.EXPAND)
				self.mainSizer.Add(self.usesList, pos=(1, 5), span=(5, 1), flag=wx.EXPAND)
				self.mainSizer.Add(self.producesHint, pos=(6, 4), span=(1, 1), flag=wx.ALIGN_RIGHT|wx.EXPAND)
				self.mainSizer.Add(self.producesList, pos=(6, 5), span=(2, 1), flag=wx.EXPAND)
				self.mainSizer.Add(self.buttonApply, pos=(8, 5), span=(2, 2), flag=wx.ALIGN_RIGHT|wx.EXPAND)

	
			elif self.editingType=="Commodities":
				self.tickerEdit=wx.TextCtrl(self, value=data[0], style=wx.TE_PROCESS_ENTER)
				self.tickerEdit.SetHint("Ticker")
				self.nameEdit=wx.TextCtrl(self, value=data[1], style=wx.TE_PROCESS_ENTER)
				self.nameEdit.SetHint("Name")
				self.sectorsCombo=wx.ComboBox(self, choices=SECTOR_VALUES, style=wx.CB_READONLY)
				try:
					self.sectorsCombo.Select(SECTOR_VALUES.index(data[2]))
				except:
					self.sectorsCombo.Select(0)
				self.descriptionEdit=wx.TextCtrl(self, size=(200, 150), style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER, value=data[3].replace("§", "\n"))
				self.descriptionEdit.SetHint("Description")
				self.influenceHint=wx.StaticText(self, label="Influence:")
				self.influenceList=wx.ListCtrl(self, size=(200, 150), style=wx.LC_REPORT)
				self.startPriceEdit=FloatTextCtrl(self, value=data[5], style=wx.TE_PROCESS_ENTER)
				self.startPriceEdit.SetHint("Start price")
	
				self.mainSizer.Add(self.tickerEdit, pos=(1, 1), span=(1, 2))
				self.mainSizer.Add(self.nameEdit, pos=(2, 1), span=(1, 2))
				self.mainSizer.Add(self.sectorsCombo, pos=(3, 1), span=(1, 1))
				self.mainSizer.Add(self.startPriceEdit, pos=(1, 5), span=(1, 2))
				self.mainSizer.Add(self.descriptionEdit, pos=(4, 1), span=(2, 2), flag=wx.EXPAND)
				self.mainSizer.Add(self.influenceHint, pos=(4, 4), span=(1, 1), flag=wx.ALIGN_RIGHT|wx.EXPAND)
				self.mainSizer.Add(self.influenceList, pos=(4, 5), span=(2, 1), flag=wx.EXPAND)
				self.mainSizer.Add(self.buttonApply, pos=(6, 5), span=(2, 2), flag=wx.ALIGN_RIGHT|wx.EXPAND)
	
			elif self.editingType=="Global News":
				self.idEdit=IntTextCtrl(self, style=wx.TE_READONLY, value=data[0])
				self.idEdit.Enable(False)
				self.durationEdit=IntTextCtrl(self, value=data[1], style=wx.TE_PROCESS_ENTER)
				self.durationEdit.SetHint("Duration")
				self.forceEdit=IntTextCtrl(self, value=data[2], style=wx.TE_PROCESS_ENTER)
				self.forceEdit.SetHint("Force")
				self.textEdit=wx.TextCtrl(self, size=(200, 150), style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER, value=data[3].replace("§", "\n"))
				self.textEdit.SetHint("Text")
				self.descriptionEdit=wx.TextCtrl(self, size=(200, 150), style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER, value=data[4].replace("§", "\n"))
				self.descriptionEdit.SetHint("Description")
				self.hintEdit=wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER, value=data[5].replace("§", "\n"))
				self.hintEdit.SetHint("Hint")
				self.influenceHint=wx.StaticText(self, label="Influence:")
				self.influenceList=wx.ListCtrl(self, size=(200, 150), style=wx.LC_REPORT)
				self.nextNewsCombo=wx.ComboBox(self, choices=['None'] + sorted(list(set(list(map(str, self.GetParent().GetParent().panel.reservedNewsIds)))-set(data[0]))), style=wx.CB_READONLY)
				try:
					self.nextNewsCombo.Select(data[7].split(':')[0])
				except:
					self.nextNewsCombo.Select(0)
				if ":" in data[7]:
					self.nextNewsSinceDays=IntTextCtrl(self, value=data[7].split(':')[1], style=wx.TE_PROCESS_ENTER)
				else:
					self.nextNewsSinceDays=IntTextCtrl(self, style=wx.TE_PROCESS_ENTER)

				self.durationEdit.SetHint("next")
	
				self.mainSizer.Add(self.idEdit, pos=(1, 1), span=(1, 1), flag=wx.EXPAND)
				self.mainSizer.Add(self.durationEdit, pos=(2, 1), span=(1, 1), flag=wx.EXPAND)
				self.mainSizer.Add(self.forceEdit, pos=(3, 1), span=(1, 1), flag=wx.EXPAND)
				self.mainSizer.Add(self.hintEdit, pos=(4, 1), span=(2, 2), flag=wx.EXPAND)
				self.mainSizer.Add(self.textEdit, pos=(6, 1), span=(2, 2), flag=wx.EXPAND)
				self.mainSizer.Add(self.descriptionEdit, pos=(1, 5), span=(5, 1), flag=wx.EXPAND)
				self.mainSizer.Add(self.influenceHint, pos=(6, 4), span=(1, 1), flag=wx.ALIGN_RIGHT|wx.EXPAND)
				self.mainSizer.Add(self.influenceList, pos=(6, 5), span=(2, 1), flag=wx.EXPAND)
				self.mainSizer.Add(self.nextNewsCombo, pos=(8, 1), span=(1, 1), flag=wx.EXPAND)
				self.mainSizer.Add(self.nextNewsSinceDays, pos=(8, 2), span=(1, 1), flag=wx.EXPAND)
				self.mainSizer.Add(self.buttonApply, pos=(8, 5), span=(2, 2), flag=wx.ALIGN_RIGHT|wx.EXPAND)

	
			elif self.editingType=="Local News":
				self.idEdit=IntTextCtrl(self, style=wx.TE_READONLY, value=data[0])
				self.idEdit.Enable(False)
				self.durationEdit=IntTextCtrl(self, value=data[1], style=wx.TE_PROCESS_ENTER)
				self.durationEdit.SetHint("Duration")
				self.forceEdit=IntTextCtrl(self, value=data[2], style=wx.TE_PROCESS_ENTER)
				self.forceEdit.SetHint("Force")
				self.textEdit=wx.TextCtrl(self, size=(200, 150), style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER, value=data[3].replace("§", "\n"))
				self.textEdit.SetHint("Text")
				self.descriptionEdit=wx.TextCtrl(self, size=(200, 150), style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER, value=data[4].replace("§", "\n"))
				self.descriptionEdit.SetHint("Description")
				self.countryCombo=wx.ComboBox(self, choices=COUNTRIES, style=wx.CB_READONLY)
				try:
					self.countryCombo.Select(COUNTRIES.index(data[5]))
				except:
					self.countryCombo.Select(0)
				self.hintEdit=wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER, value=data[6].replace("§", "\n"))
				self.hintEdit.SetHint("Hint")
				self.influenceHint=wx.StaticText(self, label="Influence:")
				self.influenceList=wx.ListCtrl(self, size=(200, 150), style=wx.LC_REPORT)
				self.nextNewsCombo=wx.ComboBox(self, choices=['None'] + sorted(list(set(list(map(str, self.GetParent().GetParent().panel.reservedNewsIds)))-set(data[0]))), style=wx.CB_READONLY)
				try:
					self.nextNewsCombo.Select(list(map(str, self.GetParent().GetParent().panel.reservedNewsIds)).index(data[8].split(':')[0]))
				except:
					self.nextNewsCombo.Select(0)
				if ":" in data[8]:
					self.nextNewsSinceDays=IntTextCtrl(self, value=data[8].split(':')[1], style=wx.TE_PROCESS_ENTER)
				else:
					self.nextNewsSinceDays=IntTextCtrl(self, style=wx.TE_PROCESS_ENTER)
				self.durationEdit.SetHint("next")
	
				self.mainSizer.Add(self.idEdit, pos=(1, 1), span=(1, 1), flag=wx.EXPAND)
				self.mainSizer.Add(self.durationEdit, pos=(2, 1), span=(1, 1), flag=wx.EXPAND)
				self.mainSizer.Add(self.forceEdit, pos=(3, 1), span=(1, 1), flag=wx.EXPAND)
				self.mainSizer.Add(self.countryCombo, pos=(1, 2), span=(1, 1))
				self.mainSizer.Add(self.hintEdit, pos=(4, 1), span=(2, 2), flag=wx.EXPAND)
				self.mainSizer.Add(self.textEdit, pos=(6, 1), span=(2, 2), flag=wx.EXPAND)
				self.mainSizer.Add(self.descriptionEdit, pos=(1, 5), span=(5, 1), flag=wx.EXPAND)
				self.mainSizer.Add(self.influenceHint, pos=(6, 4), span=(1, 1), flag=wx.ALIGN_RIGHT|wx.EXPAND)
				self.mainSizer.Add(self.influenceList, pos=(6, 5), span=(2, 1), flag=wx.EXPAND)
				self.mainSizer.Add(self.nextNewsCombo, pos=(8, 1), span=(1, 1), flag=wx.EXPAND)
				self.mainSizer.Add(self.nextNewsSinceDays, pos=(8, 2), span=(1, 1), flag=wx.EXPAND)
				self.mainSizer.Add(self.buttonApply, pos=(8, 5), span=(2, 2), flag=wx.ALIGN_RIGHT|wx.EXPAND)
				pass
			elif self.editingType=="Corporation News":
				self.idEdit=IntTextCtrl(self, style=wx.TE_READONLY | wx.TE_PROCESS_ENTER, value=data[0])
				self.idEdit.Enable(False)
				self.durationEdit=IntTextCtrl(self, value=data[1], style=wx.TE_PROCESS_ENTER)
				self.durationEdit.SetHint("Duration")
				self.forceEdit=IntTextCtrl(self, value=data[2], style=wx.TE_PROCESS_ENTER)
				self.forceEdit.SetHint("Force")
				self.textEdit=wx.TextCtrl(self, size=(200, 150), style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER, value=data[3].replace("§", "\n"))
				self.textEdit.SetHint("Text")
				self.descriptionEdit=wx.TextCtrl(self, size=(200, 150), style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER, value=data[4].replace("§", "\n"))
				self.descriptionEdit.SetHint("Description")
				self.hintEdit=wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER, value=data[5].replace("§", "\n"))
				self.hintEdit.SetHint("Hint")
				self.tickerEdit=wx.TextCtrl(self, value=data[6], style=wx.TE_PROCESS_ENTER)
				self.tickerEdit.SetHint("Ticker")
				self.nextNewsCombo=wx.ComboBox(self, choices=['None'] + sorted(list(set(list(map(str, self.GetParent().GetParent().panel.reservedNewsIds)))-set(data[0]))), style=wx.CB_READONLY)
				try:
					self.nextNewsCombo.Select(list(map(str, self.GetParent().GetParent().panel.reservedNewsIds)).index(data[7].split(':')[0]))
				except:
					self.nextNewsCombo.Select(0)
				if ":" in data[7]:
					self.nextNewsSinceDays=IntTextCtrl(self, value=data[7].split(':')[1], style=wx.TE_PROCESS_ENTER)
				else:
					self.nextNewsSinceDays=IntTextCtrl(self, style=wx.TE_PROCESS_ENTER)
				self.durationEdit.SetHint("next")
	
				self.mainSizer.Add(self.idEdit, pos=(1, 1), span=(1, 1), flag=wx.EXPAND)
				self.mainSizer.Add(self.durationEdit, pos=(2, 1), span=(1, 1), flag=wx.EXPAND)
				self.mainSizer.Add(self.forceEdit, pos=(3, 1), span=(1, 1), flag=wx.EXPAND)
				self.mainSizer.Add(self.tickerEdit, pos=(4, 1), span=(1, 1), flag=wx.EXPAND)
				self.mainSizer.Add(self.textEdit, pos=(6, 1), span=(2, 2), flag=wx.EXPAND)
				self.mainSizer.Add(self.descriptionEdit, pos=(1, 5), span=(5, 1), flag=wx.EXPAND)
				self.mainSizer.Add(self.hintEdit, pos=(6, 5), span=(2, 2), flag=wx.EXPAND)
				self.mainSizer.Add(self.nextNewsCombo, pos=(8, 1), span=(1, 1), flag=wx.EXPAND)
				self.mainSizer.Add(self.nextNewsSinceDays, pos=(8, 2), span=(1, 1), flag=wx.EXPAND)
				self.mainSizer.Add(self.buttonApply, pos=(8, 5), span=(2, 2), flag=wx.ALIGN_RIGHT|wx.EXPAND)
				pass



			if self.editingType=="Commodities" or self.editingType=="Global News" or self.editingType=="Local News":
				self.influenceList.Bind(wx.EVT_RIGHT_DOWN, lambda event: self.onRightClickList(event, type="influence"), self.influenceList)

				self.influenceList.InsertColumn(0, "ticker", width=self.influenceList.GetSize().x/2)
				self.influenceList.InsertColumn(1, "value", width=self.influenceList.GetSize().x/2)
				self.Bind(wx.EVT_LIST_KEY_DOWN, lambda event: self.anyKeyPressByListItem(event, type="influence"), self.influenceList)
				if self.editingType=="Commodities":
					self.Bind(wx.EVT_TEXT_ENTER, self.onCloseByButton, self.tickerEdit)
					self.Bind(wx.EVT_TEXT_ENTER, self.onCloseByButton, self.nameEdit)
					self.Bind(wx.EVT_TEXT_ENTER, self.onCloseByButton, self.sectorsCombo)
					self.Bind(wx.EVT_TEXT_ENTER, self.onCloseByButton, self.descriptionEdit)
					self.Bind(wx.EVT_TEXT_ENTER, self.onCloseByButton, self.startPriceEdit)
					i=0
					for key, value in Commodity.convertInfluenceStringToDict(data[4]).items():
						self.influenceList.InsertItem(i, str(i))
						self.influenceList.SetItem(i, 0, key)
						self.influenceList.SetItem(i, 1, value)
						i+=1
					self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.editItem, self.influenceList)
				elif self.editingType=="Global News":
					self.Bind(wx.EVT_TEXT_ENTER, self.onCloseByButton, self.durationEdit)
					self.Bind(wx.EVT_TEXT_ENTER, self.onCloseByButton, self.forceEdit)
					self.Bind(wx.EVT_TEXT_ENTER, self.onCloseByButton, self.hintEdit)
					self.Bind(wx.EVT_TEXT_ENTER, self.onCloseByButton, self.textEdit)
					self.Bind(wx.EVT_TEXT_ENTER, self.onCloseByButton, self.descriptionEdit)
					i=0
					for key, value in GlobalNews.convertInfluenceStringToDict(data[6]).items():
						self.influenceList.InsertItem(i, str(i))
						self.influenceList.SetItem(i, 0, key)
						self.influenceList.SetItem(i, 1, value)
						i+=1
					self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.editItem, self.influenceList)
				elif self.editingType=="Local News":
					self.Bind(wx.EVT_TEXT_ENTER, self.onCloseByButton, self.countryCombo)
					self.Bind(wx.EVT_TEXT_ENTER, self.onCloseByButton, self.durationEdit)
					self.Bind(wx.EVT_TEXT_ENTER, self.onCloseByButton, self.forceEdit)
					self.Bind(wx.EVT_TEXT_ENTER, self.onCloseByButton, self.hintEdit)
					self.Bind(wx.EVT_TEXT_ENTER, self.onCloseByButton, self.textEdit)
					self.Bind(wx.EVT_TEXT_ENTER, self.onCloseByButton, self.descriptionEdit)
					i=0
					for key, value in LocalNews.convertInfluenceStringToDict(data[7]).items():
						self.influenceList.InsertItem(i, str(i))
						self.influenceList.SetItem(i, 0, key)
						self.influenceList.SetItem(i, 1, value)
						i+=1
					self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.editItem, self.influenceList)
			elif self.editingType=="Stocks":
				self.Bind(wx.EVT_TEXT_ENTER, self.onCloseByButton, self.tickerEdit)
				self.Bind(wx.EVT_TEXT_ENTER, self.onCloseByButton, self.countryCombo)
				self.Bind(wx.EVT_TEXT_ENTER, self.onCloseByButton, self.companyEdit)
				self.Bind(wx.EVT_TEXT_ENTER, self.onCloseByButton, self.industrialCombo)
				self.Bind(wx.EVT_TEXT_ENTER, self.onCloseByButton, self.startPriceEdit)
				self.Bind(wx.EVT_TEXT_ENTER, self.onCloseByButton, self.descriptionEdit)
				self.usesList.Bind(wx.EVT_RIGHT_DOWN, lambda event: self.onRightClickList(event, type="uses"), self.usesList)
				self.producesList.Bind(wx.EVT_RIGHT_DOWN, lambda event: self.onRightClickList(event, type="produces"), self.producesList)

				self.usesList.InsertColumn(0, "ticker", width=self.usesList.GetSize().x/2)
				self.usesList.InsertColumn(1, "value", width=self.usesList.GetSize().x/2)
				self.usesList.Bind(wx.EVT_LIST_KEY_DOWN, lambda event: self.anyKeyPressByListItem(event, type="uses"), self.usesList)
				self.producesList.Bind(wx.EVT_LIST_KEY_DOWN, lambda event: self.anyKeyPressByListItem(event, type="produces"), self.producesList)
				i=0
				for key, value in Stock.convertUsesStringToDict(data[5]).items():
					self.usesList.InsertItem(i, str(i))
					self.usesList.SetItem(i, 0, key)
					self.usesList.SetItem(i, 1, value)
					i+=1
				self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, lambda event: self.editItem(event, "_uses"), self.usesList)
				self.producesList.InsertColumn(0, "ticker", width=self.producesList.GetSize().x/2)
				self.producesList.InsertColumn(1, "value", width=self.producesList.GetSize().x/2)
				i=0
				for key, value in Stock.convertProducesStringToDict(data[6]).items():
					self.producesList.InsertItem(i, str(i))
					self.producesList.SetItem(i, 0, key)
					self.producesList.SetItem(i, 1, value)
					i+=1
				self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, lambda event: self.editItem(event, "_produces"), self.producesList)
			elif self.editingType=="Corporation News":
				self.Bind(wx.EVT_TEXT_ENTER, self.onCloseByButton, self.durationEdit)
				self.Bind(wx.EVT_TEXT_ENTER, self.onCloseByButton, self.forceEdit)
				self.Bind(wx.EVT_TEXT_ENTER, self.onCloseByButton, self.tickerEdit)
				self.Bind(wx.EVT_TEXT_ENTER, self.onCloseByButton, self.textEdit)
				self.Bind(wx.EVT_TEXT_ENTER, self.onCloseByButton, self.descriptionEdit)
				self.Bind(wx.EVT_TEXT_ENTER, self.onCloseByButton, self.hintEdit)
	

			self.Bind(wx.EVT_BUTTON, self.onCloseByButton, self.buttonApply)
			self.GetParent().Bind(wx.EVT_CLOSE, self.onClose, self.GetParent())
			self.SetSizerAndFit(self.mainSizer)

		def editItem(self, event, type=""):
			if type=="_uses":
				ticker=self.usesList.GetItemText(self.usesList.GetFocusedItem(), 0)
				value=self.usesList.GetItemText(self.usesList.GetFocusedItem(), 1)
			elif type=="_produces":
				ticker=self.producesList.GetItemText(self.producesList.GetFocusedItem(), 0)
				value=self.producesList.GetItemText(self.producesList.GetFocusedItem(), 1)
			else:
				ticker=self.influenceList.GetItemText(self.influenceList.GetFocusedItem(), 0)
				value=self.influenceList.GetItemText(self.influenceList.GetFocusedItem(), 1)
			editorWindow=self.InfluenceWindow(parent=wx.GetTopLevelParent(self), type=self.editingType + type, data=[ticker, value])
			editorWindow.Show(True)
			self.Enable(False)
			self.GetParent().Enable(False)

		def catchEditedData(self, data=["", "", ""]):
			if data[2]=="Stocks_uses":
				index=self.usesList.GetFocusedItem()
				self.usesList.SetItem(index, 0, data[0])
				self.usesList.SetItem(index, 1, data[1])
			elif data[2]=="Stocks_produces":
				index=self.producesList.GetFocusedItem()
				self.producesList.SetItem(index, 0, data[0])
				self.producesList.SetItem(index, 1, data[1])
			else:
				index=self.influenceList.GetFocusedItem()
				self.influenceList.SetItem(index, 0, data[0])
				self.influenceList.SetItem(index, 1, data[1])
			
			

		class InfluenceWindow(wx.Frame):
			def __init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE, name=wx.FrameNameStr, type="", data=[]):
				super().__init__(parent, id=id, title="Influence Editor", pos=pos, size=size, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER|wx.STAY_ON_TOP, name=name)
				self.type=type
				self.panel=wx.Panel(self)
				self.sizer=wx.GridBagSizer(10, 10)
				if self.type=="Stocks_uses" or self.type=="Stocks_produces":
					self.chooser=wx.ComboBox(self.panel, style=wx.CB_READONLY, choices=list(COMMODITIES.values()))
					self.tickerEdit=wx.TextCtrl(self.panel, style=wx.TE_READONLY, value=data[0])
					self.tickerEdit.SetHint("Тикер элемента")
					self.tickerEdit.Enable(False)
					try:
						self.chooser.Select(list(COMMODITIES.keys()).index(data[0]))
					except:
						self.chooser.Select(-1)

				elif self.type=="Commodities":
					self.chooser=wx.ComboBox(self.panel, style=wx.CB_READONLY, choices=COUNTRIES)
					try:
						self.chooser.Select(COUNTRIES.index(data[0]))
					except:
						self.chooser.Select(-1)
				elif "News" in self.type:
					self.chooser=wx.ComboBox(self.panel, style=wx.CB_READONLY, choices=list(COMPANIES.values()) + list(COMMODITIES.values()))
					self.tickerEdit=wx.TextCtrl(self.panel, style=wx.TE_READONLY, value=data[0])
					self.tickerEdit.Enable(False)

					try:
						self.chooser.Select(list(COMMODITIES.keys()).index(data[0]))
					except:
						try:
							self.chooser.Select(list(COMPANIES.keys()).index(data[0]))
						except:
							self.chooser.Select(-1)

				self.valueEdit=FloatTextCtrl(self.panel, value=data[1], style=wx.TE_PROCESS_ENTER)
				self.valueEdit.SetHint("Значение")
				self.buttonContinue=wx.Button(self.panel, label="Continue")

				self.Bind(wx.EVT_COMBOBOX, self.changeTicker, self.chooser)
				self.Bind(wx.EVT_TEXT_ENTER, self.onCloseByButton, self.valueEdit)
				self.Bind(wx.EVT_BUTTON, self.onCloseByButton, self.buttonContinue)
				self.Bind(wx.EVT_CLOSE, self.onClose, self)

				self.sizer.Add(self.chooser, pos=(1, 1), span=(1, 2), flag=wx.EXPAND)
				try:
					self.sizer.Add(self.tickerEdit, pos=(1, 3), span=(1, 1), flag=wx.EXPAND)
				except:
					pass
				self.sizer.Add(self.valueEdit, pos=(2, 1), span=(1, 1), flag=wx.EXPAND)
				self.sizer.Add(self.buttonContinue, pos=(2, 3), span=(1, 1), flag=wx.ALIGN_CENTER)
				self.panel.SetSizerAndFit(self.sizer)
				self.mainsizer=wx.BoxSizer()
				self.mainsizer.Add(self.panel)
				self.SetSizerAndFit(self.mainsizer)

				self.changeTicker()


			def onCloseByButton(self, event):
				result=[]
				try:
					result.append(self.tickerEdit.GetValue())
				except:
					result.append(self.chooser.GetStringSelection())
				result.append(self.valueEdit.GetValue())
				result.append(self.type)
				self.GetParent().panel.catchEditedData(data=result)
				self.GetParent().panel.Enable(True)
				self.GetParent().Enable(True)
				self.Destroy()


			def onClose(self, event):
				self.GetParent().panel.Enable(True)
				self.GetParent().Enable(True)
				self.Destroy()


			def changeTicker(self, event=None):
				if self.type=="Stocks_uses" or self.type=="Stocks_produces":
					try:
						self.tickerEdit.SetValue(list(COMMODITIES.keys())[list(COMMODITIES.values()).index(self.chooser.GetStringSelection())])
					except:
						self.tickerEdit.SetValue("")
				if self.type=="Commodities":
					return
				if "News" in self.type:
					try:
						self.tickerEdit.SetValue(list(COMMODITIES.keys())[list(COMMODITIES.values()).index(self.chooser.GetStringSelection())])
					except:
						try:
							self.tickerEdit.SetValue(list(COMPANIES.keys())[list(COMPANIES.values()).index(self.chooser.GetStringSelection())])
						except:
							self.tickerEdit.SetValue("")
				




		def anyKeyPressByListItem(self, event, type=""):
			if event.GetKeyCode()==wx.WXK_DELETE:
				self.onRemoveItem(event=event, type=type)



		def onRightClickList(self, event=None, type=""):
			menu=wx.Menu()
			itemAdd=menu.Append(wx.ID_ANY, "Add")
			itemDel=menu.Append(wx.ID_ANY, "Delete")
			itemSpecialAdd=menu.Append(wx.ID_ANY, "Special add")
			itemPaste=menu.Append(wx.ID_ANY, "Paste")
			self.Bind(wx.EVT_MENU, lambda event: self.onAddItem(event, type), itemAdd)
			self.Bind(wx.EVT_MENU, lambda event: self.onSpecialAddItem(event, type), itemSpecialAdd)
			self.Bind(wx.EVT_MENU, lambda event: self.onRemoveItem(event, type), itemDel)
			self.Bind(wx.EVT_MENU, lambda event: self.onPasteItem(event, type), itemPaste)
			
			self.PopupMenu(menu)


		def onPasteItem(self, event=None, type=""):
			pw=self.pasteWindow(self, type=type)
			pw.Show()
			self.Enable(False)
			self.GetParent().Enable(False)

		def catchPastedData(self, type="", data={}):
			if type=="influence":
				for key, value in data.items():
					index=self.influenceList.GetItemCount()
					self.influenceList.InsertItem(index, "")
					self.influenceList.SetItem(index, 0, key)
					self.influenceList.SetItem(index, 1, value)
			elif type=="uses":
				for key, value in data.items():
					index=self.usesList.GetItemCount()
					self.usesList.InsertItem(index, "")
					self.usesList.SetItem(index, 0, key)
					self.usesList.SetItem(index, 1, value)
			elif type=="produces":
				for key, value in data.items():
					index=self.producesList.GetItemCount()
					self.producesList.InsertItem(index, "")
					self.producesList.SetItem(index, 0, key)
					self.producesList.SetItem(index, 1, value)
			self.Enable(True)
			self.GetParent().Enable(True)
				


		
		class pasteWindow(wx.Frame):
			def __init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE, name=wx.FrameNameStr, type=""):
				super().__init__(parent, id=id, title="Paste Window", pos=pos, size=size, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER|wx.STAY_ON_TOP, name=name)
			
				self.type=type
					
				self.SetSize(wx.Size(475, 400))
				self.SetPosition(wx.Point(200, 350))

				self.panel=wx.Panel(self, pos=(0, 0), size=(475, 500))

				self.tickerEdit=wx.TextCtrl(self.panel, pos=(15, 15), size=(200, 200), style=wx.TE_MULTILINE)
				self.valueEdit=wx.TextCtrl(self.panel, pos=(230, 15), size=(200, 200), style=wx.TE_MULTILINE)
				self.tickerEdit.SetHint("Ticker")
				self.valueEdit.SetHint("Value")
				
				self.buttonContinue=wx.Button(self.panel, label="Продолжить", pos=(15, 275), size=(200, 70))
				
				self.panel.Bind(wx.EVT_BUTTON, self.btContinue, self.buttonContinue)
				self.Bind(wx.EVT_CLOSE, self.onClose, self)


			def onClose(self, event):
				self.GetParent().Enable(True)
				self.GetParent().GetParent().Enable(True)
				self.Destroy()

			def btContinue(self, event):
				tickers=self.tickerEdit.GetValue().split("\n")
				values=self.valueEdit.GetValue().split("\n")
				count=0
				if len(tickers) > len(values):
					count=len(values)
				else:
					count=len(tickers)
				result={}
				for index in range(count):
					result[tickers[index]]=values[index]
				self.GetParent().catchPastedData(type=self.type, data=result)
				self.Destroy()
				

			

		def onSpecialAddItem(self, event=None, type=""):
			numberDialog=wx.NumberEntryDialog(self, "Количество добавляемых элементов:", prompt="", caption="Диалог", value=0, min=1, max=1000)
			numberDialog.ShowModal()
			count=numberDialog.GetValue()
			for addedItem in range(count):
				self.onAddItem(event=event, type=type)


		def onAddItem(self, event=None, type=""):
			if type=="influence":
				self.influenceList.InsertItem(self.influenceList.GetItemCount(), "")
			elif type=="uses":
				self.usesList.InsertItem(self.usesList.GetItemCount(), "")
			elif type=="produces":
				self.producesList.InsertItem(self.producesList.GetItemCount(), "")

		def onRemoveItem(self, event=None, type=""):
			if type=="influence":
				while self.influenceList.GetSelectedItemCount() > 0:
					id=self.influenceList.GetFirstSelected();
					self.influenceList.DeleteItem(id)
			elif type=="uses":
				while self.usesList.GetSelectedItemCount() > 0:
					id=self.usesList.GetFirstSelected();
					self.usesList.DeleteItem(id)
			elif type=="produces":
				while self.producesList.GetSelectedItemCount() > 0:
					id=self.producesList.GetFirstSelected();
					self.producesList.DeleteItem(id)
			

		def onCloseByButton(self, event=None):
			if self.editingType=="Stocks":
				ticker=self.tickerEdit.GetValue()
				country=self.countryCombo.GetStringSelection()
				company=self.companyEdit.GetValue()
				industry=self.industrialCombo.GetStringSelection()
				description=self.descriptionEdit.GetValue().replace("\n", "§")
				uses={}
				for index in range(self.usesList.GetItemCount()):
					uses[self.usesList.GetItemText(index, 0)]=self.usesList.GetItemText(index, 1)
				produces={}
				for index in range(self.producesList.GetItemCount()):
					produces[self.producesList.GetItemText(index, 0)]=self.producesList.GetItemText(index, 1)
				startPrice=self.startPriceEdit.GetValue()
				result=Stock(ticker, country, company, industry, description, uses, produces, startPrice)
			elif self.editingType=="Commodities":
				ticker=self.tickerEdit.GetValue()
				name=self.nameEdit.GetValue()
				sector=self.sectorsCombo.GetStringSelection()
				description=self.descriptionEdit.GetValue().replace("\n", "§")
				influence={}
				for index in range(self.influenceList.GetItemCount()):
					influence[self.influenceList.GetItemText(index, 0)]=self.influenceList.GetItemText(index, 1)
				startPrice=self.startPriceEdit.GetValue()
				result=Commodity(ticker, name, sector, description, influence, startPrice)
				pass
			elif self.editingType=="Global News":
				id=self.idEdit.GetValue()
				duration=self.durationEdit.GetValue()
				force=self.forceEdit.GetValue()
				hint=self.hintEdit.GetValue().replace("\n", "§")
				text=self.textEdit.GetValue().replace("\n", "§")
				description=self.descriptionEdit.GetValue().replace("\n", "§")
				influence={}
				for index in range(self.influenceList.GetItemCount()):
					influence[self.influenceList.GetItemText(index, 0)]=self.influenceList.GetItemText(index, 1)
				nextNews=self.nextNewsCombo.GetStringSelection() + ":" + self.nextNewsSinceDays.GetValue()
				result=GlobalNews(id, duration, force, text, description, hint, influence, nextNews)
				pass
			elif self.editingType=="Local News":
				id=self.idEdit.GetValue()
				duration=self.durationEdit.GetValue()
				force=self.forceEdit.GetValue()
				country=self.countryCombo.GetStringSelection()
				hint=self.hintEdit.GetValue().replace("\n", "§")
				text=self.textEdit.GetValue().replace("\n", "§")
				description=self.descriptionEdit.GetValue().replace("\n", "§")
				influence={}
				for index in range(self.influenceList.GetItemCount()):
					influence[self.influenceList.GetItemText(index, 0)]=self.influenceList.GetItemText(index, 1)
				nextNews=self.nextNewsCombo.GetStringSelection() + ":" + self.nextNewsSinceDays.GetValue()
				result=LocalNews(id, duration, force, text, description, hint, country, influence, nextNews)
			elif self.editingType=="Corporation News":
				id=self.idEdit.GetValue()
				duration=self.durationEdit.GetValue()
				force=self.forceEdit.GetValue()
				ticker=self.tickerEdit.GetValue()
				hint=self.hintEdit.GetValue().replace("\n", "§")
				text=self.textEdit.GetValue().replace("\n", "§")
				description=self.descriptionEdit.GetValue().replace("\n", "§")
				nextNews=self.nextNewsCombo.GetStringSelection() + ":" + self.nextNewsSinceDays.GetValue()
				result=CorporationNews(id, duration, force, text, description, hint, ticker, nextNews)


			self.GetParent().GetParent().panel.catchChangedDataFromEditorWindow(asset=result)
			self.GetParent().GetParent().panel.Enable(True)
			self.GetParent().GetParent().Enable(True)
			self.GetParent().Destroy()


		def onClose(self, event=None):
			self.GetParent().GetParent().panel.Enable(True)
			self.GetParent().GetParent().Enable(True)
			self.GetParent().Destroy()

			

class ExtandedViewWindow(wx.Frame):
	def __init__(self, parent=None, editingType="", data=[]):
		super().__init__(parent=parent, title=editingType + " View", style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER|wx.STAY_ON_TOP)
		self.panel=wx.Panel(self, pos=(0, 0), size=(1000, 600))
		self.sizer=wx.BoxSizer()
		self.list=wx.ListCtrl(self.panel, pos=(0, 0), size=(1000, 600), style=wx.LC_REPORT)
		if editingType=="Stocks":
			self.list.InsertColumn(0, "ticker", width=60)
			self.list.InsertColumn(1, "country", width=70)
			self.list.InsertColumn(2, "company", width=140)
			self.list.InsertColumn(3, "industry", width=140)
			self.list.InsertColumn(4, "description", width=160)
			self.list.InsertColumn(5, "uses", width=185)
			self.list.InsertColumn(6, "produces", width=185)
			self.list.InsertColumn(7, "startPrice", width=70)
			for item in data:
				index = data.index(item)
				self.list.InsertItem(index, item.ticker)
				self.list.SetItem(index, 1, item.country)
				self.list.SetItem(index, 2, item.company)
				self.list.SetItem(index, 3, item.industry)
				self.list.SetItem(index, 4, item.description)
				self.list.SetItem(index, 5, item.getUsesString())
				self.list.SetItem(index, 6, item.getProducesString())
				self.list.SetItem(index, 7, item.startPrice)
		elif editingType=="Commodities":
			self.list.InsertColumn(0, "ticker", width=60)
			self.list.InsertColumn(1, "name", width=160)
			self.list.InsertColumn(2, "sector", width=160)
			self.list.InsertColumn(3, "description", width=310)
			self.list.InsertColumn(4, "influence", width=235)
			self.list.InsertColumn(5, "start price", width=70)
			for item in data:
				index = data.index(item)
				self.list.InsertItem(index, item.ticker)
				self.list.SetItem(index, 1, item.name)
				self.list.SetItem(index, 2, item.sector)
				self.list.SetItem(index, 3, item.description)
				self.list.SetItem(index, 4, item.getInfluenceString())
				self.list.SetItem(index, 5, item.startPrice)
		elif editingType=="Global News":
			self.list.InsertColumn(0, "ID", width=25)
			self.list.InsertColumn(1, "duration", width=60)
			self.list.InsertColumn(2, "force", width=40)
			self.list.InsertColumn(3, "text", width=220)
			self.list.InsertColumn(4, "description", width=250)
			self.list.InsertColumn(5, "hint", width=190)
			self.list.InsertColumn(6, "influence", width=210)
			self.list.InsertColumn(6, "next", width=50)
			for item in data:
				index = data.index(item)
				self.list.InsertItem(index, item.id)
				self.list.SetItem(index, 1, item.duration)
				self.list.SetItem(index, 2, item.force)
				self.list.SetItem(index, 3, item.text)
				self.list.SetItem(index, 4, item.description)
				self.list.SetItem(index, 5, item.hint)
				self.list.SetItem(index, 6, item.getInfluenceString())
				self.list.SetItem(index, 7, item.nextNews)
		elif editingType=="Local News":
			self.list.InsertColumn(0, "ID", width=25)
			self.list.InsertColumn(1, "duration", width=60)
			self.list.InsertColumn(2, "force", width=40)
			self.list.InsertColumn(3, "text", width=220)
			self.list.InsertColumn(4, "description", width=250)
			self.list.InsertColumn(5, "country", width=70)
			self.list.InsertColumn(6, "hint", width=190)
			self.list.InsertColumn(7, "influence", width=140)
			self.list.InsertColumn(6, "next", width=50)
			for item in data:
				index = data.index(item)
				self.list.InsertItem(index, item.id)
				self.list.SetItem(index, 1, item.duration)
				self.list.SetItem(index, 2, item.force)
				self.list.SetItem(index, 3, item.text)
				self.list.SetItem(index, 4, item.description)
				self.list.SetItem(index, 5, item.country)
				self.list.SetItem(index, 6, item.hint)
				self.list.SetItem(index, 7, item.getInfluenceString())
				self.list.SetItem(index, 8, item.nextNews)
		elif editingType=="Corporation News":
			self.list.InsertColumn(0, "ID", width=25)
			self.list.InsertColumn(1, "duration", width=60)
			self.list.InsertColumn(2, "force", width=40)
			self.list.InsertColumn(3, "text", width=235)
			self.list.InsertColumn(4, "description", width=345)
			self.list.InsertColumn(5, "hint", width=220)
			self.list.InsertColumn(6, "company", width=70)
			self.list.InsertColumn(6, "next", width=50)
			for item in data:
				index = data.index(item)
				self.list.InsertItem(index, item.id)
				self.list.SetItem(index, 1, item.duration)
				self.list.SetItem(index, 2, item.force)
				self.list.SetItem(index, 3, item.text)
				self.list.SetItem(index, 4, item.description)
				self.list.SetItem(index, 5, item.hint)
				self.list.SetItem(index, 6, item.ticker)
				self.list.SetItem(index, 7, item.nextNews)
				
		self.Bind(wx.EVT_LIST_COL_CLICK, self.sort, self.list)

		self.sizer.Add(self.list)
		self.panel.SetSizerAndFit(self.sizer)
		self.mainSizer=wx.BoxSizer()
		self.mainSizer.Add(self.panel)
		self.SetSizerAndFit(self.mainSizer)
		
		

		self.Bind(wx.EVT_CLOSE, self.onClose, self)


	def sort(self, event=None):
		transformedData={}
		column=event.GetColumn()
		columns={}
		for i in range(self.list.GetColumnCount()):
			columns[self.list.GetColumn(i).GetText()]=self.list.GetColumn(i).GetWidth()
		for index in range(self.list.GetItemCount()):
			temp=[]
			for item in range(self.list.GetColumnCount()):
				temp.append(self.list.GetItem(index, item).GetText())
			transformedData[self.list.GetItem(index, col=column).GetText()]=temp
		transformedData=dict(sorted(transformedData.items(), key=lambda x: x[1]))
		self.list.ClearAll()
		for i in range(len(columns)):
			self.list.InsertColumn(i, list(columns.keys())[i], width=list(columns.values())[i])
		for key, value in transformedData.items():
			self.list.InsertItem(self.list.GetItemCount(), value[0])
			for item in value:
				self.list.SetItem(list(transformedData.keys()).index(key), value.index(item), item)
				
				
			
			

	def onClose(self, event=None):
		self.GetParent().panel.Enable(True)
		self.GetParent().Enable(True)
		self.Destroy()
		



class GlobalNews:
	def __init__(self, id, duration, force, text, description, hint, influence, nextNews):
		self.id=id
		self.duration=duration
		self.force=force
		self.text=text
		self.description=description
		self.hint=hint
		self.influence=self.convertInfluenceStringToDict(influence)
		self.nextNews=nextNews

	def toString(self):
		result="gn\t{0:s}\t{1:s}\t{2:s}\t{3:s}\t{4:s}\t{5:s}\t{6:s}\t{7:s}".format(self.id, self.duration, self.force, self.text, self.description, self.hint, self.getInfluenceString(), self.nextNews)
		return result
	
	def getInfluenceString(self):
		try:
			result=""
			for key, value in self.influence.items():
				result+="{0:s}:{1:s}\\".format(key, value)
			if result=="": return ""
			return result[:-1]
		except BaseException:
			return ""

	@staticmethod
	def convertInfluenceStringToDict(input):
		if isinstance(input, dict):
			return input
		influence={}
		try:
			tempS=input.split("\\")
			for i in tempS:
				item=i.split(":")
				influence[item[0]]=item[1]
		except BaseException:
			influence={}
		return influence


class LocalNews:
	def __init__(self, id, duration, force, text, description, hint, country, influence, nextNews):
		self.id=id
		self.duration=duration
		self.force=force
		self.text=text
		self.description=description
		self.hint=hint
		self.country=country
		self.influence=self.convertInfluenceStringToDict(influence)
		self.nextNews=nextNews

	def toString(self):
		result="ln\t{0:s}\t{1:s}\t{2:s}\t{3:s}\t{4:s}\t{5:s}\t{6:s}\t{7:s}\t{8:s}".format(self.id, self.duration, self.force, self.text, self.description, self.hint, self.country, self.getInfluenceString(), self.nextNews)
		return result
	
	def getInfluenceString(self):
		try:
			result=""
			for key, value in self.influence.items():
				result+="{0:s}:{1:s}\\".format(key, value)
			if result=="": return ""
			return result[:-1]
		except BaseException:
			return ""

	@staticmethod
	def convertInfluenceStringToDict(input):
		if isinstance(input, dict):
			return input
		influence={}
		try:
			tempS=input.split("\\")
			for i in tempS:
				item=i.split(":")
				influence[item[0]]=item[1]
		except BaseException:
			influence={}
		return influence



class CorporationNews:
	def __init__(self, id, duration, force, text, description, hint, ticker, nextNews):
		self.id=id
		self.duration=duration
		self.force=force
		self.text=text
		self.description=description
		self.hint=hint
		self.ticker=ticker
		self.nextNews=nextNews

	def toString(self):
		result="cn\t{0:s}\t{1:s}\t{2:s}\t{3:s}\t{4:s}\t{5:s}\t{6:s}\t{7:s}".format(self.id, self.duration, self.force, self.text, self.description, self.hint, self.ticker, self.nextNews)
		return result


class Stock:
	def __init__(self, ticker, country, company, industry, description, uses, produces, startPrice):
		self.ticker=ticker
		self.country=country
		self.company=company
		self.industry=industry
		self.description=description
		self.uses=self.convertUsesStringToDict(uses)
		self.produces=self.convertProducesStringToDict(produces)
		self.startPrice=startPrice

	def toString(self):
		result="s\t{0:s}\t{1:s}\t{2:s}\t{3:s}\t{4:s}\t{5:s}\t{6:s}\t{7:s}".format(self.ticker, self.country, self.company, self.industry, self.description, self.getUsesString(), self.getProducesString(), self.startPrice)
		return result
	
	def getUsesString(self):
		try:
			result=""
			for key, value in self.uses.items():
				result+="{0:s}:{1:s}\\".format(key, value)
			if result=="": return ""
			return result[:-1]
		except BaseException:
			return ""
		
	def getProducesString(self):
		if len(self.produces)==0: return ""
		try:
			result=""
			for key, value in self.produces.items():
				result+="{0:s}:{1:s}\\".format(key, value)
			return result[:-1]
		except BaseException:
			return ""

	@staticmethod
	def convertUsesStringToDict(input):
		if isinstance(input, dict):
			return input
		uses={}
		try:
			tempS=input.split("\\")
			for i in tempS:
				item=i.split(":")
				uses[item[0]]=item[1]
		except BaseException:
			uses={}
		return uses
			
	@staticmethod
	def convertProducesStringToDict(input):
		if isinstance(input, dict):
			return input
		produces={}
		try:
			tempS=input.split("\\")
			for i in tempS:
				item=i.split(":")
				produces[item[0]]=item[1]
		except BaseException:
			produces={}
		return produces


class Commodity:
	def __init__(self, ticker, name, sector, description, influence, startPrice):
		self.ticker=ticker
		self.name=name
		self.sector=sector
		self.description=description
		self.influence=self.convertInfluenceStringToDict(influence)
		self.startPrice=startPrice

	def toString(self):
		return "c\t{0:s}\t{1:s}\t{2:s}\t{3:s}\t{4:s}\t{5:s}".format(self.ticker, self.name, self.sector, self.description, self.getInfluenceString(), self.startPrice)
	
	def getInfluenceString(self):
		try:
			result=""
			for key, value in self.influence.items():
				result+="{0:s}:{1:s}\\".format(key, value)
			if result=="": return ""
			return result[:-1]
		except BaseException:
			return ""
		
	@staticmethod
	def convertInfluenceStringToDict(input):
		if isinstance(input, dict):
			return input
		influence={}
		try:
			tempS=input.split("\\")
			for i in tempS:
				item=i.split(":")
				influence[item[0]]=item[1]
		except BaseException:
			influence={}
		return influence



class TextCtrlMod(wx.TextCtrl):
	def __init__(self, parent, id=wx.ID_ANY, value=wx.EmptyString, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0, validator=wx.DefaultValidator, name=wx.TextCtrlNameStr):
		super().__init__(parent, id=id, value=value, pos=pos, size=size, style=style, validator=validator, name=name)
		self.symbols=list("")
		self.dingPath="C:\Windows\Media\Windows Ding.wav"
		self.Bind(wx.EVT_TEXT, self.changeText, self)

	def changeText(self, event):
		value=event.GetString()
		flag=False
		changedValue=""
		if len(value)!=0:
			for symbol in value:
				if not symbol in self.symbols:
					flag=True
				else:
					changedValue+=symbol
		if flag:
			sound=Sound(self.dingPath)
			sound.Play()
			self.SetLabel(changedValue)

class FloatTextCtrl(TextCtrlMod):
	def __init__(self, parent, id=wx.ID_ANY, value=wx.EmptyString, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0, validator=wx.DefaultValidator, name=wx.TextCtrlNameStr):
		super().__init__(parent, id=id, value=value, pos=pos, size=size, style=style, validator=validator, name=name)
		self.symbols=list("0123456789.")


class IntTextCtrl(TextCtrlMod):
	def __init__(self, parent, id=wx.ID_ANY, value=wx.EmptyString, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0, validator=wx.DefaultValidator, name=wx.TextCtrlNameStr):
		super().__init__(parent, id=id, value=value, pos=pos, size=size, style=style, validator=validator, name=name)
		self.symbols=list("0123456789")



class FileTransformWindow(wx.Frame):
	def __init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE, name=wx.FrameNameStr):
		super().__init__(parent, id=id, title=title, pos=pos, size=size, style=style, name=name)


def encode(string="", key=0x10356):
    result=""
    for char in string:
        c=ord(char)
        result+=chr(c^key)
    return result


app=wx.App()
w=window(None, 'main')
w.Show(True)
app.MainLoop()
