from database.models import Event, RecurringEventException, UserProfile, EventAttendee, Media, Community
from _main_.utils.massenergize_errors import MassEnergizeAPIError, InvalidResourceError, CustomMassenergizeError, NotAuthorizedError
from django.db.models import Q
from _main_.utils.context import Context
from sentry_sdk import capture_message
from .utils import get_user_or_die
import datetime
from datetime import timedelta
import calendar
import pytz

def _check_recurring_date(start_date_and_time, end_date_and_time, day_of_week, week_of_month):

  converter = {"first":1, "second":2, "third":3, "fourth":4}

  if start_date_and_time:
 
    # the date check below fails because the local date (in Massachusetts) is different than the UTC date
    # need to also save the location (as a Location) and get the time zone from that.
    # KLUGE: assume Massachusetts for now                    
    dt = datetime.datetime.strptime(start_date_and_time, '%Y-%m-%dT%H:%M:%SZ')  
    local_start = dt - timedelta(hours=4)
    #print(local_start)

    dt = datetime.datetime.strptime(end_date_and_time, '%Y-%m-%dT%H:%M:%SZ')  
    local_end = dt - timedelta(hours=4)

    # check if weekday matches the start_date_and_time
    if calendar.day_name[local_start.weekday()] != day_of_week:
      return True, "Starting date and time does not match the recurrence pattern for the event"

    # if necessary, check if week of month matches the start_date...
    if week_of_month:
      # let's say the date passed in represents the Nth occurence of a particular weekday in the month 
      # we find N
      # get the first instance of the same weekday in the month
      obj = calendar.Calendar()
      date_of_first_weekday = 1
      for d in obj.itermonthdates(int(local_start.year), int(local_start.month)):
        if int(d.day >= 8):
          continue
        d1 = datetime.datetime(int(d.year), int(d.month), int(d.day))
        if calendar.day_name[d1.weekday()] == day_of_week:
          date_of_first_weekday = int(d1.day)
          diff = local_start.day - date_of_first_weekday
          break
      if converter[week_of_month] - 1 != diff/7:
        return True, "Starting date and time does not match the recurrence pattern for the event"

    # TODO: check that starting date and time is earlier than ending date and time (need to edit substring thingy)

    # check that if the event does not go longer than a day (recurring events cannot go longer than 1 day)
    if local_start.date() != local_end.date():
      return True, "Recurring events must only last 1 day. Make sure your starting date and ending date are the same"  

  return False, "No problem with recurring dates"
  
