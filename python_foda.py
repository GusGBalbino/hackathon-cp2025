import re
import pyproj

def converter_coordenadas_e_gerar_sql(arquivo_entrada, arquivo_saida):
    """
    Lê um arquivo SQL com coordenadas UTM, converte para Lat/Lon
    e gera um novo arquivo SQL compatível com a tabela 'unidades_apoio'.
    """
    # Define os sistemas de coordenadas:
    # Origem: SAD69 / UTM zone 23S (usado no arquivo original)
    crs_origem = pyproj.CRS("EPSG:31983") 
    # Destino: WGS 84 (padrão de Latitude/Longitude)
    crs_destino = pyproj.CRS("EPSG:4326")
    
    # Cria o transformador para converter de um sistema para o outro
    transformer = pyproj.Transformer.from_crs(crs_origem, crs_destino, always_xy=True)

    # Padrão de expressão regular para extrair os dados de cada linha INSERT
    # Captura: tipo, endereco, telefone, coord_x, coord_y
    padrao = re.compile(
        r"INSERT INTO delegacias \(.*?\) VALUES \('(.*?)', '(.*?)', (.*?|NULL), ST_SetSRID\(ST_MakePoint\((.*?), (.*?)\), \d+\)\);"
    )

    try:
        with open(arquivo_entrada, 'r', encoding='utf-8') as f_in, \
             open(arquivo_saida, 'w', encoding='utf-8') as f_out:
            
            f_out.write("-- Script SQL convertido para a tabela 'unidades_apoio'\n")
            f_out.write("-- Coordenadas convertidas de EPSG:31983 para EPSG:4326 (Lat/Lon)\n\n")

            for linha in f_in:
                match = padrao.match(linha.strip())
                if match:
                    tipo, endereco, telefone, x_utm, y_utm = match.groups()
                    
                    # Limpa e prepara os dados
                    tipo = tipo.strip().replace("'", "''")
                    endereco = endereco.strip().replace("'", "''")
                    
                    # Converte as coordenadas
                    try:
                        lon, lat = transformer.transform(float(x_utm), float(y_utm))
                    except ValueError:
                        print(f"Não foi possível converter coordenadas na linha: {linha.strip()}")
                        continue

                    # Gera o nome da unidade
                    nome_unidade = f"{tipo} - {endereco}"
                    
                    # Formata o WKT para a coluna 'localizacao'
                    localizacao_wkt = f"POINT({lon} {lat})"
                    
                    # Formata o telefone (se for NULL, mantém, senão, coloca entre aspas)
                    telefone_formatado = f"'{telefone}'" if telefone != 'NULL' else 'NULL'

                    # Monta a nova instrução INSERT
                    nova_linha = (
                        f"INSERT INTO unidades_apoio (nome, tipo, endereco, telefone, localizacao) "
                        f"VALUES ('{nome_unidade}', '{tipo}', '{endereco}', {telefone_formatado}, '{localizacao_wkt}');\n"
                    )
                    
                    f_out.write(nova_linha)

        print(f"Conversão concluída! Arquivo gerado: '{arquivo_saida}'")

    except FileNotFoundError:
        print(f"Erro: O arquivo de entrada '{arquivo_entrada}' não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

# --- Execução ---
if __name__ == "__main__":
    # Nome do arquivo SQL original que você enviou
    arquivo_sql_original = "delegacias_df.sql"
    # Nome do novo arquivo que será gerado
    arquivo_sql_convertido = "unidades_apoio_convertido.sql"
    
    converter_coordenadas_e_gerar_sql(arquivo_sql_original, arquivo_sql_convertido)