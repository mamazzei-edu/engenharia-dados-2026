"""Script de configuração inicial do MINIO
Cria os buckets correspondentes às camadas da arquitetura Medalion
- Bronze
- Silver
- Gold
"""
import boto3
from botocore.exceptions import ClientError

MINIO_ENDPOINT = "http://localhost:9000"
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin123"

BUCKETS = [
    {
        "name" : "bronze",
        "description" : "Dados brutos ingeridos das fontes originais, sem transformação"
    },
    {
        "name" : "silver",
        "description" : "Dados limpos, padronizados e integrados"
    },
    {
        "name" : "gold",
        "description" : "Dados curados e modelados para Analytics e Machine Learning"
    },
]

def create_s3_client():
    """Cria e retorna um cliente S3 configurado para o MinIO Local"""
    return boto3.client(
        "s3",
        endpoint_url = MINIO_ENDPOINT,
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key = MINIO_SECRET_KEY,
        region_name = "us-east-1"
    )


def create_bucket(client, bucket_name: str) -> bool:
    """Cria um bucket no MinIO - Retorna True se criado com sucesso, false se já existia"""
    try:
        client.create_bucket(Bucket = bucket_name)
        return True
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "BucketAlreadyOwnedByYou":
            return False
        raise # Relança demais erros

def list_buckets(client) -> list:
    """Retorna a lista de buckets existentes no MinIO"""
    response = client.list_buckets()
    return [b["Name"] for b in response.get("Buckets", [])]

def main():
    print("=" * 55)
    print(" Configuração do Data Lake Local (MinIO)")
    print(" Arquitetura Medallion - Bronze / Silver / Gold")
    print("=" * 55)
    client = create_s3_client()
    for bucket in BUCKETS:
        name = bucket["name"]
        created = create_bucket(client,name)
        status = "\u2705 Criado" if created else  "\u26A0 Já existia"
        print(f"\n [{name.upper()} {status}]")

    print(f"Descrição: {bucket['description']}")
    print("\n" + "=" * 55)
    print("Buckets disponíveis no MinIO:")
    for b in list_buckets(client):
        print(f"\U0001FA9F  {b}")

    print("=" * 55)
    print("\n \u2705 Data lake local configurado com sucesso!")
    print("Acesse o console em: http://localhost:9001")


if __name__ == "__main__":
    main()
