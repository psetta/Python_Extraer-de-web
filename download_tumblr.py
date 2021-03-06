# -*- coding: utf-8 -*-

import os
import sys
import re
import socket
import urllib2
import random
from bs4 import BeautifulSoup

socket.setdefaulttimeout(10)

def operative_system():
	if os.name == "nt":
		return "windows"
	elif os.name == "poxis":
		return "linux"
	else:
		return None

def into_url():
	if len(sys.argv) > 1:
		url = sys.argv[1]
		if not re.findall("tumblr.com",url):
			print "Insert a Tumblr URL"
			sys.exit(0)
		if not re.findall("^https?://",url):
			url = "http://"+url
		return url
	else:
		print "Insert a Tumblr URL as argument"
		print "Insert '1' below to download all pages"
		sys.exit(0)
	
def read_url(url):
	try:
		print "::URL: "+url
		print " Buscando..."
		url_open = urllib2.urlopen(url)
	except urllib2.HTTPError, e:
		print "Error code - %s." % e.code
		return None
	if re.findall("text/html",url_open.info()["content-type"]):
		return url_open.read()
	else:
		return None
		
def clear():
	if operative_system() == "windows":
		os.system("cls")
	elif operative_system() == "linux":
		os.system("clear")
		
def download(archive,dir):
	#PRINT
	clear()
	if all_pages:
		print "::URL: "+page_url
	else:
		print "::URL: "+url
	print "::TOTAL: "+str(number_archives)+"/"+str(number_archives_total)
	print "Archive: "+archive
	urlopen_error=0
	try:
		archive_open_url = urllib2.urlopen(archive, timeout=10)
	except:
		urlopen_error=1
	if not urlopen_error:
		#INFO ARCHIVE
		archive_info = archive_open_url.info()
		extension = ""
		if re.findall("video",archive_info["Content-Type"]):
			extension = "."+re.findall("video/(.+)",archive_info["Content-Type"])[0]
		#FILE NAME
		name_file = archive.replace(":","").replace("?","").replace("|","")
		name_file = "".join(name_file.split("/")[-1:])
		dir_and_file_name = dir+"/"+name_file+extension
		file_number = 2
		if os.path.isfile(dir_and_file_name):
			name_file0 = name_file.split(".")[0:-1]
			extension_file = name_file.split(".")[-1]
			if name_file0 and extension_file:
				total_name = dir+"/"+name_file0+"_"+str(file_number)+"."+extension_file
			elif extension:
				total_name = dir+"/"+name_file+"_"+str(file_number)+"."+extension
			while os.path.isfile(total_name):
				file_number += 1
				if name_file0 and extension_file:
					total_name = dir+"/"+name_file0+"_"+str(file_number)+"."+extension_file
				elif extension:
					total_name = dir+"/"+name_file+"_"+str(file_number)+"."+extension
			dir_and_file_name = total_name
		file_dw = file(dir_and_file_name,"wb")
		#ARCHIVE SIZE
		size_bytes = float(archive_info["Content-Length"])
		size_mg = size_bytes / (1024*1024)
		if len(str(size_mg).split(".")) > 1:
			size_mg_show = str(size_mg).split(".")[0]+"."+str(size_mg).split(".")[1][:3]
		else:
			size_mg_show = str(size_mg)
		#BUFFER
		bytes_pp = int(size_bytes / 40)
		bytes_pp = min(bytes_pp, 80000)
		bytes_pp = max(bytes_pp, 10000)
		per = 0
		download_bytes = 0
		while True:
			#CLEAR
			clear()
			#PRINT
			if all_pages:
				print "::URL: "+page_url
			else:
				print "::URL: "+url
			print "::TOTAL: "+str(number_archives)+"/"+str(number_archives_total)
			print "Archive: "+archive
			print "Content-Type: "+archive_info["Content-Type"]
			print "Content-Length: "+size_mg_show+" MiB"
			print "Download... "+str(per)[0:5]+"%"
			#BUFFER
			buffer = archive_open_url.read(bytes_pp)
			if not buffer:
				break
			download_bytes += len(buffer)
			try:
				file_dw.write(buffer)
			except:
				break
			per = (download_bytes/size_bytes)*100
		