class EventStore:
  def __init__(self):
    self.name = "Event Store/DB"

  def get_event_info(self, context: Context, args) -> (dict, MassEnergizeAPIError):
    try:
      event_id = args.pop("event_id")

      events_selected = Event.objects.select_related('image', 'community').prefetch_related('tags', 'invited_communities').filter(id=event_id)
      event = events_selected.first()
      if not event:
        return None, InvalidResourceError()
      return event, None
    except Exception as e:
      capture_message(str(e), level="error")
      return None, CustomMassenergizeError(e)

  def copy_event(self, context: Context, args) -> (dict, MassEnergizeAPIError):
    try:
      event_id = args.pop("event_id")

      events_selected = Event.objects.select_related('image', 'community').prefetch_related('tags', 'invited_communities').filter(id=event_id)
      event_to_copy: Event = events_selected.first()
      if not event_to_copy:
        return None, InvalidResourceError()
      
      old_tags = event_to_copy.tags.all()
      event_to_copy.pk = None
      new_event = event_to_copy 
      new_event.name = event_to_copy.name + "-Copy"
      new_event.is_published=False
      new_event.is_global = False
      new_event.start_date_and_time = event_to_copy.start_date_and_time
      new_event.end_date_and_time = event_to_copy.end_date_and_time
      new_event.description = event_to_copy.description
      new_event.featured_summary = event_to_copy.featured_summary
      new_event.location = event_to_copy.location
      if not (event_to_copy.is_recurring == None):
        new_event.is_recurring = event_to_copy.is_recurring
        new_event.recurring_details = event_to_copy.recurring_details
      new_event.save()

      #copy tags over
      for t in old_tags:
        new_event.tags.add(t)

      return new_event, None
    except Exception as e:
      capture_message(str(e), level="error")
      return None, CustomMassenergizeError(e)

  def list_recurring_event_exceptions(self, context: Context, args) -> (list, MassEnergizeAPIError):
    try:
      community_id = args.pop("community_id", None)
      subdomain = args.pop("subdomain", None)
      user_id = args.pop("user_id", None)
      event_id = args.pop("event_id", None)

      if community_id:
        #TODO: also account for communities who are added as invited_communities
        query =Q(community__id=community_id)
        events = Event.objects.select_related('image', 'community').prefetch_related('tags', 'invited_communities').filter(query)

      elif subdomain:
        query =  Q(community__subdomain=subdomain)
        events = Event.objects.select_related('image', 'community').prefetch_related('tags', 'invited_communities').filter(query)

      elif user_id:
        events = EventAttendee.objects.filter(user_id=user_id)

      elif event_id:
        events = Event.objects.filter(id=event_id).select_related('image', 'community').prefetch_related('tags', 'invited_communities')

      else:
        # not information required
        raise Exception("events.exceptions.list requires community, subdomain, user or event id")

      exceptions = []
      for event in events.all():
        e = RecurringEventException.objects.filter(event=event).first()
        if e:
          exceptions.append(event.id)

      return exceptions, None
    except Exception as e:
      capture_message(str(e), level="error")
      return None, CustomMassenergizeError(e)

  def list_events(self, context: Context, args) -> (list, MassEnergizeAPIError):
    community_id = args.pop("community_id", None)
    subdomain = args.pop("subdomain", None)
    user_id = args.pop("user_id", None)
    
    if community_id:
      #TODO: also account for communities who are added as invited_communities
      query =Q(community__id=community_id)
      events = Event.objects.select_related('image', 'community').prefetch_related('tags', 'invited_communities').filter(query)
      
    elif subdomain:
      query =  Q(community__subdomain=subdomain)
      events = Event.objects.select_related('image', 'community').prefetch_related('tags', 'invited_communities').filter(query)
      
    elif user_id:
      events = EventAttendee.objects.filter(user_id=user_id)
      
    else:
      events = []
    
    if not context.is_sandbox and events:
      events = events.filter(is_published=True)

    return events, None


  def create_event(self, context: Context, args) -> (dict, MassEnergizeAPIError):
    
    try:
      image = args.pop('image', None)
      tags = args.pop('tags', [])
      community = args.pop("community_id", None)
      start_date_and_time = args.get('start_date_and_time', None)
      end_date_and_time = args.get('end_date_and_time', None)

      is_recurring  = args.pop('is_recurring', False)
      if is_recurring == False or is_recurring == "false" or is_recurring == "":
        recurring = False
      else: recurring = True
      recurring_type = args.pop('recurring_type', None)
      separation_count = args.pop('separation_count', None)
      if separation_count:
        separation_count = int(separation_count)
    
      day_of_week = args.pop('day_of_week', None)
      week_of_month = args.pop("week_of_month", None)
      if recurring_type != "month":
        week_of_month = None

      have_address = args.pop('have_address', False)
      if not have_address:
        args['location'] = None

      if community:
        community = Community.objects.get(pk=community)
        if not community:
          return None, CustomMassenergizeError("Please provide a valid community_id")

      new_event: Event = Event.objects.create(**args)
      if community:
        new_event.community = community

      if image:
        media = Media.objects.create(file=image, name=f"ImageFor{args.get('name', '')}Event")
        new_event.image = media

      if tags:
        new_event.tags.set(tags)

      if recurring:

        # check that the event's start date coincides with the recurrence pattern if it is listed as recurring
        err, message = _check_recurring_date(start_date_and_time, end_date_and_time, day_of_week, week_of_month)
        if err:
          return None, CustomMassenergizeError(message)

        if recurring_type == "week" and week_of_month: 
          return None, CustomMassenergizeError("Cannot fill out week of month field if your event is weekly")
        
        new_event.is_recurring = True
        new_event.recurring_details = {
          "recurring_type": recurring_type, 
          "separation_count": separation_count, 
          "day_of_week": day_of_week, 
          "week_of_month": week_of_month
        } 

      new_event.save()      
      return new_event, None
    except Exception as e:
      capture_message(str(e), level="error")
      return None, CustomMassenergizeError(e)

  def update_event(self, context: Context, args) -> (dict, MassEnergizeAPIError):
    try:
      event_id = args.pop('event_id', None)
      image = args.pop('image', None)
      tags = args.pop('tags', [])
      start_date_and_time = args.get('start_date_and_time', None)
      end_date_and_time = args.get('end_date_and_time', None)

      recurring  = args.get('is_recurring', False)
      recurring_type = args.pop('recurring_type', None)
      separation_count = args.pop('separation_count', None)
      if separation_count:
        separation_count = int(separation_count)
      day_of_week = args.pop('day_of_week', None)
      week_of_month = args.pop("week_of_month", None)
      rescheduled_start_datetime = args.pop('rescheduled_start_datetime', False)
      rescheduled_end_datetime = args.pop('rescheduled_end_datetime', False)

      if recurring_type != "month":
        week_of_month = None
      upcoming_is_cancelled = args.pop("upcoming_is_cancelled", None)
      upcoming_is_rescheduled = args.pop('upcoming_is_rescheduled', None)

      events = Event.objects.filter(id=event_id)
      if not events:
        return None, CustomMassenergizeError(f"No event with id: {event_id}")

      have_address = args.pop('have_address', False)
      if not have_address:
        args['location'] = None

      community = args.pop("community_id", None)
      if community:
        community = Community.objects.filter(pk=community).first()

      events.update(**args)
      event: Event = events.first()

      event.is_recurring = recurring
      if start_date_and_time:
        event.start_date_and_time = start_date_and_time
      if end_date_and_time:
        event.end_date_and_time = end_date_and_time

      if image:
        media = Media.objects.create(file=image, name=f"ImageFor{args.get('name', '')}Event")
        event.image = media
      
      if community:
        event.community = community
      else:
        event.community = None

      if tags:
        event.tags.set(tags)

      event.save()

      if recurring:

        # check that the event's start date coincides with the recurrence pattern if it is listed as recurring
        err, message = _check_recurring_date(start_date_and_time, end_date_and_time, day_of_week, week_of_month)
        if err:
          return None, CustomMassenergizeError(message)

        # this seems to be an invalid check.  Even for monthly events, you have the day_of_week 
        #if week_of_month: return None, CustomMassenergizeError("Cannot fill out week of month field if your event is weekly")
        if recurring_type == "week" and week_of_month: 
          return None, CustomMassenergizeError("Cannot fill out week of month field if your event is weekly")

        event.is_recurring = True
        event.recurring_details = {
            "recurring_type": recurring_type, 
            "separation_count": separation_count, 
            "day_of_week": day_of_week, 
            "week_of_month": week_of_month
        } 

        if upcoming_is_cancelled and upcoming_is_rescheduled:
          return None, CustomMassenergizeError("Cannot cancel and reschedule next instance of a recurring event at the same time")

        # CAdmin is cancelling the upcoming event instance     
        if not event.recurring_details:
          event.recurring_details = { }
        event.recurring_details["is_cancelled"] = upcoming_is_cancelled


        # check if there was a previously rescheduled event instance
        rescheduled: RecurringEventException = RecurringEventException.objects.filter(event=event).first()

        #CAdmin is rescheduling the upcoming event instance
        if upcoming_is_rescheduled:
          # only create the event and recurring event exception if the event is being newly rescheduled, 
          # otherwise, don't do anything
          if not rescheduled:

            rescheduled_event = Event.objects.create(
              name = event.name + " (rescheduled)", 
              featured_summary = event.featured_summary, 
              start_date_and_time = rescheduled_start_datetime,
              end_date_and_time = rescheduled_end_datetime,
              description = event.description, 
              community = event.community, 
              location = event.location, 
              image = event.image, 
              archive = event.archive, 
              is_global = event.is_global, 
              external_link = event.external_link, 
              more_info = event.more_info, 
              is_deleted = event.is_deleted, 
              is_published = event.is_published, 
              rank = event.rank, 
              is_recurring = False, 
              recurring_details = None
            )
            rescheduled_event.save()

            old_tags = event.tags.all()
            old_communities = event.invited_communities.all()

            for t in old_tags:
              rescheduled_event.tags.add(t)
            for c in old_communities:
              rescheduled_event.invited_communities.add(c)

            rescheduled_event.save()

            rescheduled = RecurringEventException.objects.create(
            event = event,  
            former_time = event.start_date_and_time, 
            rescheduled_event = rescheduled_event
            )
