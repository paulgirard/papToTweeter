#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Josh Rendek 2009 bluescripts.net 
# No liability blah blah use at your own risk, etc 


import lxml.html as html
from urllib import urlopen 
import re 
import random 
from os import popen
from datetime import datetime

#specify user / pass 
user = "crisedulogement" 
password = "gicipa"   
#raw xml 

papPage="http://www.pap.fr/annonce/locations-appartement-paris-01er-g37768g37769g37770g37771g37772g37773g37774g37776g37777g37778g37785g37786g37787-jusqu-a-850-euros-a-partir-de-30-m2" 
  
#xml parsed 
doc=html.parse(papPage)
doc=doc.getroot()
annonces=doc.find_class("annonce")

stringAnnonces=[]


for annonce in annonces :
	tweet=[]
	prix=annonce.find_class("prix")[0]
	surface=annonce.find_class("surface")[0]
	description=annonce.find_class("annonce-resume-texte")[0]
	header=annonce.xpath("h2")[0]
	url=annonce.xpath("h2/a/@href")[0]
	url = "\t\t\thttp://www.pap.fr"+url
	
	#	print prix.text_content().encode("utf-8")
#	print surface.text_content().encode("utf-8")
#	print paris


	# filtrage des meublés
	if not re.search("(.{10} meubl[eé].{10})",description.text_content().encode("utf-8")) :

		#stringAnnonce= surface.text_content().encode("utf-8")+" "+prix.text_content().encode("utf-8")+" "	
		surface,prix,piece=re.match(".*?(\d{3}.{5}).*?(\d{2}.{6})(.*)",re.sub(" +"," ",re.sub("[\r\t\n]+|appartement|Location|Paris"," ",header.text_content().encode("utf_8")))).groups()
		tweet+=surface,prix,piece
		try :
			metro="metro "+annonce.find_class("metro")[0].text_content().encode("utf-8")
		except :
			metro=""
		try :
			tel=re.search("((\d{2}\W*?){4}\d{2})",description.text_content().strip().encode("utf-8")).group(0)
		except :
			tel=""
		
		tweet.append(metro)	
		tweet.append(tel)	
		tweet.append(url)
		stringAnnonce=" ".join(tweet)
			
		stringAnnonces.append(stringAnnonce+"\n")
		#print stringAnnonce[0:140]
	

try :
	file=open("/home/pom/pap/lastAnnonces.txt")
	lastAnnonces=file.readlines()
	file.close()
except :
	lastAnnonces=[]

for	annonce in stringAnnonces :
	if annonce in lastAnnonces :
		pass
	else :
		print annonce
		url = 'http://twitter.com/statuses/update.xml' 
		curl = 'curl -s -u %s:%s -d status="%s" %s' % (user,password,annonce[0:135]+" "+datetime.now().strftime("%H:%M"),url) 
		p = popen(curl)   

file=open("/home/pom/pap/lastAnnonces.txt","w")
for string in stringAnnonces :
	file.write(string)
file.close()
