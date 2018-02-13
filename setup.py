import os
import sys
import subprocess

dependencies = ['bs4', 'fuzzywuzzy', 'trakt', 'simplejson', 'feedparser']
dependencies3 = ['discord.py', 'multidict', 'websockets']
noRtorrent = "The program \'rtorrent\' is currently not installed. You can install it by typing:\napt install rtorrent"
rtorrentAuto = '#system.method.set_key=event.download.finished,ascript,\"execute=python,/home/seedbox/ani-script/superScript.py,$d.get_base_path=,$d.get_hash=,$d.get_name=\"'
cronTabData = "0,30 * * * * cd /home/seedbox/ani-script && python pull2.py > /tmp/pull2.log\n5,35 * * * * cd /home/seedbox/ani-script && python pull.py > /tmp/pull.log\n0,0 * * * 0 cd /home/seedbox/ani-script && python delete.py > /tmp/delete.log\n5,0 * * * 0 cd /home/seedbox/downloads/Anime && find -size 0 -delete\n"

def checkRutorrent():
	try:
		process = subprocess.Popen(["rtorrent", "-h"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		while True:
			output = process.stdout.readline()
			error = process.stderr.readline()
			print ("Rtorrent is installed")
			os.chdir(os.path.expanduser('~'))
			lineInFile = False
			with open(".rtorrent.rc", "r") as ins:
				for line in ins:
					if line.strip() == rtorrentAuto.strip():
						lineInFile = True
			ins.close()

			if(lineInFile == False):
				ins = open(".rtorrent.rc", "a")
				ins.write(rtorrentAuto)
				ins.write('\n')
				ins.close()

			return
	except OSError as e:
		if e.errno == os.errno.ENOENT:
			print ("Rtorrent not installed")
		else:
			raise

def cronTabAdding():
	homedir = os.environ['HOME']
	try:
		process = subprocess.Popen(["crontab", "-l"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		while True:
			output = process.stdout.readline()
			error = process.stderr.readline()
			noCronMessage = "b\'no crontab for " + str(homedir[6:] + '\'') #darn byte notation
			if str(error.strip()) == noCronMessage:
				tempCron = open("cron.tmp", "w+")
				tempCron.write(cronTabData)
				tempCron.close()
				process = subprocess.Popen(["crontab", "-u", homedir[6:], "cron.tmp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				output = process.stdout.readline()
				error = process.stderr.readline()
				os.remove("cron.tmp")
			else:
				cronList = cronTabData.split('\n')
				del cronList[4]
				process = subprocess.Popen(["crontab", "-l"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				tempCron = open("cron.tmp", "w+")
				#write output to file and then append the missing commands from remaining cronlist
				while True:
					output = process.stdout.readline()
					outputClean = str(output, 'utf-8')
					tempCron.write(outputClean)
					if outputClean == '' or outputClean == '\n':
						tempCron.close()
						break
					if output:
						for lines in cronList:
							if (str(output) == 'b\'' + lines + '\\n\''):
								print ("Line Found")
								cronList.remove(lines)

				if(len(cronList) == 0):
					pass
					print("all commands Found")
					os.remove("cron.tmp")
				else:
					#one or more commands are missing
					print ("Dank")
					tempCron = open("cron.tmp", "a+")
					for lines in cronList:
						tempCron.write(lines + '\n')
					tempCron.close()
					process = subprocess.Popen(["crontab", "-u", homedir[6:], "cron.tmp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
					output = process.stdout.readline()
					error = process.stderr.readline()
					os.remove("cron.tmp")
			break
	except OSError as e:
		print (type(e))
		if e.errno == os.errno.ENOENT:
			print ("File Not Found?")
		else:
			raise

def checkForRTcontrol():
	pass

def constructVarFile():
	pass

def getPipList():
	try:
		packages = []
		process = subprocess.Popen(["sudo", "pip", "list", "--format=legacy"], stdout=subprocess.PIPE)
		while True:
			output = process.stdout.readline()
			if output != b'':
				package_Name = output[0:str(output).find(' ', 0)-2]
				package_Version = output[str(output).rfind(' '):len(str(output))-6].strip()
				#print ("name: " + str(package_Name) + " version: " + str(package_Version))
				installed_package = {'Name': str(package_Name).strip(), 'Version': str(package_Version).strip()}
				packages.append(installed_package)
			else:
				break
		return packages
	except OSError as e:
		print (type(e))
		if e.errno == os.errno.ENOENT:
			print ("File Not Found?")
		else:
			raise

def getPip3List():
	try:
		packages = []
		process = subprocess.Popen(["sudo", "pip3", "list", "--format=legacy"], stdout=subprocess.PIPE)
		while True:
			output = process.stdout.readline()
			if output != b'':
				package_Name = output[0:str(output).find(' ', 0)-2]
				package_Version = output[str(output).rfind(' '):len(str(output))-6].strip()
				#print ("name3: " + str(package_Name) + " version: " + str(package_Version))
				installed_package = {'Name': str(package_Name).strip(), 'Version': str(package_Version).strip()}
				packages.append(installed_package)
			else:
				break
		return packages
	except OSError as e:
		print (type(e))
		if e.errno == os.errno.ENOENT:
			print ("File Not Found?")
		else:
			raise

def checkList(packages):
	allPackageNames = []
	remainingDependicies = []
	index = 0

	for element in dependencies:
		remainingDependicies.append(element)

	for package in packages:
		allPackageNames.append(packages[index]['Name'])
		index+=1

	for term in dependencies:
		byteTerm = 'b\'' + term + '\'' #add binary typing ish
		if byteTerm in allPackageNames:
			remainingDependicies.remove(term)

	return remainingDependicies

def check3List(packages):
	allPackageNames = []
	remainingDependicies = []
	index = 0

	for element in dependencies3:
		remainingDependicies.append(element)

	for package in packages:
		allPackageNames.append(packages[index]['Name'])
		index+=1

	for term in dependencies3:
		byteTerm = 'b\'' + term + '\'' #add binary typing ish
		if byteTerm in allPackageNames:
			remainingDependicies.remove(term)

	return remainingDependicies

def installMissingDependicies(dependencies):
    failedToFind = b'No matching distribution found for'
    for package in dependencies:
        #print (package)
        process = subprocess.Popen(["sudo", "pip", "install", package], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while True:
            output = process.stdout.readline()
            error = process.stderr.readline()
            if(failedToFind in error):
                break
            if output == '' and process.poll() is not None:
                break
            if output:
                pass
        rc = process.poll()

def installMissing3Dependicies(dependencies):
	failedToFind = b'No matching distribution found for'
	for package in dependencies:
		process = subprocess.Popen(["sudo", "pip3", "install", package], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		while True:
			output = process.stdout.readline()
			error = process.stderr.readline()
			if(failedToFind in error):
				break
			if output == '' and process.poll() is not None:
				break
			if output:
				pass
		rc = process.poll()

cronTabAdding()
#checkRutorrent()
# packages = getPipList()
# packages3 = getPip3List()
# theDependiciesLeft = checkList(packages)
# theDependicies3Left = check3List(packages3)
# if(len(theDependicies3Left) == 0):
# 	print ("All Deps of Pip3 installed")
# else:
# 	installMissing3Dependicies(theDependicies3Left)
# if(len(theDependiciesLeft) == 0):
# 	print ("All Deps of Pip installed")
# else:
# 	installMissingDependicies(theDependiciesLeft)
