import json
import sys
import os

def main():
	if len(sys.argv) < 3:
		print "Error: Not enough arguments"
		exit()
	elif sys.argv[1] == "AddUser":
		if len(sys.argv) != 4:
			sys.exit("Error: wrong number of arguments")
		addUser(str(sys.argv[2]),str(sys.argv[3]))
		
	elif sys.argv[1] == "Authenticate":
		if len(sys.argv) != 4:
			sys.exit("Error: wrong number of arguments")
		authenticate(str(sys.argv[2]),str(sys.argv[3]))
		
	elif sys.argv[1] == "SetDomain":
		if len(sys.argv) != 4:
			sys.exit("Error: wrong number of arguments")
		setDomain(str(sys.argv[2]),str(sys.argv[3]))
		
	elif sys.argv[1] == "DomainInfo":
		if len(sys.argv) != 3:
			sys.exit("Error: wrong number of arguments")
		domainInfo(str(sys.argv[2]))
	elif sys.argv[1] == "SetType":
		if len(sys.argv) != 4:
			sys.exit("Error: wrong number of arguments")
		setType((sys.argv[2]),str(sys.argv[3]))
		
	elif sys.argv[1] == "TypeInfo":
		if len(sys.argv) != 3:
			sys.exit("Error: wrong number of arguments")
		typeInfo((sys.argv[2]))
		
	elif sys.argv[1] == "AddAccess":
		if len(sys.argv) != 5:
			sys.exit("Error: wrong number of arguments")
		addAccess((sys.argv[2]),str(sys.argv[3]),str(sys.argv[4]))
		
	elif sys.argv[1] == "CanAccess":
		if len(sys.argv) != 5:
			sys.exit("Error: wrong number of arguments")
		canAccess((sys.argv[2]),str(sys.argv[3]),str(sys.argv[4]))
	else:
		sys.exit("Error: wrong command")


def canAccess(operation, user, object_Name):
	if operation == "":
		print "Error: missing operation"
		sys.exit()
		
	if user == "":
		print "Error: missing user"
		sys.exit()
	
	if object_Name == "":
		print "Error: missing type"
		sys.exit()
		
		
	with open('domains.json') as j:
		domains = json.load(j)
		
	with open('types_file.json') as p:
		typeNames = json.load(p)
	
	with open('operations_file.json') as f:
		operations_file = json.load(f)
	
	for i, userList in domains[0].items():
		if user in userList:
			for k, objectList in typeNames[0].items():
				if object_Name in objectList:
					if i in operations_file[operation]:
						if k in operations_file[operation][i]:
							print "Success"
							sys.exit()
	print "Error: access denied"


def addAccess(operation, domain_name, type_name):
	
	if operation == "":
		print "Error: missing operation"
		sys.exit()
		
	if domain_name == "":
		print "Error: missing domain"
		sys.exit()
	
	if type_name == "":
		print "Error: missing type"
		sys.exit()
		
	
	operations = {}
	flag1 = False
	flag2 = False
	with open('domains.json') as f:
		domains = json.load(f)
		
	for i, userList in domains[0].items():
		if domain_name in i:
			flag1 = True
			break
	if flag1 == False:
		#create new empty domain
		with open('domains.json') as p:
			data = json.load(p)
		if type (data) is dict:
			data = [data]
		#domain = [userName]
		data[0][domain_name] = []
		with open ('domains.json', 'w') as outfile:
			json.dump(data,outfile)
	
	
	with open('types_file.json') as k:
		types_file = json.load(k)
	for i, objectList in types_file[0].items():
		if type_name in i:
			flag2 = True
			break
	
	if flag2 == False:
		#create new empty type
		with open('types_file.json', 'a+') as p:
			data = json.load(p)
		if type (data) is dict:
			data = [data]
		#domain = [userName]
		data[0][type_name] = []
		with open ('types_file.json', 'w') as outfile:
			json.dump(data,outfile)

	
		
	with open('domains.json') as f:
		domains = json.load(f)	
	for i, userList in domains[0].items():
		if domain_name in i:
			with open('types_file.json') as k:
				types_file = json.load(k)
			for i, objectList in types_file[0].items():
				if type_name in i:
					if os.path.exists('operations_file.json') == False:
						operations[operation] = {}
						operations[operation][domain_name] = [type_name]
						with open('operations_file.json','a+') as m:
							json.dump(operations,m)
							sys.exit("Success added operation")
					
					else:
						with open('operations_file.json','a+') as f:
							operations_file = json.load(f)
						
						for k, op in operations_file.items():
							if operation in k: #1
								#check if domains exist in the operations if yes:,
								for i, domainList in operations_file[k].items():
									if domain_name in op: #2
										#check if type is in domains if yes:
										if type_name in domainList:#3
											#dont do nothing
											print "Success nothing to enter"
											sys.exit()
										else: #3
											#else add type to domains
											domainList.append(type_name)
											with open ('operations_file.json', 'w') as t:
												json.dump(operations_file,t)
											print ("Success " +  domain_name + " can " + operation + " " + type_name)
											sys.exit()
									#else add domain to operation with type	
									#else: #2
								operations_file[k][domain_name] = [type_name]
								with open('operations_file.json','w') as e:
									json.dump(operations_file,e)
								sys.exit("Success " + domain_name + " can " + operation)
									
							#else: #1
							#else add everything to operations_file with since it is not empty
						operations_file[operation] = {}
						operations_file[operation][domain_name] = [type_name]
						with open('operations_file.json','w') as f:
							json.dump(operations_file,f)
						sys.exit("Success added everything to file")
		
			
			
	
	
		

