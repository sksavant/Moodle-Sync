#!/usr/bin/python

import re
import mechanize
import urllib, os
from BeautifulSoup import BeautifulSoup
class Sync:
    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.courses = {}
        self.br = mechanize.Browser()
        #self.br.set_proxies({"http": "www.aero.iitb.ac.in:8081"})
        self.br.set_handle_robots(False)
        self.br.addheaders = [('User-Agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)')]
        self.logged_in = False
    	self.login()

    def login(self):
        self.br.open("http://moodle.iitb.ac.in")
        print self.br.title()
        assert self.br.viewing_html()
        self.br.select_form(nr=1)
        for i in range(3):
            self.br.form.controls[i].readonly = False
        self.br["username"] = self.username
        self.br["password"] = self.password
        self.br.submit()
        if not "Login" in self.br.title():
           self.logged_in = True
           print "Logged In"
        assert self.br.viewing_html()

    def listCourses(self):
        check = ('title', 'Click to enter this course')
        for link in self.br.links():
            if check in link.attrs:
                text = link.text.split(':')
                self.courses[text[0].strip()] = link
        return self.courses.keys()

    def syncCourses(self,storedCourses,folderNames,getpdf):
        self.storedCourses=storedCourses
        self.folderNames=folderNames;
        self.getpdf=getpdf
        for course in self.storedCourses:
            self.br.open(self.courses[course].url)
            assert self.br.viewing_html()
            allFiles = {}
            links=self.br.links()
            for link in links:
                if "mod/resource/view" in link.url:
                    name=link.text.replace('[IMG]','').replace('File ','')
                    allFiles[name] = link.url
                if "mod/folder" in link.url:
                    fullTxt=self.br.open(link.url)
                    links2=BeautifulSoup(fullTxt).findAll('a')
                    for link2 in links2:
                        if "mod_folder" in link2['href']:
                            name=link2.findAll('span')[1].string.replace('[IMG]','').replace('File ','').rsplit('.',2)[0]
                            allFiles[name]=link2['href']
            if(not(os.path.isdir(course))):
    			os.mkdir(course)

            storedFiles=os.listdir(self.folderNames[course])
            for i in xrange(0,len(storedFiles)):
                storedFiles[i] = storedFiles[i].rsplit('.',1)[0].strip()

            for afile in allFiles:
                if afile.split()[-1] == "document":
                    afilename=afile.rsplit(' ',2)[0].strip()
                else:
                    afilename=afile
                    print [afilename]

						
                if (not(afilename in storedFiles)):
                	response=self.br.open(allFiles[afile])
                	if(self.getpdf):
                		if (response.info()["Content-type"].split(";")[0]=="text/html"):
							for link in self.br.links():
								if (link.find("pluginfile.php")!=-1):
									response=self.br.open(link)
                	extension=response.geturl().rsplit('.',1)[1]
                	save_path=os.path.join(self.folderNames[course]+'/',afilename+'.'+extension.split('?')[0])
                	output=open(save_path,'w')
                	output.write(response.read())
                	output.close()

