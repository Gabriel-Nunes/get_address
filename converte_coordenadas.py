import re

def converter_coord_dms_para_decimal(coordenada_dms):
    """Converte as coordenadas do padrão '-5-02-4.9, -38-00-32.8" (extratos VIVO)
    para o formato '-4.965305555555556, -37.99088888888889'

    >>> converter_coord_dms_para_decimal('-5-02-4.9')
    -4.965305555555556
    """
    graus, minutos, segundos = (float(a) for a in re.search(r"(-?\d+).(\d+).([\d\.]+)", coordenada_dms).groups())
    decimal = graus + minutos/60 + segundos/3600
    return decimal

# Exemplo de uso
coord_dms_lat = "-5-02-4.9"
coord_dms_lon = "-38-00-32.8"

coord_decimal_lat = converter_coord_dms_para_decimal(coord_dms_lat)
coord_decimal_lon = converter_coord_dms_para_decimal(coord_dms_lon)

print(f"Coordenadas decimais: {coord_decimal_lat}, {coord_decimal_lon}")