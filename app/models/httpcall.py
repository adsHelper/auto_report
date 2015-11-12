# -*- coding: utf-8 -*-
import urllib2

ddd = None

class HttpCall(object):
	"""请求发送类"""
	def __init__(self, url,requests,param='',header='',cookie=''):
		super(ClassName, self).__init__()
		self.header = header
		self.cookie = cookie
		self.url = url
		self.requests = requests

	def send(self):
	 	try:
	 	 	cookieHandle = urllib2.HTTPCookieProcessor()
	 	 	opener = urllib2.build_opener(cookieHandle)
			opener = addHeaders(opener)
			opener = addCookies(opener)
			urllib2.install_opener(opener)
			if len(self.param)>0:
				request = urllib2.Request(self.url,self.param)
			else:
				request = urllib2.Request(url)
			response = opener.open(request)
			body = response.read()
			decodejson = json.loads(body)
		except Exception, e:
			raise e 

	def addCookies(self,opener):
		if(len(self.cookies)>0):
			opener.addheaders.append("Cookie",cookies)
			return opener

	def addHeaders(self,opener):
		if len(self.header)>0:
			for (key,value) in header.items():
				opener.addheaders.append(key,value)
			return opener

def main():
	httpcall = HttpCall()

if __name__ == '__main__':
	main()