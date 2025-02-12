from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Farm, ERDA
from django.shortcuts import render, get_object_or_404


def lista_productos(request):
    query = request.GET.get('q', '')  # Captura el término de búsqueda
    query = query.replace(' ', '')
    if query:
        fincas = Farm.objects.filter(name__icontains=query)
    else:
        fincas = Farm.objects.all()

    return render(request, 'lista_productos.html', {'fincas': fincas})

def detail(request, id):
    farm_obj = get_object_or_404(Farm, id=id)  # Obtener el producto o lanzar 404 si no existe
    geometria = 0

    area = 0
    subfarms = farm_obj.farm_subfarms.all()
    for subfarm in subfarms:
        subfarm_area_pol = subfarm.area_pol or 0
        if subfarm_area_pol:
            area = area + subfarm_area_pol
        else:
            areas_erda = subfarm.farm_erda.all()
            for sub_area in areas_erda:
                area = area + sub_area.area_pol


    area = round(area, 2)

    farm = {
        "name": farm_obj.name,
        "area": area,
        "geometria": geometria,
        "total_lotes_finca": 2,
        "is_riesgo_deforestacion": 0,
        "total_riesgo_deforestacion": 0,
        "riesgo_deforestacion": 33,
        "total_puntos_verificar": 0,
        "analisis": 0,
        "fase_deforestacion": 0,
        "tecnico": 0,
    }

    return render(request, 'detail.html', {'farm': farm})
