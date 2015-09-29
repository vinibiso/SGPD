from django.shortcuts import render, render_to_response
from django.core.context_processors import csrf
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.core import serializers
from django.utils import simplejson, timezone
from models import User, Problem, Subproblem, Status

from django.core.mail import send_mail
import threading, random

# View responsible for rendering Main Page's Template
def mainPage(request):
	return render_to_response('index.html')

# View responsible for rendering the Processing Template
@ensure_csrf_cookie
def processingPage(request):
	userHash = request.GET.get('userHash')
	template = get_template('processing.html')
	context = {'userHash': userHash}

	return render(request, 'processing.html' ,context)

# View responsible for rendering the Contact Template
def contactPage(request):
	return render_to_response('contact.html')

# View responsible for generating and sending a new Processing Hash
def hashGenerator(request):
	loop = True
	while loop:
		serial = generator()
		exist = False
		for e in User.objects.all():
			if e.hashuser == serial:
				exist = True
				break
		if exist == False:
			loop = False

	data = {}
	data['hash'] = serial

	data_json = simplejson.dumps(data)

	query = User(hashuser = serial, dateuser=timezone.now(), pointsuser=0)
	query.save()

	return HttpResponse(data_json)

# View responsible for registering a new Problem
def problemRegister(request):
	userHash = request.GET.get('userHash')
	md5Hash = request.GET.get('md5Hash')

	user = User.objects.filter(hashuser = userHash)
	iduser = user[0]

	problem = Problem(iduser = iduser, md5hash = md5Hash, dateproblem = timezone.now(), doneproblem = False)
	problem.save()

	problem = Problem.objects.filter(iduser = iduser, md5hash = md5Hash)
	problem = problem[0]

	insert = Inserter(problem)
	insert.start()

	data = {}
	data['status'] = 'OK'
	data_json = simplejson.dumps(data)

	return HttpResponse(data_json)

# View responsible for checking the status of the user's Problems and his Points
def checker(request):
	userHash = request.GET.get('userHash')

	user = User.objects.filter(hashuser = userHash)
	user = user[0]

	objects = Problem.objects.all()
	group = objects.filter(iduser = user)

	count = 0
	problems = []
	for e in group:
		count = count + 1
		problem = {}
		problem['number'] = count
		problem['md5Hash'] = e.md5hash
		if e.doneproblem == False:
			problem['status'] = 'Em Processamento'
		else:
			problem['status'] = 'Pronto'
		problem['answer'] = e.answerproblem
		problems.append(problem)


	data = {}
	data['points'] = user.pointsuser
	data['problems'] = problems
	data_json = simplejson.dumps(data)

	return HttpResponse(data_json)

# View responsible for checking if a Hash exists
def hashChecker(request):
	userHash = request.GET.get('userHash')
	data = {}
	data['status'] = 'error'

	for e in User.objects.all():
		if e.hashuser == userHash:
			data['status'] = 'OK'
			break;

	data_json = simplejson.dumps(data)
	return HttpResponse(data_json)

# View reponsible for sending a SubProblem to a User
def pieceSender(request):
	userHash = request.POST.get('userHash')
	problem = Problem.objects.filter(doneproblem = False)
	problem = problem[0]

	status = Status.objects.filter(descstatus = 'Created')
	status = status[0]

	user = User.objects.filter(hashuser = userHash)
	user = user[0]

	subproblems = Subproblem.objects.filter(idproblem = problem, idstatus = status)
	subproblem = subproblems[0]

	status = Status.objects.filter(descstatus = 'Processing')
	status = status[0]

	Subproblem.objects.filter(idsubproblem = subproblem.idsubproblem).update(iduser = user, senddateproblem = timezone.now(), idstatus = status)

	data = {}
	data['status'] = 'OK'
	data['idSubProblem'] = subproblem.idsubproblem
	data['startString'] = subproblem.startstringsubproblem
	data['stopString'] = subproblem.stopstringsubproblem
	data['md5hash'] = problem.md5hash
	data_json = simplejson.dumps(data)

	return HttpResponse(data_json)

