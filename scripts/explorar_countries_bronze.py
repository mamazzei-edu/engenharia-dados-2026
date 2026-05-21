"""
Exploração dos dados da REST Countries API na camada Bronze.
Demonstra como ler dados Parquet diretamente do MinIO com Pandas.
"""
 
import pandas as pd
import boto3
import io
 
# Configurar cliente S3
client = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="minioadmin",
    aws_secret_access_key="minioadmin123",
    region_name="us-east-1",
)
 
# Listar os arquivos Parquet criados pelo dlt
print("Arquivos criados pelo pipeline dlt:")
response = client.list_objects_v2(Bucket="bronze", Prefix="rest_countries/")
arquivos_parquet = [
    obj["Key"] for obj in response.get("Contents", [])
    if obj["Key"].endswith(".parquet")
]
 
for arq in arquivos_parquet:
    tamanho_kb = client.head_object(Bucket="bronze", Key=arq)["ContentLength"] / 1024
    print(f"  📄 {arq}  ({tamanho_kb:.1f} KB)")

# Ler o arquivo principal de países
if arquivos_parquet:
    chave_principal = next(
        (k for k in arquivos_parquet if "countries" in k.lower()), arquivos_parquet[0]
    )
    obj = client.get_object(Bucket="bronze", Key=chave_principal)
    df = pd.read_parquet(io.BytesIO(obj["Body"].read()))
 
    print(f"\nShape do dataset: {df.shape}")
    print(f"\nColunas disponíveis:\n{list(df.columns)}")
    print(f"\nDistribuição por região:")
    print(df["region"].value_counts())
    print(f"\nTop 10 países por população:")
    print(
        df[["name__common", "population", "region"]]
        .sort_values("population", ascending=False)
        .head(10)
        .to_string(index=False)
    )

