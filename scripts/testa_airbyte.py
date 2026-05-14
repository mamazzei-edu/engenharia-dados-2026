import boto3
 
client = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="minioadmin",
    aws_secret_access_key="minioadmin123",
    region_name="us-east-1",
)
 
response = client.list_objects_v2(Bucket="bronze", Prefix="airbyte/")
objetos = response.get("Contents", [])
 
print(f"Objetos criados pelo Airbyte no bucket bronze: {len(objetos)}")
for obj in objetos:
    tamanho_kb = obj["Size"] / 1024
    print(f"  📄 {obj['Key']}  ({tamanho_kb:.1f} KB)")