def download_archives(archives, dir):
	global number_archives
	global number_archives_total
	if len(archives) > 0:
		#DOWNLAOD ARCHIVES
		number_archives_total = len(archives)
		number_archives = 1
		for archive in archives:
			try:
				download(archive,dir_name)
			except:
				None
			number_archives += 1
	else:
		print "\t- No archives"
		
def download_archives_to_page(url, dir):
	html = read_url(url)
	archives = extract_archives_url_to_html(html)
	download_archives(archives, dir_name)
		
def extract_archives_url_to_html(html):
	global number_archives_total
	global number_archives
	if html:
		#SOUP
		web_soup = BeautifulSoup(html, "html.parser")
		all_img = []
		all_img_photoset = []
		all_iframe = []
		#ARTICLE
		all_articles = web_soup.find_all("article")
		for article in all_articles:
			#FIGURE
			try:
				find_figure = article.figure
				if find_figure:
					#IMG
					try:
						if find_figure.find_all("img"):
							find_imgs = find_figure.find_all("img")
							for img in find_imgs:
								all_img.append(img)
					except:
						None
					#IFRAME
					try:
						if find_figure.iframe:
							all_iframe.append(find_figure.iframe)
					except:
						None
			except:
				None
		#LI CLASS=POST
		all_li_post = web_soup.find_all("li", class_="post")
		for post in all_li_post:
			#IMG
			try:
				if post.find_all("img"):
					find_imgs = post.find_all("img")
					for img in find_imgs:
						all_img.append(img)
			except:
				None
			#IFRAME
			try:
				if post.iframe:
					all_iframe.append(post.iframe)
			except:
				None
		#DIV CLASS=POSTS
		all_div_posts = web_soup.find_all("div", class_="posts")
		for post in all_div_posts:
			#IMG
			try:
				if post.find_all("img"):
					find_imgs = post.find_all("img")
					for img in find_imgs:
						all_img.append(img)
			except:
				None
			#IFRAME
			try:
				if post.iframe:
					all_iframe.append(post.iframe)
			except:
				None
		#DIV CLASS=POST
		all_div_post = web_soup.find_all("div", class_="post")
		for post in all_div_post:
			#IMG
			try:
				if post.find_all("img"):
					find_imgs = post.find_all("img")
					for img in find_imgs:
						all_img.append(img)
			except:
				None
			#IFRAME
			try:
				if post.iframe:
					all_iframe.append(post.iframe)
			except:
				None
		#DIV CLASS=POST-PANEL
		all_div_post = web_soup.find_all("div", class_="post-panel")
		for post in all_div_post:
			#IMG
			try:
				if post.find_all("img"):
					find_imgs = post.find_all("img")
					for img in find_imgs:
						all_img.append(img)
			except:
				None
			#IFRAME
			try:
				if post.iframe:
					all_iframe.append(post.iframe)
			except:
				None
		#DIV CLASS=MEDIA
		all_div_post = web_soup.find_all("div", class_="media")
		for post in all_div_post:
			#IMG
			try:
				if post.find_all("img"):
					find_imgs = post.find_all("img")
					for img in find_imgs:
						all_img.append(img)
			except:
				None
			#IFRAME
			try:
				if post.iframe:
					all_iframe.append(post.iframe)
			except:
				None
		#DIV ID=POSTS
		all_div_post = web_soup.find_all("div", id="posts")
		for post in all_div_post:
			#IMG
			try:
				if post.find_all("img"):
					find_imgs = post.find_all("img")
					for img in find_imgs:
						all_img.append(img)
			except:
				None
			#IFRAME
			try:
				if post.iframe:
					all_iframe.append(post.iframe)
			except:
				None
		#DIV CLASS=ENTRY
		all_div_entry = web_soup.find_all("div", class_="entry")
		for post in all_div_entry:
			#IMG
			try:
				if post.find_all("img"):
					find_imgs = post.find_all("img")
					for img in find_imgs:
						all_img.append(img)
			except:
				None
			#IFRAME
			try:
				if post.iframe:
					all_iframe.append(post.iframe)
			except:
				None
		########PHOTOSET########
		#DIV CLASS=HTML_PHOTOSET
		all_div_photoset = web_soup.find_all("div", class_="html_photoset")
		for post in all_div_photoset:
			try:
				if post.find_all("iframe"):
					#SRC
					photoset_url = post.find("iframe")["src"]
					sort_url = url.split("/")[:3]
					sort_url = "/".join(sort_url)
					photoset_complete_url = sort_url+photoset_url
					download_archives_to_page(photoset_complete_url, dir_name)
			except:
				None
		#DIV CLASS=PHOTOSET
		all_div_photoset_2 = web_soup.find_all("div", class_="photoset")
		for post in all_div_photoset_2:
			try:
				if post.find_all("a", href=True):
					a_all = post.find_all("a")
					for a in a_all:
						all_img_photoset.append(a["href"])
			except:
				None
		################
		#DIV ALL
		if not all_img:
			all_div = web_soup.find_all("div")
			for post in all_div:
				#IMG
				try:
					if post.find_all("img"):
						if not post.find_all("a", class_="user-avatar"):
							find_imgs = post.find_all("img")
							for img in find_imgs:
								all_img.append(img)
				except:
					None
				#IFRAME
				try:
					if post.iframe:
						all_iframe.append(post.iframe)
				except:
					None
		#EXTRACCION SRC FROM IMG AND IFRAMES
		imgs_src = []
		iframes_src = []
		#SRC IN IMG
		for img in all_img:
			if img["src"]:
				imgs_src.append(img["src"])
		#all_img_photoset
		imgs_src += all_img_photoset
		#SRC IN IFRAME
		for iframe in all_iframe:
			if iframe["src"]:
				iframes_src.append(iframe["src"])
		
		#ARCHIVES
		archives = []
			#IMGS
		for src in imgs_src:
			archives.append(src)
			#IFRAMES
		for src in iframes_src:
			try:
				open_archive_url = urllib2.urlopen(src)
			except:
				open_archive_url = False
			if open_archive_url:
				archive_type = open_archive_url.info()["content-type"]
				if re.findall("text/html",archive_type):
					archive_html = open_archive_url.read()
					#SOUP
					archive_soup = BeautifulSoup(archive_html, "html.parser")
					#SOURCE
					sources = archive_soup.find_all("source")
					for source in sources:
						try:
							archives.append(source["src"])
						except:
							None
					#IMG
					imgs = archive_soup.find_all("img")
					for img in imgs:
						try:
							archives.append(img["src"])
						except:
							None
					#EXTRACT HREF FOR A_LINKS
					#a_tags = archive_soup.find_all("a")
					#for a in a_tags:
					#	try:
					#		archives.append(a["href"])
					#	except:
					#		None
		return list(set(archives))
	