# View responsible for receiving the SubProblem send to the User and giving him its points
def pieceReceiver(request):
	answer = request.POST.get('answer')
 	idSubProblem = request.POST.get('idSubProblem')

 	subproblem = Subproblem.objects.filter(idsubproblem = idSubProblem)
	subproblem = subproblem[0]

	user = User.objects.filter(iduser = subproblem.iduser.iduser)
	user = user[0]

	if answer == 'false':
		status = Status.objects.filter(descstatus = 'Done')
		status = status[0]

		User.objects.filter(iduser = user.iduser).update(pointsuser = user.pointsuser + 1)
		Subproblem.objects.filter(idsubproblem = idSubProblem).update(receivedateproblem = timezone.now(), idstatus = status)

	else:
		answerString = request.POST.get('answerString')

		status = Status.objects.filter(descstatus = 'The One')
		status = status[0]

		status2 = Status.objects.filter(descstatus = 'Created')
		status2 = status2[0]

		status3 = Status.objects.filter(descstatus = 'Canceled')
		status3 = status3[0]

		Subproblem.objects.filter(idsubproblem = idSubProblem).update(receivedateproblem = timezone.now(), idstatus = status)
		User.objects.filter(iduser = user.iduser).update(pointsuser = user.pointsuser + 10)
		Subproblem.objects.filter(idproblem = subproblem.idproblem, idstatus = status2).update(idstatus = status3)
		Problem.objects.filter(md5hash = subproblem.idproblem.md5hash).update(doneproblem = True, answerproblem = answerString, datedoneproblem=subproblem.receivedateproblem, idsubproblem = subproblem.idsubproblem)

	data = {}
	data['status'] = 'OK'
	data_json = simplejson.dumps(data)

	return HttpResponse(data_json)

# Function responsible for generating a new Processing Hash
def generator():
	Sequence_A = 'ABCDEFGHIJKLMNOPQRSTUVXZ'
	Sequence_B = 'RSTUVXZLMNOPQGHIJKABCDEF'
	Sequence_C = 'STUVXZLMNOPQRABCDEFGHIJK'
	Sequence_D = 'ZXVUTSRQPONMLKJIHGFEDCBA'
	Sequence_E = '%$@!='

	First = str(random.choice(Sequence_E))
	Second = str(random.randint(3,8))
	Third = str(random.choice(Sequence_A))
	Fourth= str(random.choice(Sequence_B))
	Fifth = str(random.randint(0,9))
	Sixth = str(random.choice(Sequence_C))
	Seventh = str(random.randint(1,7))
	Eighth = str(random.randint(4,8))
	Ninth = str(random.choice(Sequence_D))
	Tenth = str(random.randint(3,5))
	Eleventh = str(random.choice(Sequence_B))
	Twelfth = str(random.choice(Sequence_A))
	Thirteenth = str(random.randint(0,9))

	serial = First+Second+Third+Fourth+Fifth+'-'+Sixth+Seventh+Eighth+Ninth+'-'+Tenth+Eleventh+Twelfth+Thirteenth

	return serial

# Threading Function responsible for, every five minutes, cleaning the SubProblem Model
def redundancy():
	threading.Timer(300, redundancy).start()

  	status = Status.objects.filter(descstatus = 'Processing')
	status = status[0]

  	subproblems = Subproblem.objects.filter(idstatus = status)

  	status = Status.objects.filter(descstatus = 'Created')
	status = status[0]

  	for e in subproblems:
  		if (e.senddateproblem - timezone.now()).seconds > 300:
  			Subproblem.objects.filter(idsubproblem = e.idsubproblem).update(idstatus = status)

  	print "CLEANED!"

# Class responsible for inserting new SubProblems of a Problem | Used by problemRegister
class Inserter (threading.Thread):
	def __init__(self, problem):
		threading.Thread.__init__(self)
		self.problem = problem

	def run(self):
		print "STARTED!"
  		status = Status.objects.filter(descstatus = 'Created')
		status = status[0]

		charArray = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','x','y','w','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','X','Y','W','Z']
		x = 0

		while x < 62:
			fl = charArray[x]
			y = 0
			while y < 62:
				sl = charArray[y]
				if y+3 > 62:
					tl = charArray[61]
					y = 62
				else:
					tl = charArray[y+3]
					y = y + 4
				subproblem = Subproblem(idproblem = self.problem, startstringsubproblem = fl+sl, stopstringsubproblem = fl+tl ,idstatus = status)
				subproblem.save()
			x = x + 1
		print "DONE!"
