import json
from django.core.management.base import BaseCommand
from locations.models import Airport, Lounge, LoungeSchedule, EntryCondition, Feature, GalleryImage


class Command(BaseCommand):
    help = 'Import data from JSON file'

    def handle(self, *args, **options):
        with open('output.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

            for item in data:
                airport_data = item['airport']
                airport, _ = Airport.objects.get_or_create(
                    name=airport_data['name'],
                    code=airport_data['code'],
                    city=airport_data['city'],
                    country=airport_data['country'],
                    location=f"POINT({airport_data['coordinates']['lng']} {
                        airport_data['coordinates']['lat']})"
                )

                for lounge_data in item['lounges']:
                    lounge, _ = Lounge.objects.get_or_create(
                        airport_id=airport,
                        name=lounge_data['name'],
                        description=lounge_data.get('description', ''),
                        terminal=lounge_data.get('terminal', ''),
                        # пример установки базовой цены
                        base_price=lounge_data['entry_conditions']['costs'][0]['cost']
                    )

                    for schedule_data in lounge_data['schedule']:
                        LoungeSchedule.objects.create(
                            lounge=lounge,
                            valid_from_time=schedule_data['valid_from_time'],
                            valid_till_time=schedule_data['valid_till_time'],
                            valid_days=schedule_data['valid_days']
                        )

                    for cost_data in lounge_data['entry_conditions']['costs']:
                        EntryCondition.objects.create(
                            lounge=lounge,
                            type=cost_data['type'],
                            cost=cost_data['cost'],
                            max_stay_duration=lounge_data['entry_conditions']['max_stay_duration']
                        )

                    for feature_name in lounge_data['features']:
                        Feature.objects.create(
                            lounge=lounge, name=feature_name)

                    for image_url in lounge_data['gallery']:
                        GalleryImage.objects.create(
                            lounge=lounge, image_url=image_url)

            self.stdout.write(self.style.SUCCESS('Data imported successfully'))