def download_all_pages(url, dir):
	global page_url
	page=1
	#LOOP
	while True:
		if re.findall("page/$",url):
			complete_url = url+str(page)
		elif re.findall("page$",url):
			complete_url = url+"/"+str(page)
		elif re.findall("/$",url):
			complete_url = url+"page/"+str(page)
		else:
			complete_url = url+"/page/"+str(page)
		page_url = complete_url
		html = read_url(page_url)
		archives = extract_archives_url_to_html(html)
		if len(archives) > 0:
			download_archives(archives, dir_name)
			page += 1
			next = 0
			clear()
		else:
			##NEXT_PAGE
			soap_html = BeautifulSoup(html, "html.parser")
			all_a_next = soap_html.find_all("a", class_="next")
			if not all_a_next or next >= 10:
				break
			else:
				clear()
				next += 1
				page += 1

###### MAIN
def main(main_url=False,main_all_pages=False):
	clear()
	global url
	global dir_name
	global all_pages
	#URL
	if main_url:
		url = main_url
	else:
		url = into_url()
	sort_url = url.split("/")[2:]
	#ALL_PAGES
	if main_all_pages:
		all_pages = main_all_pages
	else:
		if len(sys.argv) > 2:
			all_pages = True if sys.argv[2] in ["1","True","all"] else False
		else:
			all_pages = False
	#LAUNCH
	if url:
		#DIR NAME
		dir_name = "_".join(url.split("/")[2:])
		dir_number = 2
		if all_pages:
			dir_name = dir_name+"_all"
		if os.path.isdir(dir_name):
			while os.path.isdir(dir_name+"_"+str(dir_number)):
				dir_number += 1
			dir_name = dir_name+"_"+str(dir_number)
		os.mkdir(dir_name)
		##DOWNLOAD##
		if all_pages:
			download_all_pages(url,dir_name)
		else:
			download_archives_to_page(url,dir_name)
		print " DESCARGA COMPLETADA!"

if __name__ == "__main__":			
	main()
	
	