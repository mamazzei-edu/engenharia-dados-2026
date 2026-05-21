# scripts/reingerir_com_particionamento.py
"""
Demonstração do uso da classe BronzeWriter para ingestão padronizada.
Reingestão dos dados de Countries e Pokémon com particionamento correto.
"""
 
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
 
import requests
import pandas as pd
import time
from datetime import datetime, timezone
from bronze_writer import BronzeWriter
 
writer = BronzeWriter()
 
# ── 1. Reingestão da REST Countries API ──────────────────────────────────────
print("\n" + "─" * 55)
print("  Reingestão: REST Countries API → Bronze (particionado)")
print("─" * 55)
 
resposta = requests.get(
    "https://restcountries.com/v3.1/all",
    params={"fields": "name,cca2,region,continents,capital,languages,currencies,population,area,latlng"},
    timeout=30,
)
resposta.raise_for_status()


# Normalizar o campo 'name' (é um objeto aninhado)
paises_raw = resposta.json()
paises_normalizados = []
for p in paises_raw:
    paises_normalizados.append({
        "cca2": p.get("cca2"),
        "nome_comum": p.get("name", {}).get("common"),
        "nome_oficial": p.get("name", {}).get("official"),
        "regiao": p.get("region"),
        "continentes": p.get("continents"),
        "moedas": p.get("currencies"),
        "populacao": p.get("population"),
        "area_km2": p.get("area"),
        "latlng" : p.get("latlng"),
        "capital": p.get("capital", [None])[0] if p.get("capital") else None,
    })

df_countries = pd.DataFrame(paises_normalizados)
 
resultado_countries = writer.gravar(
    df=df_countries,
    sistema_origem="restcountries_api",
    entidade="countries",
    versao_schema="1.0",
)
# Registrar manifesto
writer.registrar_manifesto({
    "pipeline": "rest_countries_bronze",
    "execucao_em": datetime.now(timezone.utc).isoformat(),
    "resultado": resultado_countries,
})

print(f"  ✅ {resultado_countries['registros']} países gravados")
print(f"  📍 {resultado_countries['caminho_objeto']}")
 
# ── 2. Reingestão da PokeAPI (primeiros 50 pokémons) ─────────────────────────
print("\n" + "─" * 55)
print("  Reingestão: PokeAPI → Bronze (particionado)")
print("─" * 55)
 
BASE_URL = "https://pokeapi.co/api/v2"

pokemon_lista = []

# Buscar lista dos primeiros 50 pokémons
resp_lista = requests.get(f"{BASE_URL}/pokemon?limit=50&offset=0", timeout=15)
resp_lista.raise_for_status()
 
for i, item in enumerate(resp_lista.json()["results"]):
    resp_detalhe = requests.get(item["url"], timeout=10)
    resp_detalhe.raise_for_status()
    d = resp_detalhe.json()
 
    pokemon_lista.append({
        "id": d["id"],
        "nome": d["name"],
        "altura_dm": d["height"],
        "peso_hg": d["weight"],
        "experiencia_base": d.get("base_experience"),
        "tipo_primario": d["types"][0]["type"]["name"] if d["types"] else None,
        "tipo_secundario": d["types"][1]["type"]["name"] if len(d["types"]) > 1 else None,
        "hp_base": next((s["base_stat"] for s in d["stats"] if s["stat"]["name"] == "hp"), None),
        "ataque_base": next((s["base_stat"] for s in d["stats"] if s["stat"]["name"] == "attack"), None),
        "defesa_base": next((s["base_stat"] for s in d["stats"] if s["stat"]["name"] == "defense"), None),
        "sprite_url": d.get("sprites", {}).get("front_default"),
    })
 
    if (i + 1) % 10 == 0:
        print(f"  Extraídos: {i + 1}/50 pokémons...")
    time.sleep(0.1)
 
df_pokemon = pd.DataFrame(pokemon_lista)
 
resultado_pokemon = writer.gravar(
    df=df_pokemon,
    sistema_origem="pokeapi",
    entidade="pokemon",
    versao_schema="1.0",
)
 
writer.registrar_manifesto({
    "pipeline": "pokeapi_bronze",
    "execucao_em": datetime.now(timezone.utc).isoformat(),
    "resultado": resultado_pokemon,
})
 
print(f"  ✅ {resultado_pokemon['registros']} pokémons gravados")
print(f"  📍 {resultado_pokemon['caminho_objeto']}")
 
# ── 3. Relatório final ────────────────────────────────────────────────────────
print("\n" + "=" * 55)
print("  RELATÓRIO FINAL — CAMADA BRONZE")
print("=" * 55)
 
for sistema, entidade in [("restcountries_api", "countries"), ("pokeapi", "pokemon")]:
    particoes = writer.listar_particoes(sistema, entidade)
    total_bytes = sum(p["tamanho_bytes"] for p in particoes)
    print(f"\n  [{sistema}/{entidade}]")
    print(f"    Arquivos:  {len(particoes)}")
    print(f"    Tamanho:   {total_bytes / 1024:.1f} KB")
    for p in particoes:
        print(f"    📄 {p['caminho']}")
 
print("\n  ✅ Camada Bronze organizada com particionamento correto!")
print("  Acesse: http://localhost:9001/browser/bronze")
