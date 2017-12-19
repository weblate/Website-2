from allauth.socialaccount.models import SocialAccount
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.core.mail import mail_admins
from django.db.models import Max
from django.http import HttpResponseRedirect, QueryDict, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.translation import gettext_lazy as _
from pycent import percentage
from pytz import utc
from rest_framework import authentication, permissions, status
from rest_framework.decorators import detail_route
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from trainer.forms import QuickUpdateForm
from trainer.models import Trainer, Faction, Update
from trainer.serializers import UserSerializer, BriefTrainerSerializer, DetailedTrainerSerializer, FactionSerializer, BriefUpdateSerializer, DetailedUpdateSerializer, LeaderboardSerializer, SocialAllAuthSerializer
from trainer.shortcuts import nullbool, cleanleaderboardqueryset, level_parser

# RESTful API Views

class UserViewSet(ModelViewSet):
	serializer_class = UserSerializer
	queryset = User.objects.all()
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class TrainerListView(APIView):
	"""
	GET - Accepts paramaters for Team (t) and Username (q)
	POST - Register a Trainer, needs PK for User
	"""
	
	authentication_classes = (authentication.TokenAuthentication,)
	
	def get(self, request):
		queryset = Trainer.objects.exclude(active=False)
		if request.GET.get('q') or request.GET.get('t'):
			if request.GET.get('q'):
				queryset = queryset.filter(username__icontains=request.GET.get('q'))
			if request.GET.get('t'):
				queryset = queryset.filter(faction=request.GET.get('t'))
		
		if request.GET.get('detail') == '1':
			serializer = DetailedTrainerSerializer(queryset, many=True)
			return Response(serializer.data)
		else:
			serializer = BriefTrainerSerializer(queryset, many=True)
			return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
	
	def post(self, request):
		serializer = DetailedTrainerSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	

