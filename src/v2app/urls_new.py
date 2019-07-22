from django.urls import path, re_path
from django.conf.urls import url
from .views_new import *

urlpatterns = [
  url(r'^$', ping),
  path('actions', actions),
  path('action/<int:id>', action),
  path('action-properties', action_properties),
  path('action-property/<int:id>', action_property),
  path('billing-statements', billing_statements),
  path('billing-statement/<int:id>', billing_statement),
  path('communities', communities),
  path('community/<int:cid>', community),
  path('community/<int:cid>/actions', community_actions),
  path('community/<int:cid>/members', community_members),
  path('community/<int:cid>/impact', community_impact),
  path('community/<int:cid>/pages', community_pages),
  path('community/<int:cid>/events', community_events),
  path('community/<int:cid>/households', community_households),
  path('community/<int:cid>/goals', community_goals),
  path('community/<int:cid>/teams', community_teams),
  path('community/<int:cid>/data', community_data),
  path('community/<int:cid>/testimonials', community_testimonials),
  path('community/<int:cid>/stories', community_testimonials),
  path('community/<str:subdomain>', community),
  path('community/<str:subdomain', community_actions),
  path('community/<str:subdomain', community_members),
  path('community/<str:subdomain', community_impact),
  path('community/<str:subdomain', community_pages),
  path('community/<str:subdomain>/events', community_events),
  path('community/<str:subdomain>/households', community_households),
  path('community/<str:subdomain>/goals', community_goals),
  path('community/<int:cid>/teams', community_teams),
  path('community/<int:cid>/data', community_data),
  path('community/<int:cid>/testimonials', community_testimonials),
  path('community/<int:cid>/stories', community_testimonials),
  path('community-admins', community_admins),
  path('community-admins/<int:id>', community_admins),
  path('data', data),
  path('data/<int:id>', data_by_id),
  path('email-categories', email_categories),
  path('email-category/<int:id>', email_category),
  path('events', events),
  path('event/<int:id>', event),
  path('event-attendees', event_attendees),
  path('event-attendee/<int:id>', event_attendee),
  path('goals', goals),
  path('goal/<int:id>', goal),
  path('graphs', graphs),
  path('graph/<int:id>', graph),
  path('households', households),
  path('household/<int:id>', household),
  path('locations', locations),
  path('location/<int:id>', location),
  path('media', media),
  path('media/<int:id>', media_by_id),
  path('media/<slug:slug>', media_with_slug),
  path('menus', menus),
  path('menu/<int:id>', menu),
  path('pages', pages),
  path('page/<int:id>', page),
  path('page-sections', page_sections),
  path('page-section/<int:id>', page_section),
  path('permissions', permissions),
  path('permission/<int:id>', permission),
  path('policies', policies),
  path('policy/<int:id>', policy),
  path('roles', roles),
  path('role/<int:id>', role),
  path('services', services),
  path('service/<int:id>', service),
  path('sliders', sliders),
  path('slider/<int:id>', slider),
  path('slider-images', slider_images),
  path('slider-image/<int:id>', slider_image),
  path('statistics', data),
  path('statistic/<int:id>', data_by_id),
  path('stories', testimonials),
  path('story/<int:id>', testimonial),
  path('subscribers', subscribers),
  path('subscriber/<int:id>', subscriber),
  path('subscriber-email-preferences', subscriber_email_preferences),
  path('subscriber-email-preference/<int:id>', subscriber_email_preference),
  path('tags', tags),
  path('tag/<int:id>', tag),
  path('tag-collections', tag_collections),
  path('tag-collection/<int:id>', tag_collection),
  path('teams', teams),
  path('team/<int:id>', team),
  path('testimonials', testimonials),
  path('testimonial/<int:id>', testimonial),
  path('users', users),
  path('user/<str:id>', user),
  path('user/<str:id>/households', user_households),
  path('user/<str:id>/household/<int:hid>/actions', user_household_actions),
  path('user/<str:id>/actions', user_actions),
  path('user/<str:id>/action/<int:aid>', user_action),
  path('user/<str:id>/teams', user_teams),
  path('user/<str:id>/testimonials', user_testimonials),
  path('user-groups', user_groups),
  path('user-group/<int:id>', user_group),
  path('uuid/new', new_uuid),
  path('vendors', vendors),
  path('vendor/<int:id>', vendor),
]