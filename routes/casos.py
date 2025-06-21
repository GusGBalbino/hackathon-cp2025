from fastapi import APIRouter, HTTPException
from typing import List
from models import CasoCreate, Caso, BODados
from database import supabase
from utils import wkb_to_coords
from geopy.geocoders import Nominatim

router = APIRouter(tags=["Casos"])

@router.post("/casos", response_model=Caso, status_code=201, summary="Registra um novo caso")
def create_caso(caso: CasoCreate):
    try:
        # Geocodificação reversa
        geolocator = Nominatim(user_agent="hackathon_app")
        location = geolocator.reverse(f"{caso.latitude}, {caso.longitude}", language='pt')
        cidade = estado = None

        if location and location.raw and 'address' in location.raw:
            cidade = location.raw['address'].get('city') or location.raw['address'].get('town') or location.raw['address'].get('village')
            estado = location.raw['address'].get('state')

        localizacao_wkt = f'POINT({caso.longitude} {caso.latitude})'

        data, count = supabase.table('casos').insert({
            'descricao': caso.descricao,
            'localizacao': localizacao_wkt,
            'user_id': caso.user_id,
            'cidade': cidade,
            'estado': estado
        }).execute()

        if not data[1]:
            raise HTTPException(status_code=500, detail="Não foi possível registrar o caso.")
        
        created_caso = data[1][0]
        
        return {
            "id": created_caso['id'],
            "descricao": created_caso['descricao'],
            "latitude": caso.latitude,
            "longitude": caso.longitude,
            "cidade": cidade,
            "estado": estado,
            "user_id": caso.user_id,
            "data_ocorrencia": created_caso['data_ocorrencia'],
            "bo_solicitado": created_caso['bo_solicitado']
        }
    except Exception as e:
        print(f"Erro ao criar caso: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get-lat-long-by-id")
def get_lat_long_by_id(id: str):
    try:
        response = supabase.table('casos').select('localizacao').eq('id', id).execute()
        wkb_hex = response.data[0]['localizacao']
        lat, lon = wkb_to_coords(wkb_hex)
        return {"latitude": lat, "longitude": lon}
    except Exception as e:
        print(f"Erro ao buscar latitude e longitude: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/casos/{caso_id}/gerar-bo", status_code=200, summary="Solicita a geração de um B.O.")
def gerar_bo(caso_id: str, dados_bo: BODados):
    try:
        dados_bo_dict = dados_bo.model_dump()
        data, count = supabase.table('casos').update({
            'bo_solicitado': True,
            'dados_bo': dados_bo_dict
        }).eq('id', caso_id).execute()
        if not data[1]:
            raise HTTPException(status_code=404, detail="Caso não encontrado.")
        print(f"Simulação: B.O. solicitado para o caso {caso_id} com os dados: {dados_bo_dict}")
        return {"mensagem": "Solicitação de Boletim de Ocorrência enviada com sucesso.", "caso_id": caso_id}
    except Exception as e:
        print(f"Erro ao gerar B.O.: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/casos/{caso_id}", summary="Busca os detalhes de um caso pelo id")
def get_caso_by_id(caso_id: str):
    try:
        response = supabase.table('casos').select('*').eq('id', caso_id).execute()
        if not response.data or len(response.data) == 0:
            raise HTTPException(status_code=404, detail="Caso não encontrado.")
        
        return response.data[0]
    except Exception as e:      
        print(f"Erro ao buscar caso por id: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 