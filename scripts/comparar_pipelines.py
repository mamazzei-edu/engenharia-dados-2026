# scripts/comparar_pipelines.py
"""
Compara os dados ingeridos pelos dois pipelines (Countries e PokeAPI)
e demonstra as diferenças de estrutura entre dados cadastrais
e dados com relacionamentos complexos.
"""
 
import pandas as pd
import boto3
import io
 
client = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="minioadmin",
    aws_secret_access_key="minioadmin123",
    region_name="us-east-1",
)
 
def ler_parquet_do_minio(bucket: str, prefixo: str) -> pd.DataFrame:
    """Lê o primeiro arquivo Parquet encontrado no prefixo especificado."""
    response = client.list_objects_v2(Bucket=bucket, Prefix=prefixo)
    arquivos = [
        obj["Key"] for obj in response.get("Contents", [])
        if obj["Key"].endswith(".parquet")
    ]
    if not arquivos:
        raise FileNotFoundError(f"Nenhum arquivo Parquet em {bucket}/{prefixo}")
 
    obj = client.get_object(Bucket=bucket, Key=arquivos[0])
    return pd.read_parquet(io.BytesIO(obj["Body"].read()))


print("=" * 65)
print("  COMPARATIVO DOS DADOS INGERIDOS NA CAMADA BRONZE")
print("=" * 65)
 
# REST Countries
df_countries = ler_parquet_do_minio("bronze", "rest_countries/")
print(f"\n🌍 REST Countries API")
print(f"   Registros: {len(df_countries):,}")
print(f"   Colunas:   {len(df_countries.columns)}")
print(f"   Regiões:   {df_countries['region'].nunique()} únicas")
print(f"   Metadados: {[c for c in df_countries.columns if c.startswith('_')]}")

# PokeAPI
df_pokemon = ler_parquet_do_minio("bronze", "pokeapi/")
print(f"\n🎮 PokeAPI")
print(f"   Registros: {len(df_pokemon):,}")
print(f"   Colunas:   {len(df_pokemon.columns)}")
print(f"   Tipos únicos: {df_pokemon['tipo_primario'].nunique()}")
print(f"   Metadados: {[c for c in df_pokemon.columns if c.startswith('_')]}")

print(f"\n{'─' * 65}")
print("  Distribuição de pokémons por tipo primário:")
print(df_pokemon["tipo_primario"].value_counts().head(10).to_string())
print("=" * 65)
