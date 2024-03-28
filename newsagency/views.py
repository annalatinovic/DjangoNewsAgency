from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from datetime import datetime, date
from newsagency.models import Story
import json

# Create your views here.

@csrf_exempt
def Login(request):
	# checks if it is a POST request
	if (request.method == 'POST'):
		un = request.POST['username']
		pw = request.POST['password']
		# user is authenticated
		user = authenticate(request, username=un, password=pw)
	else:
		# added a bad response request for incorrect requests
		http_bad_response = HttpResponseBadRequest()
		http_bad_response['Content-Type'] = 'text/plain'
		http_bad_response.status_code = 400
		http_bad_response.reason_phrase = 'Bad Request'
		http_bad_response.content = 'Only POST requests are allowed for this resource.'
		return http_bad_response		
	if user is not None:
		# checks if the user is active
		if user.is_active:
			try: 
				# logs in the user
				login(request, user)
			except Exception as e:
				# formulates a response for error when logging in
				http_bad_response = HttpResponseBadRequest()
				http_bad_response['Content-Type'] = 'text/plain'
				http_bad_response.status_code = 503
				http_bad_response.reason_phrase = 'Service Unavailable'
				http_bad_response.content = str(e)
				return http_bad_response				

			# checks if the user is authenticated
			if (user.is_authenticated):
				# formulates a response for successfully logging in
				http_response = HttpResponse()
				http_response['Content-Type'] = 'text/plain'
				http_response.status_code = 200
				http_response.reason_phrase = 'OK'
				http_response.content = 'Welcome ' + un + "!"
				return http_response
			else:
				# formulates a response for a disabled account
				http_bad_response = HttpResponseBadRequest()
				http_bad_response['Content-Type'] = 'text/plain'
				http_bad_response.status_code = 405
				http_bad_response.reason_phrase = 'Method Not Allowed'
				http_bad_response.content = 'Disabled account'
				return http_bad_response
	else:
		# returns an 'invalid login' error message.
		http_bad_response = HttpResponseBadRequest()
		http_bad_response['Content-Type'] = 'text/plain'
		http_bad_response.status_code = 401
		http_bad_response.reason_phrase = 'Unauthorized'
		http_bad_response.content = 'Invalid login.'
		return http_bad_response

@csrf_exempt
def LogOut(request):
	# checks if the user is logged in 
	if (request.user.is_authenticated):
		# checks if the request method is POST
		if (request.method == 'POST'):
			# logs out the user
			try:
				logout(request)
			except Exception as e:
				# formulates a response for error when logging out
				http_bad_response = HttpResponseBadRequest()
				http_bad_response['Content-Type'] = 'text/plain'
				http_bad_response.status_code = 503
				http_bad_response.reason_phrase = 'Service Unavailable'
				http_bad_response.content = str(e)
				return http_bad_response					

			# formulates, a response for successfully logging out
			http_response = HttpResponse()
			http_response['Content-Type'] = 'text/plain'
			http_response.status_code = 200
			http_response.reason_phrase = 'OK'
			http_response.content = 'Goodbye!'
			return http_response
		else:
			# added a bad response request for incorrect requests
			http_bad_response = HttpResponseBadRequest()
			http_bad_response['Content-Type'] = 'text/plain'
			http_bad_response.status_code = 400
			http_bad_response.reason_phrase = 'Bad Request'
			http_bad_response.content = 'Only POST requests are allowed for this resource.'
			return http_bad_response	
	else:
		# added a bad response request for user not logged in
		http_bad_response = HttpResponseBadRequest()
		http_bad_response['Content-Type'] = 'text/plain'
		http_bad_response.status_code = 503
		http_bad_response.reason_phrase = 'Service Unavailable'
		http_bad_response.content = 'User must be logged in to logout.'
		return http_bad_response

