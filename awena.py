# -*- coding: UTF-8 -*-

# Awena - Alternative Wikidata Enquiry Application

import requests

class Crawler:

	VERSION					= "0.1"
	USER_AGENT			= "Mozilla/5.0 (compatible; Awena/"+VERSION+"; +https://github.com/sedthh/awena-wikidata-crawler/)"

	##### CONSTRUCTOR #####
	def __init__(self,	lang='en'):
		self.lang				= lang.lower()
		self.cache				= {}
		self.n					= 0
		
	##### DATA MODEL #####
	def __repr__(self):
		return "<Awena Search instance at {0}>".format(hex(id(self)))
		
	def __str__(self):
		return self.query

	def __len__(self):
		return len(self.cache)
		
	def __eq__(self, other):
		if isinstance(other, bool):
			return bool(self.cache)==other
		return False
	
	def __ne__(self, other):
		return not self.__eq__(other)
	
	##### CLASS FUNCTIONS #####
	
	def number_of_requests(self):
		return self.n
	
	def search(self, query):
		return self._request(query,False)
		
	def load(self,id=None):
		if not id:
			return {}
		if id not in self.cache:
			data		= self._request(False,id)
			self.cache[id]= self._parse(data,id)
		return self.cache[id]
	
	def _request(self,query=False,id=False):
		headers	= {
			"User-Agent"	: Crawler.USER_AGENT
		}
		if id:
			params	= {
				"action"		: "wbgetentities",
				"ids"			: id,
				"language"		: self.lang,
				"format"		: "json"
			}
		else:
			if not query:
				return None
			query	= query.strip()
			params	= {
				"action"		: "wbsearchentities",
				"search"		: query,
				"language"		: self.lang,
				"format"		: "json"
			}
		data	= requests.get("https://www.wikidata.org/w/api.php",headers=headers,params=params)
		result	= data.json()

		# for i,j in result.items():
		# 	# print(i," : ",j)
		self.n	+= 1
		if 'error' in result:	
			raise Exception(result['error']['code'],result['error']['info'])
		elif query and "search" in result and result["search"]:
			guess	= None
			for item in result["search"]:
				if "id" in item and "match" in item and "text" in item["match"] and "language" in item["match"]:
					if item["match"]["language"]==self.lang:
						# if not guess: 
						# 	guess	= item["id"]
						
						if query.lower()==item["display"]['label']['value'].lower():
							return item['id']
						
			for item in result["search"]:
				if 'id' in item and 'match' in item and 'text' in item["match"] and 'language' in item['match']:
					if item['match']['language']==self.lang:
						if query.lower().strip() in item["display"]["label"]['value'].lower().strip():
							return item["id"]
				# return guess
		elif id and "entities" in result and result["entities"]:
			if id in result["entities"] and result["entities"][id]:
				return result["entities"][id]
		if query:
			for item in result["search"]:
				return item["id"]
		return None
		
	def _parse(self,data,id):
		relation={'P6379', 'P749', 'P366', 'P739', 'P121', 'P4950', 'P131', 'P495', 'P625', 'P355', 'P463', 'P5009', 'P17', 'P1830', 'P452', 'P306', 'P176', 'P169', 'P199', 'P1344', 'P156', 'P2770', 'P3320', 'P113', 'P1454', 'P159', 'P740', 'P114', 'P31', 'P1056', 'P1889', 'P166', 'P400', 'P361', 'P155', 'P127', 'P112', 'P793'}

		result	= {"id":id}
		if id and data:
			if "labels" in data:
				if self.lang in data["labels"]:
					result["label"]		= data["labels"][self.lang]["value"]
			# if "descriptions" in data:
			# 	if self.lang in data["descriptions"]:
			# 		result["description"]	= data["descriptions"][self.lang]["value"]
			if "claims" in data:
				for key in relation:
				# for key	in data["claims"]:
					if key in data["claims"]:
						try:
							if key=='P414':
								node=[]
								for i in range(len(data['claims'][key])):
									node.append(data['claims'][key][i]['qualifiers']['P249'][0]['datavalue']['value'])
								result['ticker']=node
								
							if type(data['claims'][key][0]['mainsnak']['datavalue']['value'])==dict and "id" in data["claims"][key][0]["mainsnak"]["datavalue"]['value'].keys():
								node=[]
								for i in range(len(data['claims'][key])):
									node.append(data['claims'][key][i]['mainsnak']['datavalue']['value']['id'])
								result[key]=node
				
							
						except KeyError:
							pass
					else:
						result[key]='None'		
		return result

	def stock_exchange(self,id=None):
		if not id:
			return False
		if id not in self.cache:
			data=self._request(False,id)
			if id and data:
				if 'claims' in data:
					if 'P414' in data['claims']:
						return True
					else: return False
				else:
					return False
					

		
					