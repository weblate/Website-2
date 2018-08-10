﻿# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from trainer.models import *

admin.site.register(Faction)

@admin.register(DiscordGuild)
class DiscordGuildAdmin(admin.ModelAdmin):
	
	search_fields = ('id',)
	
@admin.register(PrivateLeague)
class PrivateLeagueAdmin(admin.ModelAdmin):
	
	search_fields = ('uuid','short_description', 'vanity')
	
@admin.register(PrivateLeagueMembershipPersonal)
class PrivateLeagueMembershipPersonalAdmin(admin.ModelAdmin):
	
	autocomplete_fields = ['league', 'trainer']

@admin.register(PrivateLeagueMembershipDiscord)
class PrivateLeagueMembershipDiscordAdmin(admin.ModelAdmin):
	
	autocomplete_fields = ['league', 'discord']

@admin.register(TrainerReport)
class TrainerReportAdmin(admin.ModelAdmin):
	
	autocomplete_fields = ['trainer']

@admin.register(Sponsorship)
class SponsorshipAdmin(admin.ModelAdmin):
	
	autocomplete_fields = ['members']
	search_fields = ('title',)

@admin.register(Update)
class UpdateAdmin(admin.ModelAdmin):
	
	autocomplete_fields = ['trainer']
	list_display = ('trainer', 'xp', 'update_time', 'meta_crowd_sourced','meta_source', 'modified_extra_fields')
	search_fields = ('trainer__username', 'trainer__owner__username')
	ordering = ('-update_time',)
	date_hierarchy = 'update_time'

@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
	
	autocomplete_fields = ['owner','leaderboard_country','leaderboard_region']
	list_display = ('username', 'level', 'faction', 'currently_cheats', 'is_on_leaderboard', 'is_verified', 'awaiting_verification')
	list_filter = ('faction', 'last_cheated', 'statistics', 'verified',)
	search_fields = ('username', 'owner__first_name')
	ordering = ('username',)
	fieldsets = (
		(None, {
			'fields': ('owner', 'username', 'faction', 'start_date', 'daily_goal', 'total_goal','trainer_code', 'thesilphroad_username')
		}),
		(_('Reports'), {
			'fields': ('last_cheated', 'verified', 'verification')
		}),
		(_('2017 Events'), {
			'classes': ('collapse',),
			'fields': ('badge_chicago_fest_july_2017', 'badge_pikachu_outbreak_yokohama_2017', 'badge_safari_zone_europe_2017_09_16', 'badge_safari_zone_europe_2017_10_07', 'badge_safari_zone_europe_2017_10_14')
		}),
		(_('2018 Events'), {
			'classes': ('collapse',),
			'fields': ('badge_chicago_fest_july_2018','badge_apac_partner_july_2018_japan')
		}),
		(_('Website Badges'), {
			'classes': ('collapse',),
			'fields': ('event_10b','event_1k_users')
		}),
		(_('Leaderboard'), {
			'fields': ('leaderboard_country', 'leaderboard_region', 'statistics')
		}),
	)
	
	def get_readonly_fields(self, request, obj=None): 
		if obj: # editing an existing object 
			return self.readonly_fields + ('event_10b','event_1k_users') 
		return self.readonly_fields
	
	def get_queryset(self, request):
		return super(TrainerAdmin,self).get_queryset(request).prefetch_related('update_set')
	
