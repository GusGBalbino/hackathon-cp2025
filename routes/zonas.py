from fastapi import APIRouter, HTTPException, Query
from typing import List
from models import RiscoZona
from database import supabase

router = APIRouter(tags=["Zonas"])

@router.get("/zonas-risco", response_model=List[RiscoZona], summary="Retorna as zonas de risco próximas")
def get_zonas_risco(
    lat: float = Query(..., description="Latitude central"),
    lon: float = Query(..., description="Longitude central"),
    raio_km: float = Query(10, description="Raio em km")
):
    try:
        response = supabase.rpc('casos_proximos', {'lat': lat, 'lon': lon, 'raio_km': raio_km}).execute()
        casos_data = response.data
        zonas = {}
        for caso in casos_data:
            zona_key = (round(caso['latitude'], 3), round(caso['longitude'], 3))
            if zona_key not in zonas:
                zonas[zona_key] = {
                    'latitude': zona_key[0],
                    'longitude': zona_key[1],
                    'contagem': 0,
                    'caso_ids': []
                }
            zonas[zona_key]['contagem'] += 1
            zonas[zona_key]['caso_ids'].append(caso['id'])
        return list(zonas.values())
    except Exception as e:
        print(f"Erro ao buscar zonas de risco: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 