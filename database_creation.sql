-- Habilita a extensão PostGIS para trabalhar com dados geográficos.
-- No Supabase, você pode precisar habilitar isso na interface em Database -> Extensions.
CREATE EXTENSION IF NOT EXISTS postgis;

-- Habilita a extensão para gerar UUIDs, o padrão do Supabase para IDs.
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tabela para armazenar os casos relatados pelas usuárias.
CREATE TABLE public.casos (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  descricao TEXT NOT NULL,
  -- Usamos o tipo GEOGRAPHY do PostGIS para armazenar coordenadas.
  -- O SRID 4326 é o padrão para coordenadas WGS 84 (latitude/longitude).
  localizacao GEOGRAPHY(Point, 4326) NOT NULL,
  data_ocorrencia TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
  -- Flag para indicar se um B.O. foi solicitado para este caso.
  bo_solicitado BOOLEAN DEFAULT FALSE,
  -- Poderíamos adicionar um user_id se tivéssemos autenticação.
  -- usuario_id UUID REFERENCES auth.users(id)
  dados_bo JSONB -- Campo para armazenar dados adicionais do B.O. (nome, CPF, etc.)
);

-- Adiciona um índice espacial na coluna de localização para otimizar buscas geográficas.
CREATE INDEX idx_casos_localizacao ON public.casos USING GIST (localizacao);

COMMENT ON TABLE public.casos IS 'Armazena os relatos de incidentes feitos pelas usuárias.';
COMMENT ON COLUMN public.casos.localizacao IS 'Localização geográfica do incidente (Ponto).';


-- Tabela para armazenar informações sobre delegacias, postos da PM, etc.
CREATE TABLE public.unidades_apoio (
  id SERIAL PRIMARY KEY,
  nome VARCHAR(255) NOT NULL,
  tipo VARCHAR(100) NOT NULL, -- Ex: 'Delegacia da Mulher', 'Polícia Militar', 'Guarda Municipal'
  endereco TEXT,
  telefone VARCHAR(20),
  localizacao GEOGRAPHY(Point, 4326) NOT NULL
);

-- Adiciona um índice espacial para otimizar buscas de unidades próximas.
CREATE INDEX idx_unidades_apoio_localizacao ON public.unidades_apoio USING GIST (localizacao);

COMMENT ON TABLE public.unidades_apoio IS 'Cadastro de delegacias, hospitais e outros pontos de apoio.';
COMMENT ON COLUMN public.unidades_apoio.tipo IS 'Tipo da unidade de apoio.';

-- Inserir alguns dados de exemplo (substitua por dados reais)
INSERT INTO public.unidades_apoio (nome, tipo, endereco, telefone, localizacao) VALUES
('1ª Delegacia de Defesa da Mulher (DDM)', 'Delegacia da Mulher', 'R. Dr. Bittencourt Rodrigues, 200 - Sé, São Paulo - SP', '(11) 3241-3328', ST_SetSRID(ST_MakePoint(-46.633308, -23.550520), 4326)),
('78º Distrito Policial - Jardins', 'Polícia Civil', 'Rua Estados Unidos, 1729 - Jardim America, São Paulo - SP', '(11) 3061-5911', ST_SetSRID(ST_MakePoint(-46.668701, -23.567330), 4326)),
('Base Comunitária PM - Pq. Ibirapuera', 'Polícia Militar', 'Av. Pedro Álvares Cabral - Vila Mariana, São Paulo - SP', '(11) 5084-7549', ST_SetSRID(ST_MakePoint(-46.658939, -23.588242), 4326));


-- Função para buscar unidades de apoio próximas a um ponto geográfico.
-- Usamos RPC (Remote Procedure Call) no Supabase para chamar esta função.
CREATE OR REPLACE FUNCTION buscar_unidades_proximas(lat float, lon float)
RETURNS TABLE (
  id integer,
  nome varchar,
  tipo varchar,
  endereco text,
  telefone varchar,
  latitude float,
  longitude float,
  distancia_metros float
) AS $$
BEGIN
  RETURN QUERY
  SELECT
    ua.id,
    ua.nome,
    ua.tipo,
    ua.endereco,
    ua.telefone,
    ST_Y(ua.localizacao::geometry) as latitude,
    ST_X(ua.localizacao::geometry) as longitude,
    -- Calcula a distância em metros do ponto fornecido até cada unidade.
    ST_Distance(ua.localizacao, ST_SetSRID(ST_MakePoint(lon, lat), 4326)) as distancia_metros
  FROM
    public.unidades_apoio AS ua
  ORDER BY
    -- Ordena pela distância para que as mais próximas apareçam primeiro.
    ua.localizacao <-> ST_SetSRID(ST_MakePoint(lon, lat), 4326);
END;
$$ LANGUAGE plpgsql;

ALTER TABLE casos
ADD COLUMN user_id VARCHAR(255),
ADD COLUMN cidade VARCHAR(255),
ADD COLUMN estado VARCHAR(255);
