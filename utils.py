from shapely import wkb

def wkb_to_coords(wkb_hex):
    try:
        point = wkb.loads(bytes.fromhex(wkb_hex))
        return point.x, point.y  # x = longitude, y = latitude
    except Exception as e:
        print(f"Erro ao converter WKB: {wkb_hex} -> {e}")
        return None, None 