# API de Segurança da Mulher

> Projeto desenvolvido durante o **Hackathon Mulher mais Segura** na **Campus Party 2025**, em Brasília.

Este projeto é um backend desenvolvido em **FastAPI** com integração ao **Supabase** para armazenamento e consultas geoespaciais, criado para um hackathon. O objetivo é fornecer uma API para relatar casos de assédio, visualizar zonas de risco e encontrar unidades de apoio próximas, facilitando o acesso à segurança para mulheres.

## Funcionalidades
- **Registro de casos de assédio** com localização geográfica.
- **Consulta de zonas de risco** baseadas na concentração de casos.
- **Busca de unidades de apoio** (delegacias, hospitais, etc.) próximas à usuária.
- **Solicitação de Boletim de Ocorrência (B.O.)** para um caso registrado.

## Tecnologias Utilizadas
- [FastAPI](https://fastapi.tiangolo.com/)
- [Supabase](https://supabase.com/) (PostgreSQL + PostGIS)
- [Geopy](https://geopy.readthedocs.io/) para geocodificação reversa
- [Shapely](https://shapely.readthedocs.io/) para manipulação de geometrias
- [dotenv](https://pypi.org/project/python-dotenv/) para variáveis de ambiente

## Estrutura do Projeto
```
├── main.py                # Ponto de entrada da API FastAPI
├── database.py            # Conexão e configuração do Supabase
├── models.py              # Modelos Pydantic para validação e schemas
├── routes/                # Rotas da API (casos, unidades, zonas)
├── database_creation.sql  # Script SQL para criação das tabelas e funções no Supabase
├── database_function.sql  # Funções SQL para buscas geoespaciais
├── utils.py               # Funções utilitárias
```

## Endpoints Principais

### Casos
- `POST /casos` — Registra um novo caso de assédio.
- `GET /casos/{caso_id}` — Busca detalhes de um caso pelo ID.
- `POST /casos/{caso_id}/gerar-bo` — Solicita a geração de um B.O. para o caso.
- `GET /get-lat-long-by-id?id=...` — Retorna latitude/longitude de um caso.

### Unidades de Apoio
- `GET /unidades-apoio/proximas?lat=...&lon=...&raio_metros=...` — Lista unidades de apoio próximas a uma localização.
- `POST /unidades-apoio` — Cria uma nova unidade de apoio.

### Zonas de Risco
- `GET /zonas-risco?lat=...&lon=...&raio_km=...` — Retorna zonas de risco próximas a uma localização.

### Health Check
- `GET /health` — Verifica se a API está online.

## Como rodar localmente
1. **Clone o repositório:**
   ```bash
   git clone <repo-url>
   cd hackathon
   ```
2. **Crie e ative um ambiente virtual:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure as variáveis de ambiente:**
   - Crie um arquivo `.env` na raiz com:
     ```
     SUPABASE_URL=...  # URL do seu projeto Supabase
     SUPABASE_KEY=...  # Chave de API do Supabase
     ```
5. **Execute as migrações SQL no Supabase:**
   - Suba as tabelas e funções usando os scripts `database_creation.sql` e `database_function.sql` no painel do Supabase.
6. **Inicie a API:**
   ```bash
   uvicorn main:app --reload
   ```

Acesse a documentação interativa em: [http://localhost:8000/docs](http://localhost:8000/docs)

## Observações
- O projeto utiliza recursos geoespaciais do PostGIS, então o Supabase deve ter a extensão PostGIS habilitada.
- Os dados de unidades de apoio podem ser inseridos manualmente ou via script SQL.
- O endpoint de B.O. simula a solicitação, podendo ser adaptado para integração real.

## Licença
Projeto desenvolvido para fins de hackathon. Sinta-se livre para adaptar e evoluir! 