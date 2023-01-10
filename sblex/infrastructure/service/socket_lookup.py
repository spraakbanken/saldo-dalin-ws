
host = "localhost"
sem_port = 8091
size = 2048 

def function(format,lemma):
        result=''
	try:
		s=socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		s.connect((host,sem_port)) 
		s.send("lem "+lemma)
		buff = ''
		while True:
			buff = s.recv(size)
			if(len(buff) == 0): break
			result += buff
		s.close() 
		result_code=apache.OK
		if format == 'xml':
			result = xmlize(result)
		elif format == 'html':
			result = htmlize(lemma,result)
	except:
		result_code=apache.HTTP_SERVICE_UNAVAILABLE
	return (result,result_code)