@csrf_exempt
def PostStory(request):
	# checks if the user is logged in 
	if (request.user.is_authenticated):
		# checks if the request method is POST
		if(request.method == 'POST'):
			headline = request.POST['headline']
			category = request.POST['category']
			region = request.POST['region']
			details = request.POST['details']

			# creates values for author and date to be added in stories table
			auth = request.user.get_username()
			dt = date.today()
			formatted_date = dt.strftime("%d/%m/%Y")

			try:
				# creates and saves the story
				story1 = Story(headline=headline, category=category, region=region, details=details, author=auth, date=formatted_date)
				story1.save()
			except Exception as e:
				# formulates a response for error when posting a story
				http_bad_response = HttpResponseBadRequest()
				http_bad_response['Content-Type'] = 'text/plain'
				http_bad_response.status_code = 503
				http_bad_response.reason_phrase = 'Service Unavailable'
				http_bad_response.content = str(e)
				return http_bad_response
			
			# formulates a response for successfully adding a story
			http_response = HttpResponse() 
			http_response.status_code = 201
			http_response.reason_phrase = 'CREATED'
			return http_response
		else:
			# added a bad response request for incorrect requests
			http_bad_response = HttpResponseBadRequest()
			http_bad_response['Content-Type'] = 'text/plain'
			http_bad_response.status_code = 400
			http_bad_response.reason_phrase = 'Bad Request'
			http_bad_response.content = 'Only POST requests are allowed for this resource.'
			return http_bad_response	
	else:
		# added a bad response request for user not logged in 
		http_bad_response = HttpResponseBadRequest()
		http_bad_response['Content-Type'] = 'text/plain'
		http_bad_response.status_code = 503
		http_bad_response.reason_phrase = 'Service Unavailable'
		http_bad_response.content = 'User must be logged in to post stories.'
		return http_bad_response				
		
@csrf_exempt
def GetStory(request):
	# checks if the request method is GET
	if(request.method == 'GET'):
		# retrieves all the data items from the get request
		story_cat = request.GET['story_cat']
		story_region = request.GET['story_region']
		story_date = request.GET['story_date']

		# initializes a list for all the stories data to be added
		the_list = []

		# retrieves all the stories
		story_list = list(Story.objects.all().values())
		
		# loops through each story and checks whether the filter for each argument matches the database's value
		# if there is a inputted filter and there is no match, then the loop continues to the next story
		for story in story_list:
			# checking the filter for the story's category
			if story_cat != "*" and story_cat == story['story_category']:
				filtered_cat = story_cat
			elif story_cat == "*":
				filtered_cat = story['story_category']
			elif story_cat != "*" and id != story['story_category']:
				continue
			
			# checking the filter for the story's region
			if story_region != "*" and story_region == story['story_region']:
				filtered_region = story_region
			elif story_region == "*":
				filtered_region = story['story_region']
			elif story_region != "*" and id != story['story_region']:
				continue			

			# checking the filter for the story's date
			if story_date != "*":
				# formats the inputted data and database date from the story object to compare the dates
				input_date = datetime.strptime(story_date, "%d/%m/%Y")
				input_date = input_date.date()

				database_date = datetime.strptime(story['date'], "%d/%m/%Y")
				database_date = database_date.date()

				# compares if the database date is on or after the inputted date (filtered date)
				if database_date >= input_date:
					filtered_date = story['date']
				else: 
					continue
			elif story_date == "*":
				filtered_date = story['date']
			elif story_date != "*" and id != story['date']:
				continue	
			
			# if the list is at a length of 20, then it breaks out of the loop and stops searching 
			if len(the_list) == 20:
				break
			else:
				# creates the item dictionary with all the data and appends it to the main list
				item = {'key': story['id'], 'headline': story['headline'], 'category': filtered_cat, 'region': filtered_region, 'author': story['author'], 'date':filtered_date, 'details': story['story_details']}				
				the_list.append(item)
		
		# needs to check if no stories were found
		if not the_list:
			# added a bad response request if no stories were found 
			http_bad_response = HttpResponseBadRequest()
			http_bad_response['Content-Type'] = 'text/plain'
			http_bad_response.status_code = 404
			http_bad_response.content = 'No stories were found.'
			return http_bad_response		

		# creates the final json payload
		payload = {'story_list': the_list}
		# creates and returns a successful response for retrieving all the stories
		http_response = HttpResponse(json.dumps(payload))
		http_response['Content-Type'] = "application/json"
		http_response.status_code = 200
		http_response.reason_phrase = 'OK'
		return http_response
	else:
		# added a bad response request for incorrect requests
		http_bad_response = HttpResponseBadRequest()
		http_bad_response['Content-Type'] = 'text/plain'
		http_bad_response.status_code = 400
		http_bad_response.reason_phrase = 'Bad Request'
		http_bad_response.content = 'Only GET requests are allowed for this resource.'
		return http_bad_response	