class TrainerDetailView(APIView):
	"""
	GET - Trainer detail
	PATCH - Update a trainer
	DELETE - Archives a trainer (hidden from APIs until trainer tries to join again)
	"""
	
	authentication_classes = (authentication.TokenAuthentication,)
	
	def get_object(self, pk):
		return get_object_or_404(Trainer, pk=pk)
	
	def get(self, request, pk):
		print(status.HTTP_423_LOCKED)
		trainer = self.get_object(pk)
		if trainer.active is True:
			if trainer.statistics is True or (trainer.statistics is False and request.GET.get('statistics') == 'force'):
				serializer = DetailedTrainerSerializer(trainer)
				return Response(serializer.data)
			elif trainer.statistics is False:
				return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
		elif trainer.active is False:
			response = {
				'code': 1,
				'reason': 'Profile deactivated',
				'profile': {
					'id': trainer.pk,
					'faction': trainer.faction.id,
				},
			}
			return Response(response, status=status.HTTP_423_LOCKED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	def patch(self, request, pk):
		trainer = self.get_object(pk)
		serializer = DetailedTrainerSerializer(trainer, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	def delete(self, request, pk):
		trainer = self.get_object(pk)
		if trainer.active:
			trainer.active = False
			trainer.save()
			response = {
				'code': 1,
				'reason': 'Profile deactivated',
				'profile': {
					'id': trainer.pk,
					'faction': trainer.faction.id,
				},
			}
			return Response(response, status=status.HTTP_204_NO_CONTENT)
		return Response(status=status.HTTP_400_BAD_REQUEST)
	

class UpdateListView(APIView):
	"""
	GET - Takes Trainer ID as part of URL, optional param: detail, shows all detail, otherwise, returns a list of objects with fields 'time_updated' (datetime), 'xp'(int) and 'fields_updated' (list)
	POST/PATCH - Create a update
	"""
	
	authentication_classes = (authentication.TokenAuthentication,)
	
	def get(self, request, pk):
		updates = Update.objects.filter(trainer=pk)
		serializer = BriefUpdateSerializer(updates, many=True)
		return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
	
	def post(self, request, pk):
		serializer = DetailedUpdateSerializer(data=request.data)
		if serializer.is_valid():
			serializer.clean()
			serializer.save(trainer=get_object_or_404(Trainer, pk=pk))
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	def patch(self, request, pk):
		return self.post(self, request, pk)
	

class UpdateDetailViewLatest(APIView):
	"""
	GET - Gets detailed view of the latest update
	PATCH - Allows editting of update within first half hour of creation, after that time, all updates are denied. Trainer, UUID and PK are locked.
	"""
	
	authentication_classes = (authentication.TokenAuthentication,)
	
	def get(self, request, pk):
		update = Update.objects.filter(trainer=pk).latest('update_time')
		serializer = DetailedUpdateSerializer(update)
		return Response(serializer.data)
	
	def patch(self, request, pk):
		update = Update.objects.filter(trainer=pk).latest('update_time')
		if update.meta_time_created > datetime.now(utc)-timedelta(minutes=32):
			serializer = DetailedUpdateSerializer(update, data=request.data)
			if serializer.is_valid():
				serializer.clean()
				serializer.save(trainer=update.trainer,uuid=update.uuid,pk=update.pk)
				return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	

class UpdateDetailView(APIView):
	"""
	GET - Gets detailed view
	PATCH - Allows editting of update within first half hour of creation, after that time, all updates are denied. Trainer, UUID and PK are locked.
	DELETE - Delete an update, works within first 48 hours of creation, otherwise, an email request for deletion is sent to admin
	"""
	
	authentication_classes = (authentication.TokenAuthentication,)
	
	def get(self, request, uuid, pk):
		update = get_object_or_404(Update, trainer=pk, uuid=uuid)
		serializer = DetailedUpdateSerializer(update)
		if update.trainer.id != int(pk):
			return Response(serializer.errors, status=400)
		return Response(serializer.data)
	
	def patch(self, request, uuid, pk):
		update = get_object_or_404(Update, trainer=pk, uuid=uuid)
		if update.meta_time_created > datetime.now(utc)-timedelta(minutes=32):
			serializer = DetailedUpdateSerializer(update, data=request.data)
			if serializer.is_valid():
				serializer.clean()
				serializer.save(trainer=update.trainer,uuid=update.uuid,pk=update.pk)
				return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	def delete(self, request, uuid, pk):
		update = get_object_or_404(Update, trainer=pk, uuid=uuid)
		if update.meta_time_created > datetime.now(utc)-timedelta(days=2):
			update.delete()
			return Response(status=status.HTTP_204_NO_CONTENT)
		else:
			SUBJECT = 'Late Update Deletion Request'
			MESSAGE = 'There has been a request to delete {update} by {requester} at {ip}'.format(update=request.build_absolute_uri(), requester=request.user, ip=request.get_host())
			mail_admins(SUBJECT, MESSAGE)
			return Response({'request_made': True, 'subject': SUBJECT, 'message': MESSAGE}, status=status.HTTP_202_ACCEPTED)
		return Response(status=status.HTTP_400_BAD_REQUEST)
	

class LeaderboardAPIView(APIView):
	
	def get(self, request):
		leaderboard = Trainer.objects.exclude(statistics=False, currently_cheats=True).annotate(Max('update__xp'), Max('update__update_time'))
		leaderboard = cleanleaderboardqueryset(leaderboard, key=lambda x: x.update__xp__max, reverse=True)
		serializer = LeaderboardSerializer(enumerate(leaderboard, 1), many=True)
		return Response(serializer.data)
	

class SocialLookupView(APIView):
	"""
	GET args:
		provider (requiered) - platform, options are 'facebook', 'twitter', 'discord', 'google', 'patreon'
		
		One of the below, they're checked in this order so if you provide more than one, only the first would be processed.
		uid - Social ID, supports a comma seperated list. Could be useful for passing a list of users in a server to retrieve a list of UserIDs, which could then be passed to api/v1/leaderboard/
		user - TrainerDex User ID, supports a comma seperated list
		trainer - TrainerDex Trainer ID
	POST: Register a SocialAccount
	"""
	
	def get(self, request):
		query = SocialAccount.objects.filter(provider=request.GET.get('provider'))
		if request.GET.get('uid'):
			query = query.filter(uid__in=request.GET.get('uid').split(','))
		elif request.GET.get('user'):
			query = query.filter(user__in=request.GET.get('user').split(','))
		elif request.GET.get('trainer'):
			query = query.filter(user=get_object_or_404(Trainer, pk=request.GET.get('trainer')).owner)
		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)
		serializer = SocialAllAuthSerializer(query, many=True)
		return Response(serializer.data)
		
	def post(self, request):
		serializer = SocialAllAuthSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AutoRegisterView(APIView):
	"""
	POST: Create an account.
	This API requests a dict of dicts or ints. If ints, it will use an existing object, if dict it'll attempt to create a new object.
	
	{
		"user":{                       # Required to exist. If not providing int value of existing user, provide an empty dict.
			"first_name": "string",    # Optional
			"last_name": "string",     # Optional
			"email": "string@mail.com",# Optional. Recommended.
		},
		"trainer":{
			"username":"TrainerName",  # Required. This MUST be an exact 1:1 copy of the Trainer name. Not case sensitive.
			"start_date":"iso-8601",   # Optional. If provided, must be provided in iso-8601 format as a string.
			"faction": 0,              # Required. Integer. 0 Teamless, 1 Blue, 2 Red, 3 Yellow
			"has_cheated": false,      # Optional. Defaults to false. This is a hidden stat that helps us with reports.
			"last_cheated":"iso-8601", # Optional. If supplied, has_cheated will reset to true. If has_cheated was true and this wasn't supplied, this will default to today.
			"currently_cheats": false, # Optional. If true, has_cheated will set to true and last_cheated will set to today.
			"statistics": true,        # Optional. Defaults to true. Option to opt out of international leaderboard and public profile will be empty.
			"daily_goal": 0,           # Optional. Defaults to null.
			"total_goal": 0,           # Optional. Defaults to null.
		},
		"update":{
			"xp": 2000000,             # Required. Please ensure accuracy when supplying this value as there is only a 32 minute window to adjust if it was entered too high. Additionally, there is a 48 hour window to delete if you miss the 32 minute window
			"walk_dist": "123.4",      # Optional. Supply as string for precision of the decimal.
			medal_name: integer,       # Any medal listed below.
		},
		"social":{                     # Ignored. Not implemented yet.
			"provider": "string",      # Required. Choices are 'facebook', 'twitter', 'discord', 'google', 'patreon'.
			"uid": "12345",            # Required. String representation of a users ID from social provider.
			"extra_data":{jsondict},   # Optional. Read [here](https://github.com/pennersr/django-allauth/issues/140#issuecomment-10607940) about how this is implemented.
		}
	}
	"""
	
	def post(self, request):
		
		if not ((isinstance(request.data['user'], dict) or isinstance(request.data['user'], int)) and isinstance(request.data['trainer'], dict) and isinstance(request.data['update'], dict)):
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		user = request.data['user']
		trainer = request.data['trainer']
		update = request.data['update']
		
		if isinstance(user, dict):
			user['username'] = '_'+trainer['username']
			user_serializer = UserSerializer(data=user)
			trainer['owner'] = 1
			try:
				user.pop('password')
			except KeyError:
				pass
		elif isinstance(user, int):
			user = get_object_or_404(User, pk=user)
			user_serializer = UserSerializer(user)
			trainer['owner'] = user.pk
		
		update['trainer'] = 0
		
		trainer_serializer = DetailedTrainerSerializer(data=trainer)
		update_serializer = DetailedUpdateSerializer(data=update)
		
		
		
		user_valid = user_serializer.is_valid() if isinstance(user, dict) else True
		trainer_valid = trainer_serializer.is_valid()
		update_valid = update_serializer.is_valid()
		if user_valid and trainer_valid and update_valid:
			if isinstance(user, dict):
				user_serializer.save()
				user_saved = get_object_or_404(User, id=user_serializer.data['id'])
				#user_saved = User.objects.create_user(**user_serializer.validated_data)
			else:
				user_saved = user
			
			trainer_serializer.save(owner=user_saved)
			trainer_saved = get_object_or_404(Trainer, id=trainer_serializer.data['id'])
			update_serializer.save(trainer=trainer_saved)
			update_saved = get_object_or_404(Update, trainer=trainer_serializer.data['id'])
			return Response([user_serializer.data, trainer_serializer.data, update_serializer.data], status=status.HTTP_201_CREATED)
		return Response(status=status.HTTP_400_BAD_REQUEST)
	
# Web-based views

BADGES = [
	{'name':'walk_dist', 'bronze':10, 'silver':100, 'gold':1000, 'i18n_name':_('Jogger')},
	{'name':'gen_1_dex', 'bronze':5, 'silver':50, 'gold':100, 'i18n_name':_('Kanto')},
	{'name':'pkmn_caught', 'bronze':30, 'silver':500, 'gold':2000, 'i18n_name':_('Collector')},
	{'name':'pkmn_evolved', 'bronze':3, 'silver':20, 'gold':200, 'i18n_name':_('Scientist')},
	{'name':'eggs_hatched', 'bronze':10, 'silver':100, 'gold':500, 'i18n_name':_('Breeder')},
	{'name':'pkstops_spun', 'bronze':100, 'silver':1000, 'gold':2000, 'i18n_name':_('Backpacker')},
	{'name':'big_magikarp', 'bronze':3, 'silver':50, 'gold':300, 'i18n_name':_('Fisherman')},
	{'name':'battles_won', 'bronze':10, 'silver':100, 'gold':1000, 'i18n_name':_('Battle Girl')},
	{'name':'legacy_gym_trained', 'bronze':10, 'silver':100, 'gold':1000, 'i18n_name':_('Ace Trainer')},
	{'name':'tiny_rattata', 'bronze':3, 'silver':50, 'gold':300, 'i18n_name':_('Younster')},
	{'name':'pikachu_caught', 'bronze':3, 'silver':50, 'gold':300, 'i18n_name':_('Pikachu Fan')},
	{'name':'gen_2_dex', 'bronze':5, 'silver':30, 'gold':70, 'i18n_name':_('Johto')},
	{'name':'unown_alphabet', 'bronze':3, 'silver':10, 'gold':26, 'i18n_name':_('Unown')},
	{'name':'berry_fed', 'bronze':10, 'silver':100, 'gold':1000, 'i18n_name':_('Berry Master')},
	{'name':'gym_defended', 'bronze':10, 'silver':100, 'gold':1000, 'i18n_name':_('Gym Leader')},
	{'name':'raids_completed', 'bronze':10, 'silver':100, 'gold':1000, 'i18n_name':_('Champion')},
	{'name':'leg_raids_completed', 'bronze':10, 'silver':100, 'gold':1000, 'i18n_name':_('Battle Legend')},
	{'name':'gen_3_dex', 'bronze':5, 'silver':40, 'gold':90, 'i18n_name':_('Hoenn')},
]

TYPE_BADGES = [
	{'name':'pkmn_normal', 'bronze':10, 'silver':50, 'gold':200, 'i18n_name':_('Normal')},
	{'name':'pkmn_flying', 'bronze':10, 'silver':50, 'gold':200, 'i18n_name':_('Flying')},
	{'name':'pkmn_poison', 'bronze':10, 'silver':50, 'gold':200, 'i18n_name':_('Poison')},
	{'name':'pkmn_ground', 'bronze':10, 'silver':50, 'gold':200, 'i18n_name':_('Ground')},
	{'name':'pkmn_rock', 'bronze':10, 'silver':50, 'gold':200, 'i18n_name':_('Rock')},
	{'name':'pkmn_bug', 'bronze':10, 'silver':50, 'gold':200, 'i18n_name':_('Bug')},
	{'name':'pkmn_steel', 'bronze':10, 'silver':50, 'gold':200, 'i18n_name':_('Steel')},
	{'name':'pkmn_fire', 'bronze':10, 'silver':50, 'gold':200, 'i18n_name':_('Fire')},
	{'name':'pkmn_water', 'bronze':10, 'silver':50, 'gold':200, 'i18n_name':_('Water')},
	{'name':'pkmn_electric', 'bronze':10, 'silver':50, 'gold':200, 'i18n_name':_('Electric')},
	{'name':'pkmn_psychic', 'bronze':10, 'silver':50, 'gold':200, 'i18n_name':_('Psychic')},
	{'name':'pkmn_dark', 'bronze':10, 'silver':50, 'gold':200, 'i18n_name':_('Dark')},
	{'name':'pkmn_fairy', 'bronze':10, 'silver':50, 'gold':200, 'i18n_name':_('Fairy')},
	{'name':'pkmn_fighting', 'bronze':10, 'silver':50, 'gold':200, 'i18n_name':_('Fighting')},
	{'name':'pkmn_ghost', 'bronze':10, 'silver':50, 'gold':200, 'i18n_name':_('Ghost')},
	{'name':'pkmn_ice', 'bronze':10, 'silver':50, 'gold':200, 'i18n_name':_('Ice')},
	{'name':'pkmn_dragon', 'bronze':10, 'silver':50, 'gold':200, 'i18n_name':_('Dragon')},
]

STATS = [
	'dex_caught',
	'dex_seen',
	'gym_badges',
	'xp'
]

def TrainerProfileView(request, username=None):
	if username:
		trainer = get_object_or_404(Trainer, username__iexact=username)
	elif request.GET.get('username'):
		trainer = get_object_or_404(Trainer, username__iexact=request.GET.get('username'))
	elif request.GET.get('id'):
		trainer = get_object_or_404(Trainer, pk=request.GET.get('id'))
	elif not request.user.is_authenticated():
		return redirect('home')
	else:
		trainer = get_object_or_404(Trainer, owner=request.user, prefered=True)
	context = {
		'trainer' : trainer,
		'updates' : Update.objects.filter(trainer=trainer),
	}
	badges = []
	type_badges = []
	for badge in BADGES:
		badge_dict = {
			'name':badge['name'],
			'readable_name':badge['i18n_name'],
		}
		try:
			badge_dict['value'] = getattr(Update.objects.filter(trainer=trainer).exclude(**{badge['name'] : None}).order_by('-'+badge['name']).first(), badge['name'])
			if badge_dict['value'] < badge['bronze']:
				badge_dict['percent'] = int(percentage(badge_dict['value'],badge['bronze'],0))
			elif badge_dict['value'] < badge['silver']:
				badge_dict['percent'] = int(percentage(badge_dict['value'],badge['silver'],0))
			elif badge_dict['value'] < badge['gold']:
				badge_dict['percent'] = int(percentage(badge_dict['value'],badge['gold'],0))
			else:
				badge_dict['percent'] = 100
			badge_dict['time'] = getattr(Update.objects.filter(trainer=trainer).exclude(**{badge['name'] : None}).order_by('-'+badge['name']).first(), 'update_time')
		except AttributeError:
			continue
		badges.append(badge_dict)
	for badge in TYPE_BADGES:
		badge_dict = {
			'name':badge['name'],
			'readable_name':badge['i18n_name'],
		}
		try:
			badge_dict['value'] = getattr(Update.objects.filter(trainer=trainer).exclude(**{badge['name'] : None}).order_by('-'+badge['name']).first(), badge['name'])
			if badge_dict['value'] < badge['bronze']:
				badge_dict['percent'] = int(percentage(badge_dict['value'],badge['bronze'],0))
			elif badge_dict['value'] < badge['silver']:
				badge_dict['percent'] = int(percentage(badge_dict['value'],badge['silver'],0))
			elif badge_dict['value'] < badge['gold']:
				badge_dict['percent'] = int(percentage(badge_dict['value'],badge['gold'],0))
			else:
				badge_dict['percent'] = 100
			badge_dict['time'] = getattr(Update.objects.filter(trainer=trainer).exclude(**{badge['name'] : None}).order_by('-'+badge['name']).first(), 'update_time')
		except AttributeError:
			continue
		type_badges.append(badge_dict)
	for badge in STATS:
		try:
			context[badge] = getattr(Update.objects.filter(trainer=trainer).exclude(**{badge : None}).order_by('-'+badge).first(), badge)
			context[badge+'-time'] = getattr(Update.objects.filter(trainer=trainer).exclude(**{badge : None}).order_by('-'+badge).first(), 'update_time')
		except AttributeError:
			continue
	context['level'] = level_parser(xp=context['xp']),
	context['badges'] = badges
	context['type_badges'] = type_badges
	return render(request, 'profile.html', context)

def QuickUpdateDialogView(request):
	form = QuickUpdateForm(request.POST or None)
	if form.is_valid() and Trainer.objects.get(pk=request.POST['trainer']) in Trainer.objects.filter(owner=request.user):
		form.save()
		return HttpResponseRedirect(reverse('api_v1:trainer_profiles:update_success'))
	form.fields['trainer'].queryset = Trainer.objects.filter(owner=request.user)
	if request.method == 'GET':
		form.fields['trainer'].initial = get_object_or_404(Trainer, owner=request.user, prefered=True)
	return render(request, 'update_dialog.html', {'form': form, 'trainers': Trainer.objects.filter(owner=request.user)})

def QuickUpdateSuccessView(request):
	return render(request, 'update_success.html')

def LeaderboardView(request):
	
	#Defining Parameters
	showValor = {'param':'Valor', 'value':nullbool(request.GET.get('valor'), default=True)}
	showMystic = {'param':'Mystic', 'value':nullbool(request.GET.get('mystic'), default=True)}
	showInstinct = {'param':'Instinct', 'value':nullbool(request.GET.get('instinct'), default=True)}
	showSpoofers = {'param':'currently_cheats', 'value':nullbool(request.GET.get('spoofers'), default=False)}
	
	_trainers_query = Trainer.objects.exclude(statistics=False)
	for param in (showValor, showMystic, showInstinct):
		if param['value'] is False:
			_trainers_query = _trainers_query.exclude(faction__name=param['param'])
	_trainers_non_legit = _trainers_query.exclude(currently_cheats = False).annotate(Max('update__xp'), Max('update__update_time'))
	_trainers_non_legit = cleanleaderboardqueryset(_trainers_non_legit, key=lambda x: x.update__xp__max, reverse=True)
	_trainers_legit = _trainers_query.exclude(currently_cheats = True).annotate(Max('update__xp'), Max('update__update_time'))
	_trainers_legit = cleanleaderboardqueryset(_trainers_legit, key=lambda x: x.update__xp__max, reverse=True)
	
	_trainers = []
	for trainer in _trainers_legit:
		_trainers.append({
			'position' : _trainers_legit.index(trainer)+1,
			'trainer' : trainer,
			'xp' : trainer.update__xp__max,
			'time' : trainer.update__update_time__max,
			'level' : level_parser(xp=trainer.update__xp__max),
		})
	if showSpoofers['value']:
		for trainer in _trainers_non_legit:
			_trainers.append({
				'position' : None,
				'trainer' : trainer,
				'xp' : trainer.update__xp__max,
				'time' : trainer.update__update_time__max,
				'level' : level_parser(xp=trainer.update__xp__max),
				})
	_trainers.sort(key = lambda x: x['xp'], reverse=True)
	
	return render(request, 'leaderboard.html', {'leaderboard' : _trainers, 'valor' : showValor, 'mystic' : showMystic, 'instinct' : showInstinct, 'spoofers' : showSpoofers})
