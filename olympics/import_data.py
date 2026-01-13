import os
import pandas as pd
from olympics.models import Athlete, Event, Medal
from django.conf import settings

DATA_FOLDER = os.path.join(settings.BASE_DIR, 'data')

def import_athletes():
    file_path = os.path.join(DATA_FOLDER, 'athletes.csv')
    print(f"Loading athletes data from: {file_path}")
    df = pd.read_csv(file_path)
    for _, row in df.iterrows():
        Athlete.objects.create(
            name=row['name'],
            country=row['country'],
            sport=row['disciplines'],
            birth_date=row.get('birth_date', None),
            birth_place=row.get('birth_place', ""),
            height=row.get('height', None),
            weight=row.get('weight', None),
            coach=row.get('coach', "")
        )
    print("Athletes data imported successfully.")


def import_events():
    file_path = os.path.join(DATA_FOLDER, 'events.csv')
    print(f"Loading events data from: {file_path}")
    df = pd.read_csv(file_path)
    for _, row in df.iterrows():
        Event.objects.create(
            name=row['event'],
            sport=row['sport'],
            sport_code=row['sport_code']
        )
    print("Events data imported successfully.")

def import_medals():
    file_path = os.path.join(DATA_FOLDER, 'medals.csv')
    print(f"Loading medals data from: {file_path}")
    df = pd.read_csv(file_path)

    for _, row in df.iterrows():
        # Debugging outputs
        print(f"Processing medal row: {row}")

        # Fetch the athlete and event
        athlete = Athlete.objects.filter(name=row['name']).first()
        event = Event.objects.filter(name=row['event']).first()

        # Ensure athlete and event exist
        if not athlete:
            print(f"Warning: Athlete '{row['name']}' not found.")
            continue
        if not event:
            print(f"Warning: Event '{row['event']}' not found.")
            continue

        # Create the medal entry
        Medal.objects.create(
            medal_type=row['medal_type'],
            medal_date=row.get('medal_date', None),
            athlete=athlete,
            discipline=row.get('discipline', ""),
            event=event,
            country=row['country']
        )
    print("Medals data imported successfully.")

