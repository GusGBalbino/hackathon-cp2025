from fastapi import APIRouter, HTTPException, Query
from typing import List
from models import UnidadeApoio, UnidadeApoioCreate
from database import supabase

router = APIRouter(tags=["Unidades"])

@router.get("/unidades-apoio/proximas", response_model=List[UnidadeApoio], summary="Encontra unidades de apoio próximas")
def get_unidades_proximas(
    lat: float = Query(..., description="Latitude da usuária"),
    lon: float = Query(..., description="Longitude da usuária"),
    raio_metros: float = Query(5000, description="Raio de busca em metros")
):
    try:
        response = supabase.rpc('buscar_unidades_proximas', {'lat': lat, 'lon': lon, 'raio_metros': raio_metros}).execute()
        if response.data is None:
            raise HTTPException(status_code=404, detail="Nenhuma unidade de apoio encontrada.")
        return response.data
    except Exception as e:
        print(f"Erro ao buscar unidades próximas: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/unidades-apoio", response_model=UnidadeApoio, status_code=201, summary="Cria uma nova unidade de apoio")
def create_unidade_apoio(unidade: UnidadeApoioCreate):
    try:
        localizacao_wkt = f'POINT({unidade.longitude} {unidade.latitude})'
        data, count = supabase.table('unidades_apoio').insert({
            'nome': unidade.nome,
            'tipo': unidade.tipo,
            'endereco': unidade.endereco,
            'telefone': unidade.telefone,
            'localizacao': localizacao_wkt
        }).execute()
        if not data[1]:
            raise HTTPException(status_code=500, detail="Não foi possível criar a unidade de apoio.")
        created = data[1][0]
        return {
            'id': created['id'],
            'nome': created['nome'],
            'tipo': created['tipo'],
            'endereco': created.get('endereco'),
            'telefone': created.get('telefone'),
            'latitude': unidade.latitude,
            'longitude': unidade.longitude,
        }
    except Exception as e:
        print(f"Erro ao criar unidade de apoio: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 