import json
from pathlib import Path
from django.core.management.base import BaseCommand
from game.models import Destination

class Command(BaseCommand):
    help = 'Import destinations from expanded_dataset.json'

    def handle(self, *args, **kwargs):
        # __file__ is at:
        # C:\GLOBETROTTER\backend\globetrotter_project\game\management\commands\import_data.py
        # We need to reach the root folder: C:\GLOBETROTTER
        # Go up 5 levels:
        root_dir = Path(__file__).resolve().parents[5]
        json_path = root_dir / 'scripts' / 'expanded_dataset.json'
        
        self.stdout.write(f"Looking for JSON file at: {json_path}")
        
        try:
            with open(json_path, 'r') as f:
                data = json.load(f)
                for entry in data:
                    destination, created = Destination.objects.get_or_create(
                        city=entry.get('city'),
                        defaults={
                            'country': entry.get('country', ''),
                            'clues': entry.get('clues', []),
                            'fun_fact': entry.get('fun_fact', ''),
                            'trivia': entry.get('trivia', []),
                            'image_url': entry.get('image_url', ''),
                        }
                    )
                    if created:
                        self.stdout.write(f"Imported: {destination.city}")
                    else:
                        self.stdout.write(f"Skipped (exists): {destination.city}")
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File not found: {json_path}"))
