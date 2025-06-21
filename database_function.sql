CREATE OR REPLACE FUNCTION casos_proximos(lat float, lon float, raio_km float)
RETURNS TABLE (
  id uuid,
  descricao text,
  latitude float,
  longitude float,
  data_ocorrencia timestamptz,
  bo_solicitado bool
) AS $$
BEGIN
  RETURN QUERY
  SELECT
    c.id,
    c.descricao,
    ST_Y(c.localizacao::geometry) as latitude,
    ST_X(c.localizacao::geometry) as longitude,
    c.data_ocorrencia,
    c.bo_solicitado
  FROM
    public.casos AS c
  WHERE
    ST_DWithin(
      c.localizacao,
      ST_SetSRID(ST_MakePoint(lon, lat), 4326),
      raio_km * 1000  -- metros
    );
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION buscar_unidades_proximas(lat float, lon float)
RETURNS TABLE (
  id integer,
  nome varchar,
  tipo varchar,
  endereco text,
  telefone varchar,
  latitude float,
  longitude float,
  distancia_km numeric -- Alterado para numeric para melhor precisão decimal
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
    -- Converte a distância para KM e arredonda para 2 casas decimais
    ROUND(
      (ST_Distance(ua.localizacao, ST_SetSRID(ST_MakePoint(lon, lat), 4326)) / 1000)::numeric, 
      2
    ) as distancia_km
  FROM
    public.unidades_apoio AS ua
  ORDER BY
    -- A ordenação continua usando o operador <-> para máxima performance
    ua.localizacao <-> ST_SetSRID(ST_MakePoint(lon, lat), 4326);
END;
$$ LANGUAGE plpgsql;