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
        file = os.path.join(settings.BASE_DIR, 'myapp/management/commands/files/farm.csv')
        # Ie.
        # Número interno de finca MOVE;Región/ Zona o cooperativa;Técnico a cargo;Nombre productor;Municipio;Departamento
        # 1626;XXXX;XXX;XXX;XXX;XX
        print("cargando farm")
        with open(file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')  # Especifica el separador ";"
            next(reader)  # Salta la primera fila (encabezado)
            
            for row in reader:
                name = row[0]
                owner = row[1]
                region = row[2]
                municipio = row[3]
                departamento = row[4]
        
                farm = Farm(
                    name=name,
                    owner=owner,
                    region=region,
                    municipio=municipio,
                    departamento=departamento,
                )
                farm.save()

        file = os.path.join(settings.BASE_DIR, 'myapp/management/commands/files/sub_farm.csv')
        # Ie. 
        # Num_int;farm_id;Tecnico;map_date;Region;Nom_pol;area_pol;latitud;longitud
        # 2770;2770_A;;XXXX;XXXX;XXXXX;0,4782590;XXXX;XXXX

        print("cargando sub_farm")

        with open(file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')  # Especifica el separador ";"
            next(reader)  # Salta la primera fila (encabezado)
            
            for row in reader:
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


        file = os.path.join(settings.BASE_DIR, 'myapp/management/commands/files/deforestation.csv')
        # Ie. 
        # Farm ID;Nivel riesgo deforestación desde oficina;Fase resultado
        # 1671;Riesgo despreciable desde oficina;Fase 2
        print("cargando deforestation")

        with open(file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')  # Especifica el separador ";"
            next(reader)  # Salta la primera fila (encabezado)
            
            for row in reader:
                sub_farm_id = row[0]
                farm_id = row[0]
                level = row[1]
                fase = row[2]
                sub_name = None
                if sub_farm_id:
                    if "_" in sub_farm_id:
                        sub_fam_data = sub_fam_name.split("_")
                        farm_id = sub_fam_data[0]
                        sub_name = sub_fam_data[1]
                    else: 
                        farm_id = sub_fam_name
                else: 
                    sub_fam_name = None
                
                
                sub_farm = SubFarm.objects.filter(
                    farm__name=farm_id,
                    sub_name=sub_name,
                ).first()
                if sub_farm and level and fase:
                    deforestation = Deforestation(
                        sub_farm=sub_farm,
                        level=level,
                        fase=fase,
                    )
                    deforestation.save()

        file = os.path.join(settings.BASE_DIR, 'myapp/management/commands/files/erda.csv')
        # Ie. 
        # FARM ID;AT RISK OF DEFORESTATION
        # 8012;NO
        print("cargando erda")

        with open(file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')  # Especifica el separador ";"
            next(reader)  # Salta la primera fila (encabezado)
            
            for row in reader:
                sub_farm_id = row[0]
                farm_id = row[0]
                risk = row[1] == "SI"

                sub_name = None
                if sub_farm_id:
                    if "_" in sub_farm_id:
                        sub_fam_data = sub_fam_name.split("_")
                        farm_id = sub_fam_data[0]
                        sub_name = sub_fam_data[1]
                    else: 
                        farm_id = sub_fam_name
                else: 
                    sub_fam_name = None
                
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
