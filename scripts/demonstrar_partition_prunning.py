"""
Demonstração do partition pruning: leitura eficiente de dados
particionados sem carregar todas as partições disponíveis.
"""
 
import pandas as pd
import boto3
import io
from datetime import datetime
 
client = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="minioadmin",
    aws_secret_access_key="minioadmin123",
    region_name="us-east-1",
)
 
def ler_particao_especifica(
    sistema: str,
    entidade: str,
    ano: int,
    mes: int,
    dia: int,
) -> pd.DataFrame:
    """
    Lê apenas a partição correspondente à data especificada.
    Ignora todas as outras partições — isso é partition pruning.
    """
    dia = dia + 1
    prefixo = f"{sistema}/{entidade}/ano={ano}/mes={mes:02d}/dia={dia:02d}/"
 
    response = client.list_objects_v2(Bucket="bronze", Prefix=prefixo)
    arquivos = [
        obj["Key"] for obj in response.get("Contents", [])
        if obj["Key"].endswith(".parquet")
    ]
 
    if not arquivos:
        print(f"  ⚠️  Nenhum dado encontrado para {prefixo}")
        return pd.DataFrame()
 
    # Ler apenas os arquivos da partição solicitada
    frames = []
    for chave in arquivos:
        obj = client.get_object(Bucket="bronze", Key=chave)
        frames.append(pd.read_parquet(io.BytesIO(obj["Body"].read())))
 
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
 
 
# Ler apenas a partição de hoje
hoje = datetime.now()
print(f"Lendo partição de hoje ({hoje.strftime('%Y-%m-%d')}):\n")
 
df_countries_hoje = ler_particao_especifica(
    "restcountries_api", "countries",
    hoje.year, hoje.month, hoje.day
)
 
if not df_countries_hoje.empty:
    print(f"  ✅ Countries: {len(df_countries_hoje)} registros carregados")
    print(f"  Colunas de metadados: {[c for c in df_countries_hoje.columns if c.startswith('_')]}")
    print(f"\n  Amostra dos dados:")
    print(
        df_countries_hoje[["nome_comum", "regiao", "populacao", "_ingerido_em"]]
        .head(5)
        .to_string(index=False)
    )
 
print("\n💡 Em um Data Lake com anos de dados históricos, a leitura")
print("   com partition pruning evita varrer milhares de arquivos")
print("   desnecessários, reduzindo custo e tempo de processamento.")
