import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from myapp.models import (
    Farm,
    SubFarm,
    Deforestation,
    ERDA,
)

class Command(BaseCommand):
    def handle(self, *args, **options):
        file = os.path.join(settings.BASE_DIR, 'myapp/management/commands/files/erda.csv')
        # Ie. 
        # FARM ID;AT RISK OF DEFORESTATION
        # 8012;NO

        with open(file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')  # Especifica el separador ";"
            next(reader)  # Salta la primera fila (encabezado)
            
            for row in reader:
                sub_fam_name = row[0]
                risk = row[1] == "SI"

                sub_name = None
                if "_" in sub_fam_name:
                    sub_fam_data = sub_fam_name.split("_")
                    farm_id = sub_fam_data[0]
                    sub_name = sub_fam_data[1]
                else:
                    farm_id = sub_fam_name

                
                sub_farm = SubFarm.objects.filter(
                    farm__name=farm_id,
                    sub_name=sub_name,
                ).first()
                if sub_farm:
                    deforestation = ERDA(
                        sub_farm=sub_farm,
                        risk=risk,
                    )
                    deforestation.save()

