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
        file = os.path.join(settings.BASE_DIR, 'myapp/management/commands/files/sub_farm.csv')
        # Ie. 
        # Num_int;farm_id;Tecnico;map_date;Region;Nom_pol;area_pol;latitud;longitud
        # 2770;2770_A;;XXXX;XXXX;XXXXX;0,4782590;XXXX;XXXX


        with open(file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')  # Especifica el separador ";"
            next(reader)  # Salta la primera fila (encabezado)
            
            for row in reader:
                print(row)
                farm_id = row[0]
                sub_fam_name = row[1]
                technical = row[2]
                map_date = None # row[3]
                region = row[4]
                nom_pol = row[5]
                area_pol = float(row[6].replace(',','.'))
                latitude = row[7]
                longitude = row[8]

                if sub_fam_name:
                    if "_" in sub_fam_name:
                        sub_fam_name = sub_fam_name.split("_")[1]
                    else: 
                        sub_fam_name = None
                else: 
                    sub_fam_name = None
                
                
                farm = Farm.objects.filter(name=farm_id).first()
                if not farm:
                    farm = Farm(
                        name=farm_id,
                    )
                    farm.save()

                sub_farm = SubFarm.objects.filter(
                    farm=farm,
                    sub_name=sub_fam_name,
                ).first()
                if not sub_farm:
                    sub_farm = SubFarm(
                        farm=farm,
                        sub_name=sub_fam_name,
                        technical=technical,
                        map_date=map_date,
                        region=region,
                        nom_pol=nom_pol,
                        area_pol=area_pol,
                        latitude=latitude,
                        longitude=longitude,
                    )
                    sub_farm.save()

