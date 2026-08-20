"""
Database of Store Codes and Names for HACKBEN.
"""

STORE_DB = {
    "518": "SENTRA PANCORAN",
    "521": "CILANDAK MALL",
    "522": "KALIBATA MAL",
    "527": "RUKO TEBET",
    "721": "RUKO KREO",
    "538": "PEJATEN VILLAGE",
    "C44": "HOKBEN KITCHEN FATMAWATI CILANDAK",
    "C54": "HOKBEN KITCHEN PASAR RUMPUT SETIABUDI",
    "C55": "HOKBEN KITCHEN KEBAYORAN LAMA",
    "C56": "HOKBEN KITCHEN CILEDUG LARANGAN",
    "C57": "HOKBEN KITCHEN PETUKANGAN UTARA",
    "C60": "HOKBEN KITCHEN BANGKA MAMPANG",
    "C61": "HOKBEN KITCHEN CONDET BALAI KAMBANG",
    "C66": "HOKBEN KITCHEN RADIO DALAM",
}

def get_store_name(code: str) -> str | None:
    """Retrieve store name by code (case-insensitive)."""
    return STORE_DB.get(code.strip().upper())

def search_stores(keyword: str) -> dict[str, str]:
    """Search stores by keyword in code or name."""
    kw = keyword.strip().upper()
    return {k: v for k, v in STORE_DB.items() if kw in k.upper() or kw in v.upper()}
