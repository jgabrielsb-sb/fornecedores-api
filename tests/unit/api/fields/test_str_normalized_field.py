import pytest
from pydantic import BaseModel, ValidationError

from fornecedores_app.api.fields.codigo_ibge_field import CodigoIBGEField, validate_codigo_ibge
from fornecedores_app.api.fields.str_normalized_field import StrNormalizedField, normalize_str

pytestmark = pytest.mark.unit

municipios = [
    ("Alta Floresta D'Oeste", "ALTA FLORESTA D OESTE"),
    ("Alto Alegre dos Parecis", "ALTO ALEGRE DOS PARECIS"),
    ("Alto Paraíso", "ALTO PARAISO"),
    ("Alvorada D'Oeste", "ALVORADA D OESTE"),
    ("Ariquemes", "ARIQUEMES"),
    ("Buritis", "BURITIS"),
    ("Cabixi", "CABIXI"),
    ("Cacaulândia", "CACAULANDIA"),
    ("Cacoal", "CACOAL"),
    ("Campo Novo de Rondônia", "CAMPO NOVO DE RONDONIA"),
    ("Candeias do Jamari", "CANDEIAS DO JAMARI"),
    ("Castanheiras", "CASTANHEIRAS"),
    ("Cerejeiras", "CEREJEIRAS"),
    ("Chupinguaia", "CHUPINGUAIA"),
    ("Colorado do Oeste", "COLORADO DO OESTE"),
    ("Corumbiara", "CORUMBIARA"),
    ("Costa Marques", "COSTA MARQUES"),
    ("Cujubim", "CUJUBIM"),
    ("Espigão D'Oeste", "ESPIGAO D OESTE"),
    ("Governador Jorge Teixeira", "GOVERNADOR JORGE TEIXEIRA"),
    ("Guajará-Mirim", "GUAJARA MIRIM"),
    ("Itapuã do Oeste", "ITAPUA DO OESTE"),
    ("Jaru", "JARU"),
    ("Ji-Paraná", "JI PARANA"),
    ("Machadinho D'Oeste", "MACHADINHO D OESTE"),
    ("Ministro Andreazza", "MINISTRO ANDREAZZA"),
    ("Mirante da Serra", "MIRANTE DA SERRA"),
    ("Monte Negro", "MONTE NEGRO"),
    ("Nova Brasilândia D'Oeste", "NOVA BRASILANDIA D OESTE"),
    ("Nova Mamoré", "NOVA MAMORE"),
    ("Nova União", "NOVA UNIAO"),
    ("Novo Horizonte do Oeste", "NOVO HORIZONTE DO OESTE"),
    ("Ouro Preto do Oeste", "OURO PRETO DO OESTE"),
    ("Parecis", "PARECIS"),
    ("Pimenta Bueno", "PIMENTA BUENO"),
    ("Pimenteiras do Oeste", "PIMENTEIRAS DO OESTE"),
    ("Porto Velho", "PORTO VELHO"),
    ("Presidente Médici", "PRESIDENTE MEDICI"),
    ("Primavera de Rondônia", "PRIMAVERA DE RONDONIA"),
    ("Rio Crespo", "RIO CRESPO"),
    ("Rolim de Moura", "ROLIM DE MOURA"),
]

@pytest.mark.parametrize("raw_str, expected_normalized_str", municipios)
def test_str_normalized_field_normalizes_to_digits(raw_str: str, expected_normalized_str: str):
    assert normalize_str(raw_str) == expected_normalized_str