@csrf_exempt
def DeleteStory(request, key):
	# checks if the user is logged in 
	if (request.user.is_authenticated):
		# checks if the request method is DELETE
		if(request.method == 'DELETE'):

			try:
				# tries to retrieve the deleted story
				deleted_story = Story.objects.get(id=key)
				deleted_story.delete()
			except Exception as e:
				# creates a bad response for not successfully deleting the specified key
				http_bad_response = HttpResponseBadRequest()
				http_bad_response['Content-Type'] = 'text/plain'
				http_bad_response.status_code = 503
				http_bad_response.reason_phrase = 'Service Unavailable'
				http_bad_response.content = str(e)
				return http_bad_response				

			# creates a response for successfully deleting the specified key
			http_response = HttpResponse()
			http_response.status_code = 200
			http_response.reason_phrase = 'OK'
			return http_response
		else:
			# added a bad response request for incorrect requests
			http_bad_response = HttpResponseBadRequest()
			http_bad_response['Content-Type'] = 'text/plain'
			http_bad_response.status_code = 400
			http_bad_response.reason_phrase = 'Bad Request'
			http_bad_response.content = 'Only DELETE requests are allowed for this resource.'
			return http_bad_response
	else:
		# added a bad response request for user not logged in 
		http_bad_response = HttpResponseBadRequest()
		http_bad_response['Content-Type'] = 'text/plain'
		http_bad_response.status_code = 503
		http_bad_response.reason_phrase = 'Service Unavailable'
		http_bad_response.content = 'User must be logged in to post stories.'
		return http_bad_response

@csrf_exempt
def List(request):
	# checks if it is a GET request
	if(request.method == 'GET'):
		try:
			# retrieves the list of agenices
			agency_list = Story.objects.all().values('agency_name', 'url', 'agency_code')
			# collects the agency list items and creates a list with appropriate json names
			the_list = []
			for agency in agency_list:
				item = {'agency_name': agency['agency_name'], 'url': agency['url'], 'agency_code': agency['agency_code']}
				the_list.append(item)
				agency_count = agency_count + 1
		except Exception as e:
			http_bad_response = HttpResponseBadRequest()
			http_bad_response['Content-Type'] = 'text/plain'
			http_bad_response.status_code = 503
			http_bad_response.reason_phrase = 'Service Unavailable'
			http_bad_response.content = str(e)
			return http_bad_response
		
		# creates the final json payload
		payload = {'agency_list': agency_list}
		# creates and returns a normal response
		http_response = HttpResponse()
		http_response['Content-Type'] = 'application/json'
		http_response.status_code = 200
		http_response.reason_phrase = 'OK'
		http_response.content = json.dumps(payload)
		return http_response
	else:
		# creates a bad response if the request is not GET
		http_bad_response = HttpResponseBadRequest()
		http_bad_response['Content-Type'] = 'text/plain'
		http_bad_response.status_code = 400
		http_bad_response.reason_phrase = 'Bad Request'
		http_bad_response.content = 'Only GET requests are allowed for this resource.'
		return http_bad_response	