def typeInfo(typeName):
	if(typeName == ""):
		print "Error: missing type Name"
		sys.exit()
		
	with open('types_file.json') as j:
		typeNames = json.load(j)
	
	for i, objectList in typeNames[0].items():
		if typeName in i:
			for i in objectList:
				print i
	

def setType(objectName, typeName):
	typeNames = [{}]
	if ((objectName == "") or (typeName == "")):
		sys.exit("Error: missing object or type name")

	if os.path.exists('types_file.json') == False:
		typeNames [0][typeName] = [objectName]
		with open('types_file.json','a+') as f:
			json.dump(typeNames,f)
		sys.exit("Success added object to " + str(typeName))
	else:
		with open('types_file.json') as j:
			typeNames = json.load(j)
		for i, objectList in typeNames[0].items():
			if typeName in i: 
				if objectName in objectList:
					print ("Success " + str(objectName) + " already in " + str(typeName))
					sys.exit()
				else:
					objectList.append(objectName)
					with open ('types_file.json', 'w') as outfile:
						json.dump(typeNames,outfile)
					print  ("Success " + str(objectName) + " set as " + str(typeName) + " type")
					sys.exit()
					
					
		with open('types_file.json') as p:
			data = json.load(p)
		if type (data) is dict:
			data = [data]
		data[0][typeName] = [objectName]
		with open ('types_file.json', 'w') as outfile:
			json.dump(data,outfile)
		print ("Success added " + str(objectName) + " to " + str(typeName) + " type")
		sys.exit()

def domainInfo(domainName):
	if domainName == "":
		print "Error: missing domain"
		sys.exit()
	
	with open('domains.json') as j:
		domains = json.load(j)
	
	for i, userList in domains[0].items():
		if domainName in i:
			for i in userList:
				print i
			
		
def setDomain(userName, domain):
	domains = [{}]
	if domain == "" :
		print "Error: missing domain"
		sys.exit()
		
	with open('users.json') as f:
		users = json.load(f)
		
	for i in range(len(users)):
		nameChecker = users[i]['user']
		if(nameChecker == userName):
			if os.path.exists('domains.json') == False:
				domains [0][domain] = [userName]
				with open('domains.json','a+') as k:
					json.dump(domains,k)
				sys.exit("Success domain added")
			else:
				with open('domains.json') as j:
					domains = json.load(j)
				for i, userList in domains[0].items():
					if domain in i: 
						if userName in userList:
							print "Success user already exists"
							sys.exit()
						else:
							userList.append(userName)
							with open ('domains.json', 'w') as outfile:
								json.dump(domains,outfile)
							print "Success user added"
							sys.exit()
					
					
				with open('domains.json') as p:
					data = json.load(p)
				if type (data) is dict:
					data = [data]
				data[0][domain] = [userName]
				with open ('domains.json', 'w') as outfile:
					json.dump(data,outfile)
				print "Success added new domain and user"
				sys.exit()
	print "Error: no such user"
					
def authenticate(userName, password):
	with open('users.json') as f:
		data = json.load(f)
	for i in range(len(data)):
		nameChecker = data[i]['user']
		if(nameChecker == userName):
			if(password != data[i]['password']):
				sys.exit("Error: bad password")
			else:
				sys.exit("Success")
	
	print "Error: no such user"

def addUser(userName, password):
	
	if userName == "":
		print "Error: username missing"
		sys.exit()
	
	if os.path.exists('users.json') == False:
		user = [{'user':userName,'password': password
		}]
		with open ('users.json','a+') as f:
			json.dump(user,f)
		print "Success"
		sys.exit()
	
	else:
		with open('users.json') as f:
			data = json.load(f)
		
		for i in range(len(data)):
			nameChecker = data[i]['user']
			if(nameChecker == userName):
				sys.exit("Error: user exists")
				
		if type (data) is dict:
			data = [data]
		data.append( 
			{
			'user' : userName,
			'password': password
			})
		with open ('users.json', 'w') as outfile:
			json.dump(data,outfile)
			print "Success"
	
	
def domainInfo(domainName):
	with open('domains.json') as j:
		domains = json.load(j)
	if(domainName == ""):
		print "Error: missing domain"
		sys.exit()
	
	for i, userList in domains[0].items():
		if domainName in i:
			for i in userList:
				print i
				


if __name__ == '__main__':
	main()
