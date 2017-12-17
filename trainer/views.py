from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import Max
from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.translation import gettext_lazy as _
from ekpogo.utils import nullbool, cleanleaderboardqueryset
from pycent import percentage
from rest_framework import authentication, permissions, status
from rest_framework.decorators import detail_route
from rest_framework.views import APIView
from rest_framework.response import Response
from trainer.forms import QuickUpdateForm
from trainer.models import Trainer, Faction, Update, ExtendedProfile
from trainer.serializers import UserSerializer, TrainerSerializer, FactionSerializer, UpdateSerializer

# RESTful API Views

class TrainerListView(APIView):
	"""
	GET - Accepts HTTP.get paramaters for team, q and all
	POST - Create a trainer
	"""
	authentication_classes = (authentication.TokenAuthentication,)
	permission_classes = (permissions.IsAdminUser,)
	
	def get(self, request):
		_queryset = Trainer.objects
		_queryset_out = _queryset.none()
		if request.GET.get('q'):
			_queryset_query = _queryset.filter(username__icontains=request.GET.get('q'))
			_queryset_out = _queryset_out.union(_queryset_query)
		if request.GET.get('team'):
			_queryset_team = _queryset.filter(faction=request.GET.get('team'))
			_queryset_out = _queryset_out.union(_queryset_team)
		if nullbool(request.GET.get('all'), default=False) and request.GET.get('all') in (1, True, '1', 'True'):
			_queryset_all = _queryset.all()
			_queryset_out = _queryset_out.union(_queryset_all)
		
		trainers = _queryset_out.exclude(active=False)
		serializer = TrainerSerializer(trainers, many=True)
		return Response(serializer.data)
	
	def post(self, request):
		serializer = TrainerSerializer(data=request.data)
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
	
	def get_object(self, pk):
		return get_object_or_404(Trainer, pk=pk)
	
	def get(self, request, pk):
		trainer = self.get_object(pk)
		if trainer.active is True:
			serializer = TrainerSerializer(trainer)
			return Response(serializer.data)
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
		serializer = TrainerSerializer(trainer, data=request.data, partial=True)
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
		response = {
				'code': 2,
				'reason': 'Profile already deactivated',
				'profile': {
					'id': trainer.pk,
					'faction': trainer.faction.id,
				},
			}
		return Response(response, status=status.HTTP_400_BAD_REQUEST)
	

class UpdateListView(APIView):
	"""
	GET - Takes Trainer ID as part of URL, optional param: detail, shows all detail, otherwise, returns a list of objects with fields 'time_updated' (datetime), 'xp'(int) and 'fields_updated' (list)
	POST/PATCH - Create a update
	"""
	pass

class UpdateDetailView(APIView):
	"""
	GET - Gets detailed view
	PATCH - Allows editting of update within first half hour of creation, after that time, all updates are denied
	DELETE - Delete an update, works within first 48 hours of creation, otherwise, an email request for deletion is sent to admin
	"""
	pass

class TrainerOwnerRedirect(APIView):
	"""
	Always turns 303 See Other redirect to correct URI
	"""
	pass

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
		_extended_profile = get_object_or_404(ExtendedProfile, user=request.user)
		trainer = _extended_profile.prefered_profile
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
	context['badges'] = badges
	context['type_badges'] = type_badges
	return render(request, 'profile.html', context)

def QuickUpdateDialogView(request):
	
	if request.method == 'POST':
		form = QuickUpdateForm(data=request.POST)
		if form.is_valid() and Trainer.objects.get(pk=request.POST['trainer']) in Trainer.objects.filter(owner=request.user):
			form.save()
			return HttpResponseRedirect('/trainer')
	else:
		form = QuickUpdateForm()
		form.fields['trainer'].queryset = Trainer.objects.filter(owner=request.user)
		form.fields['trainer'].initial = ExtendedProfile.objects.get(pk=request.user).prefered_profile
	return render(request, 'update_dialog.html', {'form': form, 'trainers': Trainer.objects.filter(owner=request.user)})

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
		})
	if showSpoofers['value']:
		for trainer in _trainers_non_legit:
			_trainers.append({
				'position' : None,
				'trainer' : trainer,
				'xp' : trainer.update__xp__max,
				'time' : trainer.update__update_time__max,
				})
	_trainers.sort(key = lambda x: x['xp'], reverse=True)
	
	
	
	return render(request, 'leaderboard.html', {'leaderboard' : _trainers, 'valor' : showValor, 'mystic' : showMystic, 'instinct' : showInstinct, 'spoofers' : showSpoofers})
