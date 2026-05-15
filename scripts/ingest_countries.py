"""
Pipeline de ingestão da REST Countries API para a camada Bronze.
 
Fonte: https://restcountries.com/v3.1/all
Destino: MinIO (bucket bronze) — formato Parquet com compressão Snappy
Tipo de dado: Cadastral estático (dimensão geográfica)
 
A REST Countries API retorna um array JSON com ~250 objetos,
cada um representando um país com dezenas de atributos aninhados.
O dlt normaliza automaticamente esses objetos aninhados em tabelas
relacionais (ex: languages, currencies, translations).
"""
 
import dlt
import requests
import logging
from datetime import datetime, timezone
from typing import Iterator
 
# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)
 
# ── Configuração do destino MinIO ─────────────────────────────────────────────
# O dlt usa variáveis de ambiente para configurar credenciais.
# Para o ambiente local, podemos passá-las diretamente no código.
import os
os.environ["DESTINATION__FILESYSTEM__BUCKET_URL"] = "s3://bronze"
os.environ["DESTINATION__FILESYSTEM__CREDENTIALS__AWS_ACCESS_KEY_ID"] = "minioadmin"
os.environ["DESTINATION__FILESYSTEM__CREDENTIALS__AWS_SECRET_ACCESS_KEY"] = "minioadmin123"
os.environ["DESTINATION__FILESYSTEM__CREDENTIALS__ENDPOINT_URL"] = "http://localhost:9000"
os.environ["DESTINATION__FILESYSTEM__CREDENTIALS__REGION_NAME"] = "us-east-1"

# URL da API
API_URL = "https://restcountries.com/v3.1/all"

 
# Campos selecionados para a ingestão (evitar sobrecarga com campos irrelevantes)
CAMPOS_SELECIONADOS = [
    "name", "cca2",
    "region", "continents",
    "capital", "languages", "currencies",
    "population", "area", "latlng"
]
  
 
@dlt.resource(
    name="countries",
    write_disposition="replace",  # Substitui os dados a cada execução (dado cadastral)
    primary_key="cca2",           # Código ISO 3166-1 alpha-2 como chave primária
)
def extrair_paises() -> Iterator[dict]:
    """
    Extrai todos os países da REST Countries API.
    O decorador @dlt.resource transforma esta função geradora
    em um recurso gerenciado pelo pipeline dlt.
    """
    logger.info(f"Iniciando extração de: {API_URL}")
    timestamp_ingestao = datetime.now(timezone.utc).isoformat()
 
    resposta = requests.get(
        API_URL,
        params={"fields": ",".join(CAMPOS_SELECIONADOS)},
        timeout=30,
    )
    resposta.raise_for_status()
 
    paises = resposta.json()
    logger.info(f"Total de países recebidos da API: {len(paises)}")
 
    for pais in paises:
        # Adicionar metadados de rastreabilidade (prática obrigatória na camada Bronze)
        pais["_fonte"] = "restcountries_v3"
        pais["_ingerido_em"] = timestamp_ingestao
        pais["_versao_api"] = "v3.1"
        yield pais

def executar_pipeline():
    """Configura e executa o pipeline dlt para a REST Countries API."""
 
    # Criar o pipeline dlt
    pipeline = dlt.pipeline(
        pipeline_name="rest_countries_bronze",
        destination="filesystem",
        dataset_name="rest_countries",  # Subdiretório dentro do bucket bronze
    )
 
    logger.info("Iniciando pipeline: REST Countries → MinIO Bronze")
    inicio = datetime.now()
 
    # Executar a carga
    info = pipeline.run(
        extrair_paises(),
        loader_file_format="parquet",  # Formato Parquet com Snappy (padrão do dlt)
    )
 
    duracao = (datetime.now() - inicio).total_seconds()
 
    # Exibir o relatório de execução
    print("\n" + "=" * 60)
    print("  RELATÓRIO DE EXECUÇÃO — REST Countries API")
    print("=" * 60)
    print(f"  Status:        {'✅ Sucesso' if not info.has_failed_jobs else '❌ Falha'}")
    print(f"  Duração:       {duracao:.2f}s")
    print(f"  Destino:       s3://bronze/rest_countries/")
    print(f"  Formato:       Parquet + Snappy")
    print()
    print("  Detalhes da carga:")
    print(info)
    print("=" * 60)
 
    return info
 
 
if __name__ == "__main__":
    executar_pipeline()
