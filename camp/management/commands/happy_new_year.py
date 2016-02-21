
from django.core.management.base import NoArgsCommand
from django.utils.encoding import smart_str
from datetime import datetime, timedelta
from camp.models import Event, Meal, UserProfile, MealShift
import csv



def _parse_date(value):
    year, month, day = map(int, value.split('-'))

    return datetime(year, month, day)

class Command(NoArgsCommand):
    help = "Sets up a new event/year"

    def add_arguments(self, parser):
        parser.add_argument('start_date', action="store", type=_parse_date, help="in YYYY-MM-DD format")
        parser.add_argument('num_days', action="store", type=int, help="How long is this event?")
        parser.add_argument('--noinput', '--no-input',
            action='store_false', dest='interactive', default=True,
            help='Do NOT prompt the user for input of any kind.')

    def handle_noargs(self, **options):
        start_date = options['start_date']
        num_days = options['num_days']
        interactive = options['interactive']
        end_date = start_date + timedelta(days=num_days)

        event_name = "Burning Man %s" % start_date.year
        if Event.objects.filter(name=event_name).exists():
            if interactive:
                response = raw_input("%s exists - overwrite? (y/N) " % event_name)
            else:
                raise ValueError("Event %s exists, won't overwrite w/o input." % event_name)
            if response.strip().lower() != 'y':
                print "Not overwriting the existing event"
                return

            Event.objects.filter(name=event_name).delete()

        event = Event.objects.create(name=event_name,
            start_date=start_date, end_date=end_date)

        for i in range(num_days):
            day = start_date + timedelta(days=i)
            for kind, _ in Meal.Kinds:
                meal = Meal.objects.create(event=event, day=day, kind=kind)
                # Each meal needs a chef, who will define further shift needs.
                MealShift.objects.create(meal=meal, role=MealShift.Chef)

        # No need to reset shifts, as we keep old events and shifts (which are tied to events).

        # Reset camper fields that are year-specific, though.
        UserProfile.objects.update(has_ticket=False, looking_for_ticket=False,
            camping_this_year=False, date=None,
            arrival_day=None, departure_day=None)

        print "Done setting up %s" % event_name