#
          # they are trying to modify an existing event that is rescheduled
          elif rescheduled:
            ev = rescheduled.rescheduled_event
            ev.start_date_and_time = rescheduled_start_datetime
            ev.end_date_and_time = rescheduled_end_datetime
            ev.save()
          rescheduled.save()

        # CAdmin is not rescheduling the upcoming event instance
        else:
          #this is a new update = there was a previously rescheduled event, now the CAdmin wants to get rid of it
          if rescheduled: 
            rescheduled.rescheduled_event.delete()
            rescheduled.delete()

        event.save()
      
      return event, None
    except Exception as e:
      capture_message(str(e), level="error")
      return None, CustomMassenergizeError(e)

  def update_recurring_event_date(self, context: Context, args) -> (dict, MassEnergizeAPIError):
    community_id = args.pop("community_id", None)
    subdomain = args.pop("subdomain", None)
    user_id = args.pop("user_id", None)
    
    
    if community_id:
      #TODO: also account for communities who are added as invited_communities
      query =Q(community__id=community_id)
      events = Event.objects.select_related('image', 'community').prefetch_related('tags', 'invited_communities').filter(query)
      
    elif subdomain:
      # testing only
      query =  Q(community__subdomain=subdomain)
      events = Event.objects.select_related('image', 'community').prefetch_related('tags', 'invited_communities').filter(query)
      

    elif user_id:
      events = EventAttendee.objects.filter(user_id=user_id)
      
    else:
      events = []
    
    for event in events.iterator():
      if not event.is_recurring or not event.recurring_details['separation_count']:
        continue
      weekdays = {"Monday":0, "Tuesday":1, "Wednesday":2, "Thursday":3, "Friday":4, "Saturday":5, "Sunday":6}
      converter = {"first":1, "second":2, "third":3, "fourth":4}
      
      try:
        sep_count = int(event.recurring_details['separation_count'])
        
        start_date = event.start_date_and_time
        end_date = event.end_date_and_time
        duration = end_date - start_date
        tod = datetime.datetime.utcnow() 
        today = pytz.utc.localize(tod)
        if event.recurring_details['recurring_type'] == "week":
          while (start_date < today):
            start_date += timedelta(7*sep_count)
            end_date = start_date + duration
          event.start_date_and_time = start_date
          event.end_date_and_time = end_date
        elif event.recurring_details['recurring_type'] == "month":
          
          while (start_date < today):
            # use timedelta to get the new month
            new_month = start_date + timedelta((sep_count * 31) + 1)
            
            # find the corresponding ith day of the jth month
            
            obj = calendar.Calendar()
            date_of_first_weekday = 1
  
            for day in obj.itermonthdates(int(new_month.year), int(new_month.month)):
              if int(day.day) >= 8:
                continue
              d1 = pytz.utc.localize(datetime.datetime(int(day.year), int(day.month), int(day.day)))
              if calendar.day_name[d1.weekday()] == event.recurring_details['day_of_week']:
                date_of_first_weekday = int(day.day)
                break
            
            upcoming_date = date_of_first_weekday + ((converter[event.recurring_details['week_of_month']] - 1)*7)
            
            start_date = pytz.utc.localize(datetime.datetime(new_month.year, new_month.month, upcoming_date, start_date.hour, start_date.minute))
          event.start_date_and_time = start_date
          event.end_date_and_time = start_date + duration
          
        event.save()
        exception = RecurringEventException.objects.filter(event=event).first()
        if exception and pytz.utc.localize(exception.former_time) < pytz.utc.localize(event.start_date_and_time):
          exception.delete()
      except Exception as e:
        print(str(e))
        return CustomMassenergizeError(str(e))
    return events, None

  def rank_event(self, args) -> (dict, MassEnergizeAPIError):
    try:
      id = args.get('id', None)
      rank = args.get('rank', None)
      if id and rank:

        events = Event.objects.filter(id=id)
        events.update(rank=rank)
        return events.first(), None
      else:
        raise Exception("Rank and ID not provided to events.rank")
      
    except Exception as e:
      capture_message(str(e), level="error")
      return None, CustomMassenergizeError(e)

  def delete_event(self, context: Context, event_id) -> (dict, MassEnergizeAPIError):
    try:
      events = Event.objects.filter(id=event_id)
      if not events:
        return None, InvalidResourceError()
      
      if len(events) > 1:
        return None, CustomMassenergizeError("Deleting multiple events not supported")

      events.delete()
      return events.first(), None
    except Exception as e:
      capture_message(str(e), level="error")
      return None, CustomMassenergizeError(e)


  def list_events_for_community_admin(self, context: Context, args) -> (list, MassEnergizeAPIError):
    try:
      community_id = args.pop("community_id", None)

      if context.user_is_super_admin:
        return self.list_events_for_super_admin(context)

      elif not context.user_is_community_admin:
        return None, NotAuthorizedError()

      # community_id coming from admin portal is 'undefined'
      if not community_id or community_id=='undefined':
        user = UserProfile.objects.get(pk=context.user_id)
        admin_groups = user.communityadmingroup_set.all()
        comm_ids = [ag.community.id for ag in admin_groups]
        # don't return the events that are rescheduled instances of recurring events - these should be edited by CAdmins in the recurring event's edit form, 
        # not as their own separate events
        events = Event.objects.filter(Q(community__id__in = comm_ids) | Q(is_global=True), is_deleted=False).exclude(name__contains=" (rescheduled)").select_related('image', 'community').prefetch_related('tags')

        return events, None

      events = Event.objects.filter(Q(community__id = community_id) | Q(is_global=True), is_deleted=False).select_related('image', 'community').prefetch_related('tags')
      return events, None
    except Exception as e:
      capture_message(str(e), level="error")
      return None, CustomMassenergizeError(e)


  def list_events_for_super_admin(self, context: Context):
    try:
      if not context.user_is_super_admin:
        return None, NotAuthorizedError()
      # don't return the events that are rescheduled instances of recurring events - these should be edited by CAdmins in the recurring event's edit form, 
      # not as their own separate events
      events = Event.objects.filter(is_deleted=False).exclude(name__contains=" (rescheduled)").select_related('image', 'community').prefetch_related('tags')
      return events, None
    except Exception as e:
      capture_message(str(e), level="error")
      return None, CustomMassenergizeError(str(e))


  def get_rsvp_status(self, context: Context, args) -> (dict, MassEnergizeAPIError):
    try:
      event_id = args.pop("event_id", None)
      args: dict = context.args
      user = get_user_or_die(context, args)
      event = Event.objects.filter(pk=event_id).first()
      if not event:
        return None, InvalidResourceError()

      event_attendee = EventAttendee.objects.filter(event=event, user=user)
      if event_attendee:
        return event_attendee.first(), None
      else:
        return None, None
    except Exception as e:
      capture_message(str(e), level="error")
      return None, CustomMassenergizeError(e)

  def rsvp_update(self, context: Context, args) -> (dict, MassEnergizeAPIError):
    try:
      event_id = args.pop("event_id", None)
      status = args.pop("status", "SAVE")
      user = get_user_or_die(context, args)      
      event = Event.objects.filter(pk=event_id).first()
      if not event:
        return None, InvalidResourceError()

      event_attendees = EventAttendee.objects.filter(event=event, user=user, is_deleted=False)
      if event_attendees:
        event_attendee = event_attendees.first()
        if status=="Not Going":
          event_attendee.delete()
        else:
          event_attendee.status = status
          event_attendee.save()
      elif status != "Not Going":
        event_attendee = EventAttendee.objects.create(event=event, user=user, status=status)
      else:
        return None, None
      return event_attendee, None
      
    except Exception as e:
      capture_message(str(e), level="error")
      return None, CustomMassenergizeError(e)

  def rsvp_remove(self, context: Context, args) -> (dict, MassEnergizeAPIError):
    try:
      rsvp_id = args.pop("rsvp_id", None)
      event_id = args.pop("event_id", None)
      user = get_user_or_die(context, args)

      if rsvp_id:
        result = EventAttendee.objects.filter(pk=rsvp_id).delete()
      elif event_id:
        event = Event.objects.filter(pk=event_id).first()
        if not event:
          return None, InvalidResourceError()
        result = EventAttendee.objects.filter(event=event, user=user).delete()
      else:
        raise Exception("events.rsvp.remove: must specify rsvp or event id")
          
      return result, None
    except Exception as e:
      capture_message(str(e), level="error")
      return None, CustomMassenergizeError(e)