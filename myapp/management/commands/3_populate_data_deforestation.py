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
        file = os.path.join(settings.BASE_DIR, 'myapp/management/commands/files/deforestation.csv')
        # Ie. 
        # Farm ID;Nivel riesgo deforestación desde oficina;Fase resultado
        # 1671;Riesgo despreciable desde oficina;Fase 2

        with open(file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')  # Especifica el separador ";"
            next(reader)  # Salta la primera fila (encabezado)
            
            for row in reader:
                sub_farm_id = row[0]
                level = row[1]
                fase = row[2]
                sub_name = None
                if sub_farm_id:
                    if "_" in sub_farm_id:
                        sub_fam_data = sub_farm_id.split("_")
                        farm_id = sub_fam_data[0]
                        sub_name = sub_fam_data[1]
                    else: 
                        farm_id = sub_farm_id
                else: 
                    sub_name = None
                
                
                sub_farm = SubFarm.objects.filter(
                    farm__name=sub_farm_id,
                    sub_name=sub_name,
                ).first()

                deforestation = Deforestation(
                    sub_name=sub_farm,
                    level=level,
                    fase=fase,
                )
                deforestation.save()

