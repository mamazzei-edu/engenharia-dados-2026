# Aula 1 — Atividades Práticas
## Engenharia de Dados com Ferramentas Open Source

**Curso:** Engenharia de Dados com Ferramentas Open Source
**Aula:** 1 — Fundamentos da Engenharia de Dados e Arquitetura de Repositórios
**Duração das Atividades:** 2 horas
**Pré-requisitos:** Conhecimento básico de Python e linha de comando (terminal)

---

## Visão Geral das Atividades

As três atividades práticas desta aula formam uma sequência progressiva e interdependente. A **Atividade 1** prepara o ambiente completo que será utilizado ao longo de todo o curso. A **Atividade 2** coloca esse ambiente em operação, subindo o serviço de armazenamento de objetos MinIO que simulará o Data Lake local. A **Atividade 3** introduz os formatos de arquivo fundamentais para engenharia de dados, demonstrando na prática por que o formato Parquet é o padrão da indústria para repositórios analíticos.

| Atividade | Tema | Duração Estimada | Ferramentas |
|---|---|---|---|
| 1 | Configuração do Ambiente de Desenvolvimento | 40 min | Docker, Docker Compose, Python 3.11+, Git |
| 2 | Subida e Exploração do MinIO (Data Lake Local) | 30 min | Docker Compose, MinIO, Python (`boto3`) |
| 3 | Comparação de Formatos de Arquivo: CSV, JSON e Parquet | 50 min | Python, Pandas, PyArrow, Jupyter Notebook |

---

## Atividade 1 — Configuração do Ambiente de Desenvolvimento

### Objetivo

Preparar o ambiente de desenvolvimento local que será utilizado ao longo de todo o curso, garantindo que todas as ferramentas necessárias estejam instaladas, configuradas e funcionando corretamente. Um ambiente bem configurado é o alicerce de qualquer projeto de engenharia de dados.

### Contexto

Diferentemente de ambientes de produção em nuvem, o ambiente local do curso utiliza **Docker** e **Docker Compose** para isolar e orquestrar os serviços necessários (MinIO, bancos de dados, ferramentas de processamento). Essa abordagem garante reprodutibilidade: o ambiente funcionará da mesma forma em qualquer máquina, independentemente do sistema operacional do aluno. Ao final, os arquivos produzidos e as imagens poderão ser utilizados como base para ambientes de produção com o uso de Kubernetes.

### Pré-requisitos de Hardware

O ambiente mínimo recomendado para executar todas as ferramentas do curso é de 8 GB de RAM e 20 GB de espaço em disco disponível. Ambientes com 16 GB de RAM proporcionarão uma experiência mais fluida, especialmente nas aulas de Apache Spark.

---

### Passo 1 — Instalação do Docker e Docker Compose

O Docker é a plataforma de conteinerização que permite executar serviços complexos como MinIO e Airflow com um único comando, sem necessidade de instalação manual de dependências.


Instale o [Docker Desktop para Windows](https://www.docker.com/products/docker-desktop/), que requer o WSL 2 (Windows Subsystem for Linux) habilitado. Siga as instruções do instalador.

**Verificação:**

```cmd
# Verificar a versão do Docker
docker --version
# Saída esperada: Docker version 24.x.x, build ...

# Verificar o Docker Compose
docker compose version
# Saída esperada: Docker Compose version v2.x.x
```

---

### Passo 2 — Instalação do Python 3.11+ e Gerenciador de Pacotes

O Python é a linguagem principal do curso. Recomenda-se fortemente o uso de ambientes virtuais para isolar as dependências de cada projeto.

```cmd
python --version
```

### Se não estiver instalado, será oferecida a opção de instalar da Microsoft Store que é a forma mais simples de efetuar essa instalação.

---

### Passo 3 — Instalação do Git e Configuração Inicial

O Git será utilizado para versionar todos os scripts e configurações desenvolvidos ao longo do curso.

Faça o download do instalador a partir do seguinte link:  https://git-scm.com/install/windows

---

### Passo 4 — Criação da Estrutura de Diretórios do Projeto

Toda a estrutura do curso seguirá uma organização padronizada que reflete a arquitetura Medallion. Execute os comandos abaixo para criar o projeto base:

```cmd
PS C:\ mkdir ~/engenharia-dados
PS C:\ cd ~/engenharia-dados
PS C:\Users\mamaz\engenharia-dados> mkdir notebooks, scripts, dbt_project, airflow/dags, docker, data/bronze, data/silver, data/gold
PS C:\Users\mamaz\engenharia-dados> echo "" > notebooks/README.md
PS C:\Users\mamaz\engenharia-dados> echo "" > scripts/README.md
PS C:\Users\mamaz\engenharia-dados> echo "" > dbt_project/README.md
PS C:\Users\mamaz\engenharia-dados> echo "" > airflow/dags/README.md
PS C:\Users\mamaz\engenharia-dados> echo "" > docker/README.md
PS C:\Users\mamaz\engenharia-dados> echo "" > data/bronze/README.md
PS C:\Users\mamaz\engenharia-dados> echo "" > data/silver/README.md
PS C:\Users\mamaz\engenharia-dados> echo "" > data/gold/README.md
PS C:\Users\mamaz\engenharia-dados> python -m venv .venv
PS C:\Users\mamaz\engenharia-dados> Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
PS C:\Users\mamaz\engenharia-dados> .\.venv\Scripts\Activate.ps1
PS C:\Users\mamaz\engenharia-dados> pip install pandas pyarrow boto3 jupyter notebook
```
---

### Passo 5 — Inicialização do Repositório Git

Crie um arquivo .gitignore com o seguinte conteúdo na pasta engenharia-dados:

Abra o arquivo utilizando o vscode:
```cmd
PS C:\Users\mamaz\engenharia-dados> code .gitignore
```

Copie o seguinte conteúdo:

```cmd
.venv
__pycache__/
*.pyc

.ipynb_checkpoints

data/

.env
*.log
```
Nosso primeiro commit:

```cmd
PS C:\Users\mamaz\engenharia-dados> git init
PS C:\Users\mamaz\engenharia-dados> git config user.name "Seu Nome"
PS C:\Users\mamaz\engenharia-dados> git config user.email "Seu email"
PS C:\Users\mamaz\engenharia-dados> git config --list
PS C:\Users\mamaz\engenharia-dados> git add .
PS C:\Users\mamaz\engenharia-dados> git commit -m "feat: estrutura inicial do projeto do curso"
```

---

### Verificação Final da Atividade 1

Execute o script abaixo para confirmar que o ambiente está corretamente configurado (arquivo scripts/teste_instalacao_python.py):

```python
import sys
import subprocess

checks = {
    "Python 3.11+": sys.version_info >= (3, 11),
    "pandas": False,
    "pyarrow": False,
    "boto3": False,
    "jupyter": False,
}

for lib in ["pandas", "pyarrow", "boto3", "jupyter"]:
    try:
        __import__(lib)
        checks[lib] = True
    except ImportError:
        pass

print("=== Verificação do Ambiente ===")
for item, status in checks.items():
    icon = "✅" if status else "❌"
    print(f"  {icon}  {item}")

all_ok = all(checks.values())
print()
if all_ok:
    print("🎉 Ambiente configurado com sucesso! Pronto para a Atividade 2.")
else:
    print("⚠️  Alguns itens precisam de atenção. Revise os passos acima.")
```

Para executar:

```cmd
PS C:\Users\mamaz\engenharia-dados> python .\scripts\teste_instalacao_python.py
```


---

## Atividade 2 — Subida e Exploração do MinIO (Data Lake Local)

### Objetivo

Configurar e inicializar o **MinIO**, um servidor de armazenamento de objetos de alto desempenho compatível com a API do Amazon S3. O MinIO será a fundação do Data Lake local utilizado em todas as aulas do curso, simulando o comportamento de serviços de nuvem como Amazon S3, Google Cloud Storage e Azure Blob Storage.

### Contexto

Em ambientes de produção, Data Lakes são construídos sobre serviços de armazenamento de objetos em nuvem (principalmente o Amazon S3). O MinIO replica essa interface localmente, permitindo que todos os scripts e ferramentas desenvolvidos no curso funcionem em produção sem alterações de código — apenas mudando as credenciais e o endpoint de conexão.

A compatibilidade com a API S3 é fundamental: ferramentas como Apache Spark, DuckDB, dbt e Apache Airflow se conectam ao MinIO exatamente da mesma forma que se conectariam ao S3 real.

---

### Passo 1 — Criação do Arquivo Docker Compose para o MinIO

```bash
cd ~/engenharia-dados-curso/docker

cat > docker-compose.yml << 'EOF'
version: "3.9"

services:
  minio:
    image: minio/minio:RELEASE.2024-01-01T00-00-00Z
    container_name: minio-datalake
    ports:
      - "9000:9000"   # API S3 — usada pelos scripts Python
      - "9001:9001"   # Console Web — interface gráfica
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin123
    volumes:
      - minio_data:/data
    command: server /data --console-address ":9001"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 30s
      timeout: 20s
      retries: 3
    restart: unless-stopped

volumes:
  minio_data:
    driver: local
EOF
```

> **Nota de Segurança:** As credenciais `minioadmin` / `minioadmin123` são adequadas apenas para desenvolvimento local. Em ambientes de produção, utilize credenciais fortes e gerencie-as com ferramentas de gerenciamento de segredos como HashiCorp Vault ou AWS Secrets Manager.

---

### Passo 2 — Inicialização do Serviço MinIO

```bash
# Navegar para o diretório docker
cd ~/engenharia-dados-curso/docker

# Iniciar o MinIO em segundo plano
docker compose up -d

# Verificar se o contêiner está rodando
docker compose ps

# Acompanhar os logs de inicialização
docker compose logs minio
```

A saída esperada dos logs deve conter uma linha similar a:

```
MinIO Object Storage Server
Copyright: 2015-2024 MinIO, Inc.
License: GNU AGPLv3
Version: RELEASE.2024-01-01T00-00-00Z

API: http://0.0.0.0:9000
WebUI: http://0.0.0.0:9001
```

---

### Passo 3 — Acesso ao Console Web do MinIO

Abra o navegador e acesse `http://localhost:9001`. Utilize as credenciais configuradas:

- **Usuário:** `minioadmin`
- **Senha:** `minioadmin123`

Após o login, você verá o painel de administração do MinIO. Explore a interface para se familiarizar com os conceitos de **Buckets** (equivalentes a pastas raiz no S3) e **Objects** (os arquivos armazenados).

---

### Passo 4 — Criação dos Buckets da Arquitetura Medallion via Python

Em vez de criar os buckets manualmente pela interface gráfica, utilizaremos Python com a biblioteca `boto3` para automatizar essa tarefa — uma prática essencial em engenharia de dados.

Crie o arquivo `scripts/setup_minio.py`:

```python
# scripts/setup_minio.py
"""
Script de configuração inicial do MinIO.
Cria os buckets correspondentes às camadas da Arquitetura Medallion:
  - bronze: dados brutos, sem transformação
  - silver: dados limpos e conformados
  - gold:   dados curados, prontos para consumo
"""

import boto3
from botocore.exceptions import ClientError

# Configuração da conexão com o MinIO local
MINIO_ENDPOINT = "http://localhost:9000"
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin123"

# Buckets a serem criados (camadas Medallion)
BUCKETS = [
    {
        "name": "bronze",
        "description": "Dados brutos ingeridos das fontes originais, sem transformação."
    },
    {
        "name": "silver",
        "description": "Dados limpos, padronizados e integrados."
    },
    {
        "name": "gold",
        "description": "Dados curados e modelados para Analytics e Machine Learning."
    },
]


def create_s3_client():
    """Cria e retorna um cliente S3 configurado para o MinIO local."""
    return boto3.client(
        "s3",
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
        region_name="us-east-1",  # Valor obrigatório, mas ignorado pelo MinIO
    )


def create_bucket(client, bucket_name: str) -> bool:
    """
    Cria um bucket no MinIO.
    Retorna True se criado com sucesso, False se já existia.
    """
    try:
        client.create_bucket(Bucket=bucket_name)
        return True
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "BucketAlreadyOwnedByYou":
            return False  # Bucket já existe — não é um erro
        raise  # Re-lança erros inesperados


def list_buckets(client) -> list:
    """Retorna a lista de buckets existentes no MinIO."""
    response = client.list_buckets()
    return [b["Name"] for b in response.get("Buckets", [])]


def main():
    print("=" * 55)
    print("  Configuração do Data Lake Local (MinIO)")
    print("  Arquitetura Medallion — Bronze / Silver / Gold")
    print("=" * 55)

    client = create_s3_client()

    for bucket in BUCKETS:
        name = bucket["name"]
        created = create_bucket(client, name)
        status = "✅ Criado" if created else "⚠️  Já existia"
        print(f"\n  [{name.upper()}]  {status}")
        print(f"  Descrição: {bucket['description']}")

    print("\n" + "=" * 55)
    print("  Buckets disponíveis no MinIO:")
    for b in list_buckets(client):
        print(f"    🪣  {b}")
    print("=" * 55)
    print("\n  ✅ Data Lake local configurado com sucesso!")
    print("  Acesse o console em: http://localhost:9001")


if __name__ == "__main__":
    main()
```

Execute o script:

```bash
cd ~/engenharia-dados-curso
source .venv/bin/activate
python scripts/setup_minio.py
```

A saída esperada é:

```
=======================================================
  Configuração do Data Lake Local (MinIO)
  Arquitetura Medallion — Bronze / Silver / Gold
=======================================================

  [BRONZE]  ✅ Criado
  Descrição: Dados brutos ingeridos das fontes originais, sem transformação.

  [SILVER]  ✅ Criado
  Descrição: Dados limpos, padronizados e integrados.

  [GOLD]  ✅ Criado
  Descrição: Dados curados e modelados para Analytics e Machine Learning.

=======================================================
  Buckets disponíveis no MinIO:
    🪣  bronze
    🪣  silver
    🪣  gold
=======================================================

  ✅ Data Lake local configurado com sucesso!
```

---

### Passo 5 — Teste de Upload e Download de Arquivo

Valide que o MinIO está funcionando corretamente fazendo upload e download de um arquivo de teste:

```python
# scripts/test_minio_connection.py
"""
Teste de conectividade com o MinIO.
Realiza upload de um arquivo de teste, verifica sua existência
e faz o download para confirmar a integridade.
"""

import boto3
import json
from datetime import datetime, timezone

MINIO_ENDPOINT = "http://localhost:9000"
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin123"

client = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
    region_name="us-east-1",
)

# Conteúdo do arquivo de teste
test_data = {
    "mensagem": "Teste de conectividade com o MinIO",
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "camada": "bronze",
    "status": "ok",
}

# Definir o caminho do objeto no bucket (particionamento por data)
hoje = datetime.now()
object_key = f"_testes/ano={hoje.year}/mes={hoje.month:02d}/dia={hoje.day:02d}/teste_conexao.json"

# Upload
print("📤 Fazendo upload do arquivo de teste...")
client.put_object(
    Bucket="bronze",
    Key=object_key,
    Body=json.dumps(test_data, indent=2, ensure_ascii=False),
    ContentType="application/json",
)
print(f"   ✅ Arquivo enviado para: bronze/{object_key}")

# Verificar existência
response = client.head_object(Bucket="bronze", Key=object_key)
tamanho = response["ContentLength"]
print(f"\n📋 Metadados do arquivo:")
print(f"   Tamanho: {tamanho} bytes")
print(f"   Tipo: {response['ContentType']}")
print(f"   Última modificação: {response['LastModified']}")

# Download e verificação
print("\n📥 Fazendo download e verificando conteúdo...")
obj = client.get_object(Bucket="bronze", Key=object_key)
conteudo = json.loads(obj["Body"].read().decode("utf-8"))
assert conteudo["status"] == "ok", "Erro: conteúdo do arquivo não confere!"
print(f"   ✅ Conteúdo verificado: {conteudo['mensagem']}")
print("\n🎉 MinIO está funcionando corretamente!")
```

```bash
python scripts/test_minio_connection.py
```

---

### Verificação Final da Atividade 2

Ao final desta atividade, o aluno deve ser capaz de:

1. Confirmar que o contêiner MinIO está em execução com `docker compose ps`
2. Acessar o console web em `http://localhost:9001` e visualizar os 3 buckets criados (`bronze`, `silver`, `gold`)
3. Ver o arquivo de teste em `bronze/_testes/...` no console web
4. Compreender a estrutura de particionamento por data (`ano=YYYY/mes=MM/dia=DD`) que será utilizada ao longo do curso

---

## Atividade 3 — Comparação de Formatos de Arquivo: CSV, JSON e Parquet

### Objetivo

Demonstrar empiricamente as diferenças de desempenho, eficiência de armazenamento e capacidade de consulta entre os formatos CSV, JSON e Parquet. Esta atividade fundamenta a escolha do Parquet como formato padrão para Data Lakes e explica por que ele é o pilar dos formatos de tabela modernos como Apache Iceberg e Delta Lake.

### Contexto

A escolha do formato de arquivo tem impacto direto no custo de armazenamento e na velocidade de processamento de um Data Lake. O formato **Parquet** é colunar, comprimido e fortemente tipado — características que o tornam até 10 vezes mais eficiente que o CSV para cargas analíticas típicas, onde se lê apenas um subconjunto das colunas de um dataset grande.

Esta atividade utiliza o dataset **Iris** do UCI Machine Learning Repository para os exemplos básicos, e dados sintéticos para demonstrar as diferenças de escala.

---

### Passo 1 — Criação do Jupyter Notebook

```bash
cd ~/engenharia-dados-curso
source .venv/bin/activate

# Iniciar o Jupyter Notebook
jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser &

# O terminal exibirá uma URL com token de acesso, por exemplo:
# http://127.0.0.1:8888/tree?token=abc123...
```

Acesse a URL exibida no terminal e crie um novo notebook em `notebooks/` com o nome `aula1_formatos_arquivo.ipynb`.

---

### Passo 2 — Importações e Configuração Inicial

No notebook, execute as células a seguir em sequência:

```python
# Célula 1 — Importações
import pandas as pd
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import json
import os
import time
import boto3
from pathlib import Path
from datetime import datetime, timezone

print(f"Pandas: {pd.__version__}")
print(f"PyArrow: {pa.__version__}")
print("✅ Bibliotecas importadas com sucesso!")
```

```python
# Célula 2 — Configuração do cliente MinIO
s3_client = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="minioadmin",
    aws_secret_access_key="minioadmin123",
    region_name="us-east-1",
)

# Diretório temporário local para os arquivos gerados
Path("../data/bronze/iris").mkdir(parents=True, exist_ok=True)
Path("../data/bronze/sintetico").mkdir(parents=True, exist_ok=True)
print("✅ Diretórios e conexão MinIO configurados!")
```

---

### Passo 3 — Carregamento e Exploração do Dataset Iris

```python
# Célula 3 — Carregamento do dataset Iris
# O dataset Iris está disponível diretamente no repositório UCI
# Fonte: https://archive.ics.uci.edu/dataset/53/iris

URL_IRIS = (
    "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
)

COLUNAS_IRIS = [
    "comprimento_sepala_cm",
    "largura_sepala_cm",
    "comprimento_petala_cm",
    "largura_petala_cm",
    "especie",
]

df_iris = pd.read_csv(URL_IRIS, header=None, names=COLUNAS_IRIS)

# Adicionar metadados de ingestão (prática da camada Bronze)
df_iris["_fonte"] = "uci_iris"
df_iris["_ingerido_em"] = datetime.now(timezone.utc).isoformat()
df_iris["_versao_schema"] = "1.0"

print(f"Shape do dataset: {df_iris.shape}")
print(f"\nTipos de dados:\n{df_iris.dtypes}")
print(f"\nPrimeiras 5 linhas:")
df_iris.head()
```

```python
# Célula 4 — Estatísticas descritivas do dataset
print("=== Estatísticas Descritivas ===")
print(df_iris.describe())
print(f"\nDistribuição por espécie:")
print(df_iris["especie"].value_counts())
```

---

### Passo 4 — Geração de Dataset Sintético para Testes de Escala

O dataset Iris possui apenas 150 linhas, insuficiente para demonstrar diferenças de performance. Vamos gerar um dataset sintético de 1 milhão de registros que simula dados de transações de e-commerce:

```python
# Célula 5 — Geração do dataset sintético (1 milhão de registros)
print("Gerando dataset sintético de 1.000.000 registros...")
inicio = time.time()

np.random.seed(42)
N = 1_000_000

CATEGORIAS = ["Eletrônicos", "Roupas", "Alimentos", "Livros", "Esportes"]
STATUS = ["concluido", "cancelado", "pendente", "reembolsado"]
REGIOES = ["Sudeste", "Sul", "Nordeste", "Norte", "Centro-Oeste"]

df_sintetico = pd.DataFrame({
    "id_pedido": range(1, N + 1),
    "id_cliente": np.random.randint(1, 100_001, N),
    "id_produto": np.random.randint(1, 10_001, N),
    "categoria": np.random.choice(CATEGORIAS, N),
    "valor_unitario": np.round(np.random.uniform(5.0, 2000.0, N), 2),
    "quantidade": np.random.randint(1, 11, N),
    "status_pedido": np.random.choice(STATUS, N, p=[0.75, 0.10, 0.10, 0.05]),
    "regiao": np.random.choice(REGIOES, N),
    "data_pedido": pd.date_range(start="2022-01-01", periods=N, freq="30s"),
    "avaliacao_cliente": np.random.choice([1, 2, 3, 4, 5, None], N, p=[0.05, 0.08, 0.15, 0.30, 0.37, 0.05]),
    "_fonte": "sistema_ecommerce_v2",
    "_ingerido_em": datetime.now(timezone.utc).isoformat(),
})

# Calcular o valor total do pedido
df_sintetico["valor_total"] = (
    df_sintetico["valor_unitario"] * df_sintetico["quantidade"]
).round(2)

duracao = time.time() - inicio
print(f"✅ Dataset gerado em {duracao:.2f}s")
print(f"Shape: {df_sintetico.shape}")
print(f"Uso de memória: {df_sintetico.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
```

---

### Passo 5 — Gravação nos Três Formatos

```python
# Célula 6 — Gravação do dataset sintético nos três formatos

BASE_PATH = Path("../data/bronze/sintetico")

# ── CSV ──────────────────────────────────────────────────────────────────────
print("Gravando CSV...")
inicio = time.time()
caminho_csv = BASE_PATH / "pedidos.csv"
df_sintetico.to_csv(caminho_csv, index=False)
tempo_escrita_csv = time.time() - inicio
tamanho_csv = caminho_csv.stat().st_size

# ── JSON (linhas) ─────────────────────────────────────────────────────────────
print("Gravando JSON Lines (JSONL)...")
inicio = time.time()
caminho_json = BASE_PATH / "pedidos.jsonl"
df_sintetico.to_json(caminho_json, orient="records", lines=True, date_format="iso")
tempo_escrita_json = time.time() - inicio
tamanho_json = caminho_json.stat().st_size

# ── Parquet (sem compressão) ──────────────────────────────────────────────────
print("Gravando Parquet (sem compressão)...")
inicio = time.time()
caminho_parquet_raw = BASE_PATH / "pedidos_sem_compressao.parquet"
df_sintetico.to_parquet(caminho_parquet_raw, index=False, compression=None)
tempo_escrita_parquet_raw = time.time() - inicio
tamanho_parquet_raw = caminho_parquet_raw.stat().st_size

# ── Parquet (Snappy — padrão da indústria) ────────────────────────────────────
print("Gravando Parquet (Snappy)...")
inicio = time.time()
caminho_parquet_snappy = BASE_PATH / "pedidos_snappy.parquet"
df_sintetico.to_parquet(caminho_parquet_snappy, index=False, compression="snappy")
tempo_escrita_parquet_snappy = time.time() - inicio
tamanho_parquet_snappy = caminho_parquet_snappy.stat().st_size

# ── Parquet (ZSTD — melhor compressão) ───────────────────────────────────────
print("Gravando Parquet (ZSTD)...")
inicio = time.time()
caminho_parquet_zstd = BASE_PATH / "pedidos_zstd.parquet"
df_sintetico.to_parquet(caminho_parquet_zstd, index=False, compression="zstd")
tempo_escrita_parquet_zstd = time.time() - inicio
tamanho_parquet_zstd = caminho_parquet_zstd.stat().st_size

print("\n✅ Todos os arquivos gravados!")
```

---

### Passo 6 — Comparação de Tamanho em Disco

```python
# Célula 7 — Tabela comparativa de tamanho em disco

def formatar_tamanho(bytes_val: int) -> str:
    """Formata bytes em MB com 1 casa decimal."""
    return f"{bytes_val / 1024**2:.1f} MB"

def reducao_percentual(base: int, comparado: int) -> str:
    """Calcula a redução percentual em relação ao CSV."""
    reducao = (1 - comparado / base) * 100
    return f"{reducao:.1f}% menor"

resultados_tamanho = {
    "Formato": ["CSV", "JSON Lines", "Parquet (sem compressão)", "Parquet (Snappy)", "Parquet (ZSTD)"],
    "Tamanho em Disco": [
        formatar_tamanho(tamanho_csv),
        formatar_tamanho(tamanho_json),
        formatar_tamanho(tamanho_parquet_raw),
        formatar_tamanho(tamanho_parquet_snappy),
        formatar_tamanho(tamanho_parquet_zstd),
    ],
    "Redução vs CSV": [
        "— (referência)",
        reducao_percentual(tamanho_csv, tamanho_json),
        reducao_percentual(tamanho_csv, tamanho_parquet_raw),
        reducao_percentual(tamanho_csv, tamanho_parquet_snappy),
        reducao_percentual(tamanho_csv, tamanho_parquet_zstd),
    ],
    "Tempo de Escrita (s)": [
        f"{tempo_escrita_csv:.2f}",
        f"{tempo_escrita_json:.2f}",
        f"{tempo_escrita_parquet_raw:.2f}",
        f"{tempo_escrita_parquet_snappy:.2f}",
        f"{tempo_escrita_parquet_zstd:.2f}",
    ],
}

df_tamanhos = pd.DataFrame(resultados_tamanho)
print("=== Comparativo de Tamanho em Disco (1.000.000 registros) ===")
print(df_tamanhos.to_string(index=False))
```

---

### Passo 7 — Comparação de Velocidade de Leitura

Esta é a demonstração mais importante: a leitura seletiva de colunas (column pruning), que é onde o Parquet demonstra sua maior vantagem sobre formatos baseados em linhas.

```python
# Célula 8 — Comparação de velocidade de leitura (arquivo completo)

REPETICOES = 3  # Número de repetições para calcular a média

def medir_tempo_leitura(funcao_leitura, repeticoes=REPETICOES):
    """Executa a função de leitura N vezes e retorna o tempo médio."""
    tempos = []
    for _ in range(repeticoes):
        inicio = time.time()
        funcao_leitura()
        tempos.append(time.time() - inicio)
    return sum(tempos) / len(tempos)

# Leitura completa
tempo_csv_completo = medir_tempo_leitura(
    lambda: pd.read_csv(caminho_csv)
)
tempo_json_completo = medir_tempo_leitura(
    lambda: pd.read_json(caminho_json, lines=True)
)
tempo_parquet_completo = medir_tempo_leitura(
    lambda: pd.read_parquet(caminho_parquet_snappy)
)

print(f"Leitura COMPLETA (1.000.000 linhas, todas as colunas):")
print(f"  CSV:     {tempo_csv_completo:.3f}s")
print(f"  JSON:    {tempo_json_completo:.3f}s")
print(f"  Parquet: {tempo_parquet_completo:.3f}s")
print(f"  → Parquet é {tempo_csv_completo / tempo_parquet_completo:.1f}x mais rápido que CSV")
```

```python
# Célula 9 — Leitura seletiva de colunas (column pruning)
# Esta é a vantagem FUNDAMENTAL do formato colunar

COLUNAS_ANALITICAS = ["categoria", "valor_total", "status_pedido", "regiao"]

# CSV: precisa ler TODAS as colunas e depois filtrar
tempo_csv_seletivo = medir_tempo_leitura(
    lambda: pd.read_csv(caminho_csv, usecols=COLUNAS_ANALITICAS)
)

# Parquet: lê APENAS as colunas solicitadas do disco
tempo_parquet_seletivo = medir_tempo_leitura(
    lambda: pd.read_parquet(caminho_parquet_snappy, columns=COLUNAS_ANALITICAS)
)

print(f"Leitura SELETIVA (apenas 4 de 14 colunas):")
print(f"  CSV:     {tempo_csv_seletivo:.3f}s  (ainda lê tudo do disco)")
print(f"  Parquet: {tempo_parquet_seletivo:.3f}s (lê apenas as colunas necessárias)")
print(f"  → Parquet é {tempo_csv_seletivo / tempo_parquet_seletivo:.1f}x mais rápido na leitura seletiva")
print()
print("💡 Em Data Lakes com petabytes de dados, essa diferença representa")
print("   economia de horas de processamento e centenas de dólares em custo de nuvem.")
```

---

### Passo 8 — Inspeção do Schema do Parquet

Uma das vantagens do Parquet é o armazenamento do schema (metadados de tipos) junto com os dados:

```python
# Célula 10 — Inspeção do schema do arquivo Parquet

schema_parquet = pq.read_schema(caminho_parquet_snappy)

print("=== Schema do Arquivo Parquet ===")
print(schema_parquet)
print()
print("=== Metadados do Arquivo ===")
metadata = pq.read_metadata(caminho_parquet_snappy)
print(f"Número de row groups: {metadata.num_row_groups}")
print(f"Número de colunas: {metadata.num_columns}")
print(f"Número de linhas: {metadata.num_rows:,}")
print(f"Tamanho serializado: {metadata.serialized_size:,} bytes")
print()
print("💡 O Parquet armazena o schema junto com os dados.")
print("   Isso elimina a necessidade de inferência de tipos na leitura,")
print("   garantindo consistência e evitando erros silenciosos.")
```

---

### Passo 9 — Upload dos Arquivos para o MinIO (Camada Bronze)

Após comparar os formatos, vamos fazer o upload do arquivo Parquet (o escolhido para o Data Lake) para o MinIO, seguindo a convenção de particionamento por data:

```python
# Célula 11 — Upload do Parquet para o MinIO (camada Bronze)

hoje = datetime.now()
prefixo_particao = f"ano={hoje.year}/mes={hoje.month:02d}/dia={hoje.day:02d}"

# Upload do Parquet Snappy para o bucket Bronze
chave_objeto = f"ecommerce_sintetico/{prefixo_particao}/pedidos.parquet"

print(f"📤 Fazendo upload para: bronze/{chave_objeto}")
inicio = time.time()

s3_client.upload_file(
    Filename=str(caminho_parquet_snappy),
    Bucket="bronze",
    Key=chave_objeto,
    ExtraArgs={"ContentType": "application/octet-stream"},
)

duracao = time.time() - inicio
print(f"✅ Upload concluído em {duracao:.2f}s")

# Verificar o objeto no MinIO
response = s3_client.head_object(Bucket="bronze", Key=chave_objeto)
print(f"\nMetadados no MinIO:")
print(f"  Tamanho: {response['ContentLength'] / 1024**2:.1f} MB")
print(f"  Última modificação: {response['LastModified']}")
print(f"\n🎉 Dado bruto armazenado na camada Bronze do Data Lake!")
print(f"   Acesse em: http://localhost:9001/browser/bronze")
```

---

### Passo 10 — Resumo Comparativo Final

```python
# Célula 12 — Resumo final comparativo

print("=" * 65)
print("  RESUMO COMPARATIVO — FORMATOS DE ARQUIVO PARA DATA LAKES")
print("=" * 65)

resumo = pd.DataFrame({
    "Característica": [
        "Tipo de armazenamento",
        "Compressão nativa",
        "Schema embutido",
        "Leitura seletiva de colunas",
        "Suporte a tipos complexos",
        "Legível por humanos",
        "Ideal para Data Lakes",
        "Suporte em ferramentas",
    ],
    "CSV": [
        "Orientado a linhas",
        "Não",
        "Não (inferido)",
        "Não (lê tudo)",
        "Não",
        "Sim",
        "❌ Não recomendado",
        "Universal",
    ],
    "JSON/JSONL": [
        "Orientado a linhas",
        "Não",
        "Não (inferido)",
        "Não (lê tudo)",
        "Sim (aninhado)",
        "Sim",
        "⚠️  Apenas para APIs",
        "Universal",
    ],
    "Parquet": [
        "Orientado a colunas",
        "Sim (Snappy/ZSTD)",
        "Sim (forte tipagem)",
        "Sim (column pruning)",
        "Sim (listas, mapas)",
        "Não (binário)",
        "✅ Padrão da indústria",
        "Spark, DuckDB, Iceberg...",
    ],
})

print(resumo.to_string(index=False))
print()
print("Conclusão: O formato Parquet com compressão Snappy ou ZSTD é o")
print("padrão da indústria para Data Lakes por combinar alta compressão,")
print("leitura seletiva de colunas e schema fortemente tipado.")
```

## Ingestão de Dados e a Camada Bronze

**Pré-requisitos:** ambiente Docker operacional, MinIO rodando com buckets Bronze/Silver/Gold criados, ambiente virtual Python ativo

---

## Visão Geral das Atividades

As três atividades a seguir constroem os primeiros pipelines de ingestão reais do curso, conectando fontes externas ao Data Lake local. A **Atividade 1** coloca o Airbyte em operação — uma plataforma visual de ingestão que elimina a necessidade de código para conectar dezenas de fontes de dados. A **Atividade 2** desenvolve um pipeline programático em Python com a biblioteca `dlt` (Data Load Tool), extraindo dados de duas APIs públicas com paginação e carregando-os diretamente no MinIO em formato Parquet. A **Atividade 3** consolida as boas práticas de organização da camada Bronze, implementando particionamento lógico por data e adicionando metadados de rastreabilidade a cada arquivo ingerido.

| Atividade | Tema | Duração Estimada | Ferramentas |
|---|---|---|---|
| 1 | Configuração do Airbyte e Criação de Conexões | 50 min | Docker Compose, Airbyte OSS |
| 2 | Pipeline de Ingestão com `dlt` + APIs Públicas | 60 min | Python, `dlt`, REST Countries API, PokeAPI |
| 3 | Organização da Camada Bronze com Particionamento | 40 min | Python, `boto3`, Parquet, MinIO |

> **Regra de ouro da camada Bronze:** dados ingeridos nesta camada nunca devem ser alterados após a gravação. O objetivo é preservar o dado exatamente como veio da fonte, acrescentando apenas metadados de rastreabilidade (timestamp de ingestão, nome da fonte, versão do schema). Qualquer transformação, limpeza ou enriquecimento ocorre exclusivamente nas camadas Silver e Gold.

---

## Atividade 1 — Configuração do Airbyte e Criação de Conexões

### Objetivo

Instalar e configurar o **Airbyte Open Source** via Docker Compose, explorar sua interface web e criar uma conexão completa entre uma fonte de dados externa (REST Countries API) e o MinIO (destino S3-compatível), demonstrando como uma plataforma de ingestão visual elimina a necessidade de código para o processo de extração e carga (o "EL" do paradigma ELT).

### Contexto

O Airbyte é uma plataforma open source de integração de dados que oferece mais de 350 conectores pré-construídos para bancos de dados, APIs, arquivos e serviços SaaS[[1]](#ref1). Sua arquitetura baseada em contêineres Docker permite que cada conector seja executado de forma isolada, garantindo que uma falha em uma conexão não afete as demais. Em ambientes de produção, o Airbyte é implantado em Kubernetes para escalabilidade horizontal.

---

### Passo 1 — Adição do Airbyte ao Docker Compose

O Airbyte requer vários serviços internos (servidor, worker, banco de dados de metadados, servidor de temporalidade). A forma mais simples de instalá-lo localmente é utilizando o script oficial de instalação, que gerencia automaticamente todos esses serviços.

```bash
# Navegar para o diretório de trabalho do curso
cd ~/engenharia-dados-curso

# Criar um subdiretório dedicado ao Airbyte
mkdir -p airbyte && cd airbyte

# Baixar o script de instalação oficial do Airbyte OSS
curl -fsSL https://raw.githubusercontent.com/airbytehq/airbyte/master/run-ab-platform.sh \
  -o run-ab-platform.sh

# Tornar o script executável
chmod +x run-ab-platform.sh

# Executar a instalação (aceita automaticamente os termos de uso)
./run-ab-platform.sh -b
```

> **Atenção:** O Airbyte faz download de várias imagens Docker (~2 GB). Certifique-se de ter conexão estável com a internet e pelo menos 4 GB de RAM disponíveis. A inicialização completa pode levar entre 3 e 5 minutos na primeira execução.

**Verificação da inicialização:**

```bash
# Acompanhar o status dos contêineres do Airbyte
docker compose -f ~/engenharia-dados-curso/airbyte/docker-compose.yaml ps

# Aguardar até que todos os serviços estejam com status "healthy"
# Os serviços principais são: airbyte-server, airbyte-worker, airbyte-webapp
```

---

### Passo 2 — Acesso à Interface Web do Airbyte

Após todos os serviços estarem saudáveis, acesse a interface web do Airbyte:

```
URL:   http://localhost:8000
Usuário: airbyte
Senha:   password
```

Ao fazer login pela primeira vez, o Airbyte solicitará um e-mail para cadastro. Utilize qualquer e-mail válido (não é necessário confirmar). Explore brevemente a interface, identificando as seções principais:

| Seção | Descrição |
|---|---|
| **Sources** | Catálogo de conectores de origem (APIs, bancos de dados, arquivos) |
| **Destinations** | Conectores de destino (Data Warehouses, Data Lakes, bancos de dados) |
| **Connections** | Pipelines configurados (Source → Destination) com agendamento |
| **Settings** | Configurações gerais, notificações e integrações |

---

### Passo 3 — Configuração do Destination: MinIO (S3-Compatível)

Antes de criar a fonte de dados, configure o destino (MinIO) para que o Airbyte saiba onde gravar os dados extraídos.

Na interface do Airbyte, navegue até **Destinations → New Destination** e pesquise por **"S3"**. Selecione o conector **Amazon S3** e preencha os campos conforme abaixo:

| Campo | Valor |
|---|---|
| **Destination name** | `minio-bronze-local` |
| **S3 Bucket Name** | `bronze` |
| **S3 Bucket Path** | `airbyte/{namespace}/{stream_name}` |
| **S3 Bucket Region** | `us-east-1` |
| **Access Key ID** | `minioadmin` |
| **Secret Access Key** | `minioadmin123` |
| **S3 Endpoint** | `http://host.docker.internal:9000` |
| **Output Format** | `Parquet — Apache Parquet columnar storage` |
| **Compression Codec** | `SNAPPY` |

> **Nota técnica:** O endereço `host.docker.internal` é utilizado porque o Airbyte roda dentro de contêineres Docker e precisa acessar o MinIO, que está em outro contêiner na mesma máquina. Em sistemas Linux, pode ser necessário adicionar `--add-host=host.docker.internal:host-gateway` ao `docker-compose.yaml` do Airbyte se a resolução falhar.

Clique em **Test and Save**. O Airbyte criará um arquivo de teste no bucket `bronze` para validar a conexão. Se o teste passar, o destino está configurado corretamente.

---

### Passo 4 — Configuração da Source: REST Countries API

Navegue até **Sources → New Source** e pesquise por **"REST Countries"** ou, alternativamente, utilize o conector genérico **"HTTP Request"** para maior flexibilidade.

Para usar o conector HTTP genérico, selecione **"Low-code CDK Connector"** ou **"Custom HTTP"** e configure:

| Campo | Valor |
|---|---|
| **Source name** | `rest-countries-api` |
| **API URL** | `https://restcountries.com/v3.1/all` |
| **HTTP Method** | `GET` |
| **Authentication** | `No Auth` |

Clique em **Test and Save**. O Airbyte fará uma requisição de teste à API e exibirá uma amostra dos dados retornados — um array JSON com informações de todos os países do mundo.

---

### Passo 5 — Criação da Connection (Pipeline Completo)

Com Source e Destination configurados, crie a conexão que define o pipeline de ingestão:

1. Navegue até **Connections → New Connection**
2. Selecione a source `rest-countries-api`
3. Selecione o destination `minio-bronze-local`
4. Configure os parâmetros da conexão:

| Parâmetro | Valor | Justificativa |
|---|---|---|
| **Connection name** | `countries-to-bronze` | Nome descritivo do pipeline |
| **Replication frequency** | `Manual` | Para controle manual durante o curso |
| **Sync mode** | `Full Refresh — Overwrite` | Dados cadastrais raramente mudam |
| **Namespace format** | `rest_countries` | Organiza os dados por namespace |

5. Clique em **Set up connection**
6. Execute a sincronização manualmente clicando em **Sync Now**

---

### Passo 6 — Verificação dos Dados no MinIO

Após a sincronização concluir (status **Succeeded**), verifique os dados no MinIO:

```bash
# Listar os objetos criados pelo Airbyte no bucket bronze
python3 - << 'EOF'
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
EOF
```

Você deve ver arquivos Parquet criados pelo Airbyte no caminho `bronze/airbyte/rest_countries/...`. Acesse também o console web do MinIO em `http://localhost:9001` para visualizar os arquivos graficamente.

---


## Ingestão de Dados e a Camada Bronze

**Pré-requisitos:** ambiente Docker operacional, MinIO rodando com buckets Bronze/Silver/Gold criados, ambiente virtual Python ativo

---

## Visão Geral das Atividades

As três atividades a seguir constroem os primeiros pipelines de ingestão reais do curso, conectando fontes externas ao Data Lake local. A **Atividade 1** coloca o Airbyte em operação — uma plataforma visual de ingestão que elimina a necessidade de código para conectar dezenas de fontes de dados. A **Atividade 2** desenvolve um pipeline programático em Python com a biblioteca `dlt` (Data Load Tool), extraindo dados de duas APIs públicas com paginação e carregando-os diretamente no MinIO em formato Parquet. A **Atividade 3** consolida as boas práticas de organização da camada Bronze, implementando particionamento lógico por data e adicionando metadados de rastreabilidade a cada arquivo ingerido.

| Atividade | Tema | Duração Estimada | Ferramentas |
|---|---|---|---|
| 1 | Configuração do Airbyte e Criação de Conexões | 50 min | Docker Compose, Airbyte OSS |
| 2 | Pipeline de Ingestão com `dlt` + APIs Públicas | 60 min | Python, `dlt`, REST Countries API, PokeAPI |
| 3 | Organização da Camada Bronze com Particionamento | 40 min | Python, `boto3`, Parquet, MinIO |

> **Regra de ouro da camada Bronze:** dados ingeridos nesta camada nunca devem ser alterados após a gravação. O objetivo é preservar o dado exatamente como veio da fonte, acrescentando apenas metadados de rastreabilidade (timestamp de ingestão, nome da fonte, versão do schema). Qualquer transformação, limpeza ou enriquecimento ocorre exclusivamente nas camadas Silver e Gold.

---

## Atividade 1 — Configuração do Airbyte e Criação de Conexões

### Objetivo

Instalar e configurar o **Airbyte Open Source** via Docker Compose, explorar sua interface web e criar uma conexão completa entre uma fonte de dados externa (REST Countries API) e o MinIO (destino S3-compatível), demonstrando como uma plataforma de ingestão visual elimina a necessidade de código para o processo de extração e carga (o "EL" do paradigma ELT).

### Contexto

O Airbyte é uma plataforma open source de integração de dados que oferece mais de 350 conectores pré-construídos para bancos de dados, APIs, arquivos e serviços SaaS[[1]](#ref1). Sua arquitetura baseada em contêineres Docker permite que cada conector seja executado de forma isolada, garantindo que uma falha em uma conexão não afete as demais. Em ambientes de produção, o Airbyte é implantado em Kubernetes para escalabilidade horizontal.

---

### Passo 1 — Adição do Airbyte ao Docker Compose

O Airbyte requer vários serviços internos (servidor, worker, banco de dados de metadados, servidor de temporalidade). A forma mais simples de instalá-lo localmente é utilizando o script oficial de instalação, que gerencia automaticamente todos esses serviços.

```bash
# Navegar para o diretório de trabalho do curso
cd ~/engenharia-dados-curso

# Criar um subdiretório dedicado ao Airbyte
mkdir -p airbyte && cd airbyte

# Baixar o script de instalação oficial do Airbyte OSS
curl -fsSL https://raw.githubusercontent.com/airbytehq/airbyte/master/run-ab-platform.sh \
  -o run-ab-platform.sh

# Tornar o script executável
chmod +x run-ab-platform.sh

# Executar a instalação (aceita automaticamente os termos de uso)
./run-ab-platform.sh -b
```

> **Atenção:** O Airbyte faz download de várias imagens Docker (~2 GB). Certifique-se de ter conexão estável com a internet e pelo menos 4 GB de RAM disponíveis. A inicialização completa pode levar entre 3 e 5 minutos na primeira execução.

**Verificação da inicialização:**

```bash
# Acompanhar o status dos contêineres do Airbyte
docker compose -f ~/engenharia-dados-curso/airbyte/docker-compose.yaml ps

# Aguardar até que todos os serviços estejam com status "healthy"
# Os serviços principais são: airbyte-server, airbyte-worker, airbyte-webapp
```

---

### Passo 2 — Acesso à Interface Web do Airbyte

Após todos os serviços estarem saudáveis, acesse a interface web do Airbyte:

```
URL:   http://localhost:8000
Usuário: airbyte
Senha:   password
```

Ao fazer login pela primeira vez, o Airbyte solicitará um e-mail para cadastro. Utilize qualquer e-mail válido (não é necessário confirmar). Explore brevemente a interface, identificando as seções principais:

| Seção | Descrição |
|---|---|
| **Sources** | Catálogo de conectores de origem (APIs, bancos de dados, arquivos) |
| **Destinations** | Conectores de destino (Data Warehouses, Data Lakes, bancos de dados) |
| **Connections** | Pipelines configurados (Source → Destination) com agendamento |
| **Settings** | Configurações gerais, notificações e integrações |

---

### Passo 3 — Configuração do Destination: MinIO (S3-Compatível)

Antes de criar a fonte de dados, configure o destino (MinIO) para que o Airbyte saiba onde gravar os dados extraídos.

Na interface do Airbyte, navegue até **Destinations → New Destination** e pesquise por **"S3"**. Selecione o conector **Amazon S3** e preencha os campos conforme abaixo:

| Campo | Valor |
|---|---|
| **Destination name** | `minio-bronze-local` |
| **S3 Bucket Name** | `bronze` |
| **S3 Bucket Path** | `airbyte/{namespace}/{stream_name}` |
| **S3 Bucket Region** | `us-east-1` |
| **Access Key ID** | `minioadmin` |
| **Secret Access Key** | `minioadmin123` |
| **S3 Endpoint** | `http://host.docker.internal:9000` |
| **Output Format** | `Parquet — Apache Parquet columnar storage` |
| **Compression Codec** | `SNAPPY` |

> **Nota técnica:** O endereço `host.docker.internal` é utilizado porque o Airbyte roda dentro de contêineres Docker e precisa acessar o MinIO, que está em outro contêiner na mesma máquina. Em sistemas Linux, pode ser necessário adicionar `--add-host=host.docker.internal:host-gateway` ao `docker-compose.yaml` do Airbyte se a resolução falhar.

Clique em **Test and Save**. O Airbyte criará um arquivo de teste no bucket `bronze` para validar a conexão. Se o teste passar, o destino está configurado corretamente.

---

### Passo 4 — Configuração da Source: REST Countries API

Navegue até **Sources → New Source** e pesquise por **"REST Countries"** ou, alternativamente, utilize o conector genérico **"HTTP Request"** para maior flexibilidade.

Para usar o conector HTTP genérico, selecione **"Low-code CDK Connector"** ou **"Custom HTTP"** e configure:

| Campo | Valor |
|---|---|
| **Source name** | `rest-countries-api` |
| **API URL** | `https://restcountries.com/v3.1/all` |
| **HTTP Method** | `GET` |
| **Authentication** | `No Auth` |

Clique em **Test and Save**. O Airbyte fará uma requisição de teste à API e exibirá uma amostra dos dados retornados — um array JSON com informações de todos os países do mundo.

---

### Passo 5 — Criação da Connection (Pipeline Completo)

Com Source e Destination configurados, crie a conexão que define o pipeline de ingestão:

1. Navegue até **Connections → New Connection**
2. Selecione a source `rest-countries-api`
3. Selecione o destination `minio-bronze-local`
4. Configure os parâmetros da conexão:

| Parâmetro | Valor | Justificativa |
|---|---|---|
| **Connection name** | `countries-to-bronze` | Nome descritivo do pipeline |
| **Replication frequency** | `Manual` | Para controle manual durante o curso |
| **Sync mode** | `Full Refresh — Overwrite` | Dados cadastrais raramente mudam |
| **Namespace format** | `rest_countries` | Organiza os dados por namespace |

5. Clique em **Set up connection**
6. Execute a sincronização manualmente clicando em **Sync Now**

---

### Passo 6 — Verificação dos Dados no MinIO

Após a sincronização concluir (status **Succeeded**), verifique os dados no MinIO:

```bash
# Listar os objetos criados pelo Airbyte no bucket bronze
python3 - << 'EOF'
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
EOF
```

Você deve ver arquivos Parquet criados pelo Airbyte no caminho `bronze/airbyte/rest_countries/...`. Acesse também o console web do MinIO em `http://localhost:9001` para visualizar os arquivos graficamente.

---

### Verificação Final da Atividade 1

Ao concluir esta atividade, o aluno deve ser capaz de:

1. Confirmar que todos os contêineres do Airbyte estão em execução com `docker compose ps`
2. Acessar a interface web do Airbyte em `http://localhost:8000` e navegar pelas seções principais
3. Verificar que a connection `countries-to-bronze` executou com status **Succeeded**
4. Confirmar a presença de arquivos Parquet no bucket `bronze` do MinIO via script Python ou console web
5. Explicar a diferença entre os modos de sincronização **Full Refresh** e **Incremental Append**

---

## Atividade 2 — Pipeline de Ingestão com `dlt` + APIs Públicas

### Objetivo

Desenvolver pipelines de ingestão programáticos em Python utilizando a biblioteca **`dlt` (Data Load Tool)**, extraindo dados de duas APIs públicas — REST Countries API e PokeAPI — com tratamento de paginação, e carregando os dados diretamente no MinIO em formato Parquet. Esta atividade demonstra como construir pipelines de ingestão customizados quando os conectores pré-construídos do Airbyte não atendem a requisitos específicos de negócio.

### Contexto

O `dlt` é uma biblioteca Python open source que simplifica drasticamente a construção de pipelines de ingestão, oferecendo funcionalidades como inferência automática de schema, normalização de dados aninhados (JSON → tabelas relacionais), gerenciamento de estado para ingestão incremental e suporte nativo a múltiplos destinos (incluindo S3/MinIO, DuckDB, BigQuery e Snowflake)[[2]](#ref2). Diferentemente do Airbyte, o `dlt` é orientado a código, o que o torna ideal para pipelines que exigem lógica customizada de extração.

---

### Passo 1 — Instalação das Dependências

```bash
cd ~/engenharia-dados-curso
source .venv/bin/activate

# Instalar o dlt com suporte ao destino filesystem (S3/MinIO)
pip install "dlt[filesystem]"

# Instalar bibliotecas auxiliares
pip install requests tenacity

# Verificar a instalação
python -c "import dlt; print(f'dlt versão: {dlt.__version__}')"
```

---

### Passo 2 — Pipeline 1: REST Countries API

A REST Countries API retorna dados detalhados sobre todos os países do mundo em uma única requisição, sem necessidade de paginação. É ideal para demonstrar a ingestão de dados cadastrais estáticos (dimensões) — o tipo de dado que compõe as **Tabelas de Dimensão** na camada Gold.

Crie o arquivo `scripts/ingest_countries.py`:

```python
# scripts/ingest_countries.py
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
    "name", "cca2", "cca3", "ccn3",
    "region", "subregion", "continents",
    "capital", "languages", "currencies",
    "population", "area", "latlng",
    "landlocked", "independent", "status",
    "timezones", "borders",
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
```

Execute o pipeline:

```bash
cd ~/engenharia-dados-curso
source .venv/bin/activate
python scripts/ingest_countries.py
```

---

### Passo 3 — Exploração dos Dados Ingeridos (REST Countries)

Após a execução, explore os dados carregados no MinIO:

```python
# scripts/explorar_countries_bronze.py
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
```

```bash
python scripts/explorar_countries_bronze.py
```

---

### Passo 4 — Pipeline 2: PokeAPI com Paginação

A PokeAPI é um exemplo de API com paginação — um padrão extremamente comum em sistemas transacionais reais. O endpoint `/pokemon` retorna apenas 20 registros por página, exigindo múltiplas requisições para extrair o dataset completo. Esta atividade demonstra como o `dlt` gerencia paginação de forma elegante e como implementar **ingestão incremental** (extraindo apenas registros novos em execuções subsequentes).

Crie o arquivo `scripts/ingest_pokemon.py`:

```python
# scripts/ingest_pokemon.py
"""
Pipeline de ingestão da PokeAPI para a camada Bronze.

Fonte: https://pokeapi.co/api/v2/pokemon
Destino: MinIO (bucket bronze) — formato Parquet com compressão Snappy
Tipo de dado: Entidade com relacionamentos (pokémon → habilidades, tipos, estatísticas)

A PokeAPI demonstra dois padrões fundamentais de ingestão:
  1. Paginação: o endpoint lista retorna 20 itens por página
  2. Enriquecimento: cada item da lista requer uma segunda requisição
     para obter os detalhes completos (padrão "list + detail")
"""

import dlt
import requests
import time
import logging
from datetime import datetime, timezone
from typing import Iterator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

import os
os.environ["DESTINATION__FILESYSTEM__BUCKET_URL"] = "s3://bronze"
os.environ["DESTINATION__FILESYSTEM__CREDENTIALS__AWS_ACCESS_KEY_ID"] = "minioadmin"
os.environ["DESTINATION__FILESYSTEM__CREDENTIALS__AWS_SECRET_ACCESS_KEY"] = "minioadmin123"
os.environ["DESTINATION__FILESYSTEM__CREDENTIALS__ENDPOINT_URL"] = "http://localhost:9000"
os.environ["DESTINATION__FILESYSTEM__CREDENTIALS__REGION_NAME"] = "us-east-1"

# Configurações da API
BASE_URL = "https://pokeapi.co/api/v2"
LIMITE_POR_PAGINA = 100   # Máximo permitido pela PokeAPI
TOTAL_POKEMON = 300       # Limitar a 300 para a atividade (existem ~1300 no total)
DELAY_ENTRE_REQUESTS = 0.1  # Segundos entre requisições (respeitar rate limit)


def buscar_detalhes_pokemon(url: str, session: requests.Session) -> dict:
    """
    Busca os detalhes completos de um pokémon pelo URL do recurso.
    Implementa retry simples em caso de falha temporária.
    """
    for tentativa in range(3):
        try:
            resposta = session.get(url, timeout=10)
            resposta.raise_for_status()
            return resposta.json()
        except requests.RequestException as e:
            if tentativa == 2:
                raise
            logger.warning(f"Tentativa {tentativa + 1} falhou para {url}: {e}. Retentando...")
            time.sleep(1)


def normalizar_pokemon(dados: dict, timestamp: str) -> dict:
    """
    Normaliza os dados brutos de um pokémon, achatando estruturas aninhadas
    que seriam difíceis de trabalhar diretamente.
    Na camada Bronze, mantemos o dado original E adicionamos campos normalizados
    para facilitar o uso downstream.
    """
    return {
        # Identificadores
        "id": dados["id"],
        "nome": dados["name"],
        "nome_especie": dados.get("species", {}).get("name"),

        # Atributos físicos
        "altura_dm": dados["height"],       # Em decímetros
        "peso_hg": dados["weight"],         # Em hectogramas
        "experiencia_base": dados["base_experience"],

        # Tipos (até 2 tipos por pokémon)
        "tipo_primario": dados["types"][0]["type"]["name"] if dados["types"] else None,
        "tipo_secundario": dados["types"][1]["type"]["name"] if len(dados["types"]) > 1 else None,

        # Estatísticas base (estrutura original preservada como lista)
        "estatisticas": [
            {"nome": s["stat"]["name"], "valor_base": s["base_stat"]}
            for s in dados["stats"]
        ],

        # Habilidades
        "habilidades": [
            {"nome": a["ability"]["name"], "oculta": a["is_hidden"]}
            for a in dados["abilities"]
        ],

        # Sprites (imagens)
        "sprite_url": dados.get("sprites", {}).get("front_default"),

        # Metadados de rastreabilidade (obrigatórios na camada Bronze)
        "_fonte": "pokeapi_v2",
        "_url_recurso": f"{BASE_URL}/pokemon/{dados['id']}",
        "_ingerido_em": timestamp,
        "_versao_api": "v2",
    }


@dlt.resource(
    name="pokemon",
    write_disposition="replace",
    primary_key="id",
)
def extrair_pokemon(total: int = TOTAL_POKEMON) -> Iterator[dict]:
    """
    Extrai pokémons da PokeAPI com paginação automática.

    Fluxo de extração:
      1. GET /pokemon?limit=100&offset=0  → lista de 100 pokémons (apenas nome + URL)
      2. Para cada pokémon da lista: GET /pokemon/{id} → detalhes completos
      3. Repetir com offset=100, 200, ... até atingir o total desejado
    """
    timestamp_ingestao = datetime.now(timezone.utc).isoformat()
    session = requests.Session()
    session.headers.update({"User-Agent": "DataEngineeringCourse/1.0"})

    total_extraidos = 0
    offset = 0

    logger.info(f"Iniciando extração de {total} pokémons da PokeAPI")

    while total_extraidos < total:
        # Calcular quantos registros buscar nesta página
        limite_pagina = min(LIMITE_POR_PAGINA, total - total_extraidos)

        # Requisição à página de listagem
        url_lista = f"{BASE_URL}/pokemon?limit={limite_pagina}&offset={offset}"
        logger.info(f"Buscando lista: offset={offset}, limite={limite_pagina}")

        resposta_lista = session.get(url_lista, timeout=15)
        resposta_lista.raise_for_status()
        dados_lista = resposta_lista.json()

        resultados = dados_lista.get("results", [])
        if not resultados:
            logger.info("Sem mais resultados. Encerrando paginação.")
            break

        # Para cada item da lista, buscar os detalhes completos
        for item in resultados:
            dados_detalhes = buscar_detalhes_pokemon(item["url"], session)
            pokemon_normalizado = normalizar_pokemon(dados_detalhes, timestamp_ingestao)
            yield pokemon_normalizado
            total_extraidos += 1

            # Respeitar o rate limit da API (gratuita e sem autenticação)
            time.sleep(DELAY_ENTRE_REQUESTS)

        offset += limite_pagina
        logger.info(f"Progresso: {total_extraidos}/{total} pokémons extraídos")

    logger.info(f"Extração concluída. Total: {total_extraidos} pokémons")


def executar_pipeline():
    """Configura e executa o pipeline dlt para a PokeAPI."""

    pipeline = dlt.pipeline(
        pipeline_name="pokeapi_bronze",
        destination="filesystem",
        dataset_name="pokeapi",
    )

    logger.info("Iniciando pipeline: PokeAPI → MinIO Bronze")
    inicio = datetime.now()

    info = pipeline.run(
        extrair_pokemon(),
        loader_file_format="parquet",
    )

    duracao = (datetime.now() - inicio).total_seconds()

    print("\n" + "=" * 60)
    print("  RELATÓRIO DE EXECUÇÃO — PokeAPI")
    print("=" * 60)
    print(f"  Status:        {'✅ Sucesso' if not info.has_failed_jobs else '❌ Falha'}")
    print(f"  Duração:       {duracao:.2f}s")
    print(f"  Destino:       s3://bronze/pokeapi/")
    print(f"  Formato:       Parquet + Snappy")
    print()
    print("  Detalhes da carga:")
    print(info)
    print("=" * 60)

    return info


if __name__ == "__main__":
    executar_pipeline()
```

Execute o pipeline da PokeAPI:

```bash
python scripts/ingest_pokemon.py
```

> **Tempo estimado:** A extração de 300 pokémons com delay de 0,1s entre requisições leva aproximadamente 3 a 5 minutos. Este tempo é intencional para demonstrar o respeito ao rate limit de APIs públicas — uma prática obrigatória em ambientes de produção.

---

### Passo 5 — Comparação dos Dois Pipelines

Após executar ambos os pipelines, compare as estruturas geradas no MinIO:

```python
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
```

```bash
python scripts/comparar_pipelines.py
```

---

### Verificação Final da Atividade 2

Ao concluir esta atividade, o aluno deve ser capaz de:

1. Explicar a diferença entre o Airbyte (plataforma visual, conectores pré-construídos) e o `dlt` (biblioteca Python, pipelines customizados)
2. Descrever o padrão de paginação "list + detail" e implementá-lo em Python
3. Explicar por que adicionamos metadados `_fonte`, `_ingerido_em` e `_versao_api` a cada registro na camada Bronze
4. Verificar que os dados de ambas as APIs estão disponíveis no MinIO em formato Parquet
5. Ler e explorar os dados ingeridos com Pandas diretamente do MinIO

---

## Atividade 3 — Organização da Camada Bronze com Particionamento

### Objetivo

Implementar e consolidar as boas práticas de organização da camada Bronze: particionamento lógico por data de ingestão, convenção de nomenclatura de caminhos, adição de metadados de rastreabilidade e criação de um manifesto de ingestão que registra cada execução de pipeline. Estas práticas são fundamentais para a manutenibilidade e auditabilidade de Data Lakes em produção.

### Contexto

Em Data Lakes de produção com petabytes de dados, a organização dos arquivos no armazenamento de objetos tem impacto direto na performance de leitura e no custo de processamento. O **particionamento por data** (`ano=YYYY/mes=MM/dia=DD`) é o padrão mais comum porque a maioria das consultas analíticas filtra por período de tempo. Ferramentas como Apache Spark e DuckDB conseguem ignorar automaticamente partições que não correspondem ao filtro da consulta — uma técnica chamada **partition pruning** — reduzindo drasticamente a quantidade de dados lidos do disco[[3]](#ref3).

---

### Passo 1 — Convenção de Nomenclatura para a Camada Bronze

Antes de implementar o particionamento, é importante estabelecer e documentar a convenção de nomenclatura que será seguida em todo o curso. Crie o arquivo de documentação:

```bash
cat > ~/engenharia-dados-curso/docs/convencao_camada_bronze.md << 'EOF'
# Convenção de Nomenclatura — Camada Bronze

## Estrutura de Caminhos

```
bronze/
└── {sistema_origem}/
    └── {entidade}/
        └── ano={YYYY}/
            └── mes={MM}/
                └── dia={DD}/
                    └── {entidade}_{timestamp_unix}.parquet
```

## Exemplos

```
bronze/
├── restcountries_api/
│   └── countries/
│       └── ano=2024/mes=01/dia=15/
│           └── countries_1705363200.parquet
├── pokeapi/
│   └── pokemon/
│       └── ano=2024/mes=01/dia=15/
│           └── pokemon_1705363200.parquet
└── ecommerce_db/
    └── orders/
        └── ano=2024/mes=01/dia=15/
            └── orders_1705363200.parquet
```

## Regras

1. Nomes em snake_case, letras minúsculas, sem espaços ou caracteres especiais.
2. O timestamp no nome do arquivo é Unix timestamp (segundos desde epoch).
3. Particionamento obrigatório por ano/mês/dia da DATA DE INGESTÃO (não da data do dado).
4. Cada arquivo deve conter os metadados: _fonte, _ingerido_em, _versao_schema.
5. Nunca sobrescrever arquivos existentes na camada Bronze — apenas acrescentar.
EOF

mkdir -p ~/engenharia-dados-curso/docs
```

---

### Passo 2 — Classe Utilitária para Ingestão na Camada Bronze

Crie uma classe reutilizável que encapsula todas as boas práticas de ingestão na camada Bronze. Esta classe será utilizada em todos os pipelines das aulas seguintes:

```python
# scripts/bronze_writer.py
"""
Utilitário para gravação padronizada na camada Bronze do Data Lake.

Encapsula as boas práticas de:
  - Particionamento por data de ingestão
  - Adição de metadados de rastreabilidade
  - Nomenclatura padronizada de arquivos
  - Registro de manifesto de ingestão
  - Verificação de integridade (contagem de registros)
"""

import pandas as pd
import boto3
import json
import io
import hashlib
import logging
from datetime import datetime, timezone
from pathlib import PurePosixPath
from typing import Optional

logger = logging.getLogger(__name__)


class BronzeWriter:
    """
    Gerencia a gravação padronizada de dados na camada Bronze do Data Lake.

    Uso:
        writer = BronzeWriter()
        resultado = writer.gravar(
            df=meu_dataframe,
            sistema_origem="pokeapi",
            entidade="pokemon",
        )
        print(resultado["caminho_objeto"])
    """

    # Configurações padrão do MinIO local
    ENDPOINT = "http://localhost:9000"
    ACCESS_KEY = "minioadmin"
    SECRET_KEY = "minioadmin123"
    BUCKET = "bronze"

    def __init__(
        self,
        endpoint: str = ENDPOINT,
        access_key: str = ACCESS_KEY,
        secret_key: str = SECRET_KEY,
        bucket: str = BUCKET,
    ):
        self.bucket = bucket
        self.client = boto3.client(
            "s3",
            endpoint_url=endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name="us-east-1",
        )

    def _construir_caminho(
        self,
        sistema_origem: str,
        entidade: str,
        timestamp: datetime,
    ) -> str:
        """
        Constrói o caminho S3 seguindo a convenção de particionamento.

        Exemplo de saída:
            pokeapi/pokemon/ano=2024/mes=01/dia=15/pokemon_1705363200.parquet
        """
        particao = (
            f"ano={timestamp.year}/"
            f"mes={timestamp.month:02d}/"
            f"dia={timestamp.day:02d}"
        )
        nome_arquivo = f"{entidade}_{int(timestamp.timestamp())}.parquet"
        return str(PurePosixPath(sistema_origem) / entidade / particao / nome_arquivo)

    def _adicionar_metadados(
        self,
        df: pd.DataFrame,
        sistema_origem: str,
        versao_schema: str,
        timestamp: datetime,
    ) -> pd.DataFrame:
        """
        Adiciona colunas de metadados de rastreabilidade ao DataFrame.
        Estas colunas são prefixadas com '_' para diferenciá-las dos dados originais.
        """
        df = df.copy()
        df["_fonte"] = sistema_origem
        df["_ingerido_em"] = timestamp.isoformat()
        df["_versao_schema"] = versao_schema
        df["_particao_data"] = timestamp.strftime("%Y-%m-%d")
        return df

    def _calcular_checksum(self, buffer: bytes) -> str:
        """Calcula o hash MD5 do arquivo para verificação de integridade."""
        return hashlib.md5(buffer).hexdigest()

    def gravar(
        self,
        df: pd.DataFrame,
        sistema_origem: str,
        entidade: str,
        versao_schema: str = "1.0",
        compressao: str = "snappy",
        timestamp: Optional[datetime] = None,
    ) -> dict:
        """
        Grava um DataFrame Pandas na camada Bronze do MinIO.

        Args:
            df:              DataFrame com os dados a serem gravados.
            sistema_origem:  Identificador do sistema de origem (ex: 'pokeapi').
            entidade:        Nome da entidade/tabela (ex: 'pokemon').
            versao_schema:   Versão do schema dos dados (para controle de evolução).
            compressao:      Algoritmo de compressão Parquet ('snappy' ou 'zstd').
            timestamp:       Data/hora de ingestão. Se None, usa o momento atual.

        Returns:
            Dicionário com metadados da operação de gravação.
        """
        if timestamp is None:
            timestamp = datetime.now(timezone.utc)

        # Adicionar metadados de rastreabilidade
        df_com_metadados = self._adicionar_metadados(
            df, sistema_origem, versao_schema, timestamp
        )

        # Construir o caminho do objeto no MinIO
        caminho_objeto = self._construir_caminho(sistema_origem, entidade, timestamp)

        # Serializar para Parquet em memória
        buffer = io.BytesIO()
        df_com_metadados.to_parquet(buffer, index=False, compression=compressao)
        buffer.seek(0)
        dados_bytes = buffer.read()

        # Calcular checksum para verificação de integridade
        checksum = self._calcular_checksum(dados_bytes)

        # Upload para o MinIO
        self.client.put_object(
            Bucket=self.bucket,
            Key=caminho_objeto,
            Body=dados_bytes,
            ContentType="application/octet-stream",
            Metadata={
                "fonte": sistema_origem,
                "entidade": entidade,
                "registros": str(len(df)),
                "checksum_md5": checksum,
                "versao_schema": versao_schema,
            },
        )

        resultado = {
            "caminho_objeto": f"s3://{self.bucket}/{caminho_objeto}",
            "registros": len(df),
            "colunas": len(df_com_metadados.columns),
            "tamanho_bytes": len(dados_bytes),
            "checksum_md5": checksum,
            "compressao": compressao,
            "timestamp_ingestao": timestamp.isoformat(),
        }

        logger.info(
            f"✅ Bronze gravado: {caminho_objeto} "
            f"({resultado['registros']:,} registros, "
            f"{resultado['tamanho_bytes'] / 1024:.1f} KB)"
        )

        return resultado

    def registrar_manifesto(self, execucao: dict) -> None:
        """
        Registra um manifesto JSON com os metadados de cada execução de pipeline.
        O manifesto é armazenado em bronze/_manifesto/ e serve como log de auditoria.
        """
        timestamp = datetime.now(timezone.utc)
        chave_manifesto = (
            f"_manifesto/"
            f"ano={timestamp.year}/mes={timestamp.month:02d}/dia={timestamp.day:02d}/"
            f"manifesto_{int(timestamp.timestamp())}.json"
        )

        self.client.put_object(
            Bucket=self.bucket,
            Key=chave_manifesto,
            Body=json.dumps(execucao, indent=2, ensure_ascii=False, default=str),
            ContentType="application/json",
        )

        logger.info(f"📋 Manifesto registrado: {chave_manifesto}")

    def listar_particoes(self, sistema_origem: str, entidade: str) -> list:
        """
        Lista todas as partições disponíveis para uma entidade específica.
        Útil para verificar a cobertura temporal dos dados na camada Bronze.
        """
        prefixo = f"{sistema_origem}/{entidade}/"
        response = self.client.list_objects_v2(
            Bucket=self.bucket, Prefix=prefixo, Delimiter="/"
        )

        particoes = []
        # Navegar recursivamente pelas partições
        for prefix in response.get("CommonPrefixes", []):
            sub_response = self.client.list_objects_v2(
                Bucket=self.bucket, Prefix=prefix["Prefix"], Delimiter="/"
            )
            for sub_prefix in sub_response.get("CommonPrefixes", []):
                sub_sub_response = self.client.list_objects_v2(
                    Bucket=self.bucket, Prefix=sub_prefix["Prefix"]
                )
                for obj in sub_sub_response.get("Contents", []):
                    if obj["Key"].endswith(".parquet"):
                        particoes.append({
                            "caminho": obj["Key"],
                            "tamanho_bytes": obj["Size"],
                            "ultima_modificacao": obj["LastModified"],
                        })

        return particoes
```

---

### Passo 3 — Reingesta com Particionamento Correto

Utilize a classe `BronzeWriter` para reingerir os dados da REST Countries API e da PokeAPI, desta vez seguindo a convenção de particionamento padronizada:

```python
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
    params={"fields": "name,cca2,cca3,region,subregion,population,area,capital"},
    timeout=30,
)
resposta.raise_for_status()

# Normalizar o campo 'name' (é um objeto aninhado)
paises_raw = resposta.json()
paises_normalizados = []
for p in paises_raw:
    paises_normalizados.append({
        "cca2": p.get("cca2"),
        "cca3": p.get("cca3"),
        "nome_comum": p.get("name", {}).get("common"),
        "nome_oficial": p.get("name", {}).get("official"),
        "regiao": p.get("region"),
        "sub_regiao": p.get("subregion"),
        "populacao": p.get("population"),
        "area_km2": p.get("area"),
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
```

Execute o script:

```bash
python scripts/reingerir_com_particionamento.py
```

---

### Passo 4 — Verificação do Manifesto de Ingestão

O manifesto de ingestão é um registro de auditoria que documenta cada execução de pipeline. Verifique os manifestos criados:

```python
# scripts/verificar_manifesto.py
"""
Lê e exibe os manifestos de ingestão registrados na camada Bronze.
O manifesto é a base para auditoria e rastreabilidade do Data Lake.
"""

import boto3
import json

client = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="minioadmin",
    aws_secret_access_key="minioadmin123",
    region_name="us-east-1",
)

response = client.list_objects_v2(Bucket="bronze", Prefix="_manifesto/")
manifestos = sorted(
    [obj["Key"] for obj in response.get("Contents", []) if obj["Key"].endswith(".json")],
    reverse=True,  # Mais recentes primeiro
)

print(f"Manifestos de ingestão encontrados: {len(manifestos)}\n")

for chave in manifestos[:5]:  # Exibir os 5 mais recentes
    obj = client.get_object(Bucket="bronze", Key=chave)
    manifesto = json.loads(obj["Body"].read().decode("utf-8"))
    print(f"📋 {chave}")
    print(f"   Pipeline:   {manifesto.get('pipeline')}")
    print(f"   Executado:  {manifesto.get('execucao_em')}")
    resultado = manifesto.get("resultado", {})
    print(f"   Registros:  {resultado.get('registros', 'N/A'):,}")
    print(f"   Tamanho:    {resultado.get('tamanho_bytes', 0) / 1024:.1f} KB")
    print(f"   Checksum:   {resultado.get('checksum_md5', 'N/A')}")
    print()
```

```bash
python scripts/verificar_manifesto.py
```

---

### Passo 5 — Leitura com Partition Pruning

Demonstre como o particionamento por data permite leituras eficientes, ignorando partições desnecessárias:

```python
# scripts/demonstrar_partition_pruning.py
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
```

```bash
python scripts/demonstrar_partition_pruning.py
```

---

### Verificação Final da Atividade 3

Ao concluir esta atividade, o aluno deve ser capaz de:

1. Explicar a convenção de particionamento `ano=YYYY/mes=MM/dia=DD` e por que ela é o padrão da indústria
2. Utilizar a classe `BronzeWriter` para gravar qualquer DataFrame na camada Bronze com metadados padronizados
3. Verificar no console do MinIO (`http://localhost:9001`) a estrutura de diretórios particionada
4. Ler os manifestos de ingestão e explicar sua importância para auditoria e rastreabilidade
5. Demonstrar o conceito de partition pruning lendo apenas a partição de uma data específica

---

## Consolidação da Aula 2

As três atividades desta atividade construíram os primeiros pipelines de ingestão reais do curso. O Airbyte demonstrou como uma plataforma visual pode conectar dezenas de fontes sem código, enquanto o `dlt` mostrou como construir pipelines customizados em Python com controle total sobre a lógica de extração, paginação e normalização. A classe `BronzeWriter` encapsula todas as boas práticas de organização da camada Bronze e será reutilizada nas aulas seguintes.

Na **Aula 3**, os dados armazenados na camada Bronze serão processados com Apache Spark e DuckDB, e convertidos para os formatos de tabela modernos Apache Iceberg e Delta Lake, que adicionam funcionalidades de banco de dados relacional (transações ACID, time travel, evolução de schema) ao Data Lake.

---

# Aula 3 — Atividades Práticas
## Processamento Distribuído e Formatos de Tabela (Lakehouse)

**Pré-requisitos:** Conclusão das Atividades 1 e 2 — ambiente Docker operacional, MinIO rodando com dados da REST Countries API, PokeAPI e dataset sintético de e-commerce na camada Bronze.

---

## Visão Geral das Atividades

Esta aula marca a transição do paradigma de armazenamento para o de **processamento**. Os dados que foram ingeridos e preservados na camada Bronze nas aulas anteriores agora serão lidos, processados e transformados por dois motores analíticos complementares. A **Atividade 1** introduz o Apache Spark — o motor de processamento distribuído padrão da indústria — demonstrando como ele lê dados diretamente do MinIO e executa operações de DataFrame em escala. A **Atividade 2** apresenta o DuckDB, um motor OLAP in-process que executa SQL analítico de alta performance diretamente sobre arquivos Parquet, sem necessidade de servidor. A **Atividade 3** eleva o Data Lake ao nível de **Data Lakehouse**, convertendo os dados para o formato Apache Iceberg e demonstrando na prática as transações ACID, evolução de schema e *time travel* — funcionalidades que antes eram exclusivas de bancos de dados relacionais.

| Atividade | Tema | Duração Estimada | Ferramentas |
|---|---|---|---|
| 1 | Introdução ao PySpark com MinIO | 45 min | PySpark 3.5, Docker, MinIO, Jupyter |
| 2 | Consultas Analíticas com DuckDB | 35 min | DuckDB, Python, SQL, MinIO |
| 3 | Data Lakehouse com Apache Iceberg | 40 min | PyIceberg, DuckDB, MinIO, Python |

> **Contexto arquitetural:** As três atividades desta aula operam sobre a camada Bronze (leitura) e produzem resultados que serão a base da camada Silver. O processamento realizado aqui é exploratório e de validação — a transformação definitiva e documentada para a camada Silver ocorrerá na Aula 4 com o dbt.

---

## Atividade 1 — Introdução ao PySpark com MinIO

### Objetivo

Configurar um ambiente Apache Spark local via Docker, conectá-lo ao MinIO como fonte de dados S3-compatível e executar as operações fundamentais de DataFrame em PySpark: leitura de Parquet, filtros, seleções, agrupamentos, joins e gravação de resultados. O dataset de e-commerce sintético gerado na Aula 1 (1 milhão de registros) será utilizado para demonstrar o poder do processamento distribuído.

### Contexto

O Apache Spark é o motor de processamento distribuído mais amplamente utilizado na indústria para cargas de trabalho de Big Data[[1]](#ref1). Sua arquitetura divide os dados em partições que são processadas em paralelo por múltiplos executores (workers), permitindo escalar horizontalmente para petabytes de dados. Mesmo em modo local (single-node), o Spark demonstra ganhos de performance sobre o Pandas para datasets acima de alguns gigabytes, pois utiliza todos os núcleos de CPU disponíveis e executa operações de forma lazy (avaliação preguiçosa) — construindo um plano de execução otimizado antes de processar qualquer dado.

---

### Passo 1 — Configuração do PySpark via Docker

O Spark requer a JVM (Java Virtual Machine) e configurações específicas para se conectar ao MinIO. A forma mais simples de ter um ambiente Spark funcional é utilizando a imagem oficial do Jupyter com PySpark pré-instalado:

```bash
cd ~/engenharia-dados-curso/docker

# Adicionar o serviço Spark/Jupyter ao docker-compose.yml existente
cat >> docker-compose.yml << 'EOF'

  # Jupyter com PySpark e suporte a S3 (MinIO)
  spark-jupyter:
    image: jupyter/pyspark-notebook:spark-3.5.0
    container_name: spark-jupyter
    ports:
      - "8888:8888"   # Interface Jupyter
      - "4040:4040"   # Spark UI (monitoramento de jobs)
    environment:
      JUPYTER_ENABLE_LAB: "yes"
      SPARK_OPTS: "--driver-java-options=-Xms1g --driver-java-options=-Xmx4g"
    volumes:
      - ../notebooks:/home/jovyan/notebooks
      - ../scripts:/home/jovyan/scripts
      - ../data:/home/jovyan/data
    networks:
      - default
EOF

# Iniciar o serviço Spark/Jupyter
docker compose up -d spark-jupyter

# Aguardar a inicialização (pode levar 1-2 minutos)
sleep 30

# Obter o token de acesso do Jupyter
docker logs spark-jupyter 2>&1 | grep "token=" | tail -1
```

Acesse o Jupyter Lab em `http://localhost:8888` utilizando o token exibido no terminal. Crie um novo notebook em `notebooks/` com o nome `aula3_pyspark.ipynb`.

---

### Passo 2 — Configuração da Sessão Spark com Conexão ao MinIO

A configuração do Spark para se conectar ao MinIO requer a especificação de pacotes adicionais (hadoop-aws e aws-java-sdk) e as credenciais de acesso S3. Execute as células abaixo no notebook:

```python
# Célula 1 — Configuração da SparkSession com suporte ao MinIO
import os
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import (
    StructType, StructField, StringType, IntegerType,
    DoubleType, TimestampType
)

# Endereço do MinIO acessível de dentro do contêiner Docker
# "host.docker.internal" resolve para o IP do host a partir do contêiner
MINIO_ENDPOINT = "http://host.docker.internal:9000"
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin123"

# Criar a SparkSession com os pacotes necessários para S3
spark = (
    SparkSession.builder
    .appName("DataEngineeringCourse-Aula3")
    .master("local[*]")  # Usar todos os núcleos de CPU disponíveis
    .config(
        "spark.jars.packages",
        "org.apache.hadoop:hadoop-aws:3.3.4,"
        "com.amazonaws:aws-java-sdk-bundle:1.12.262"
    )
    # Configurações do conector S3A para MinIO
    .config("spark.hadoop.fs.s3a.endpoint", MINIO_ENDPOINT)
    .config("spark.hadoop.fs.s3a.access.key", MINIO_ACCESS_KEY)
    .config("spark.hadoop.fs.s3a.secret.key", MINIO_SECRET_KEY)
    .config("spark.hadoop.fs.s3a.path.style.access", "true")
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
    # Otimizações de performance
    .config("spark.sql.adaptive.enabled", "true")
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
    .config("spark.ui.port", "4040")
    .getOrCreate()
)

# Configurar nível de log para reduzir verbosidade
spark.sparkContext.setLogLevel("WARN")

print(f"✅ SparkSession criada com sucesso!")
print(f"   Versão do Spark: {spark.version}")
print(f"   Master: {spark.sparkContext.master}")
print(f"   Núcleos disponíveis: {spark.sparkContext.defaultParallelism}")
print(f"\n   Spark UI disponível em: http://localhost:4040")
```

> **Nota:** Na primeira execução, o Spark fará download dos pacotes `hadoop-aws` e `aws-java-sdk-bundle` (~150 MB). Esse processo pode levar alguns minutos. As execuções subsequentes utilizarão o cache local.

---

### Passo 3 — Leitura de Dados Parquet do MinIO

```python
# Célula 2 — Leitura do dataset de e-commerce da camada Bronze
import time

# Caminho S3A para os arquivos Parquet no MinIO
# O prefixo s3a:// indica o conector Hadoop para S3
CAMINHO_ECOMMERCE = "s3a://bronze/ecommerce_sintetico/"

print("Lendo dataset de e-commerce do MinIO...")
inicio = time.time()

df_pedidos = spark.read.parquet(CAMINHO_ECOMMERCE)

# Nota: a leitura é LAZY — o Spark ainda não processou nenhum dado
# O schema é inferido dos metadados do Parquet (sem ler os dados)
duracao = time.time() - inicio

print(f"✅ Schema inferido em {duracao:.2f}s (leitura lazy — dados ainda não carregados)")
print(f"\nSchema do DataFrame:")
df_pedidos.printSchema()
```

```python
# Célula 3 — Primeira ação: contar registros (força a execução do plano)
print("Contando registros (primeira ação — força execução do plano Spark)...")
inicio = time.time()

total_registros = df_pedidos.count()

duracao = time.time() - inicio
print(f"✅ Total de registros: {total_registros:,}")
print(f"   Tempo de execução: {duracao:.2f}s")
print(f"\n   Acesse o Spark UI em http://localhost:4040 para ver o plano de execução!")
```

```python
# Célula 4 — Exploração inicial do DataFrame
# show() é uma ação que força a execução e exibe os dados
print("Amostra dos dados (5 primeiras linhas):")
df_pedidos.show(5, truncate=False)

print(f"\nEstatísticas descritivas das colunas numéricas:")
df_pedidos.select(
    "valor_unitario", "quantidade", "valor_total"
).describe().show()
```

---

### Passo 4 — Operações Fundamentais de DataFrame

```python
# Célula 5 — Filtros e Seleções (equivalente ao WHERE e SELECT do SQL)

# Filtrar apenas pedidos concluídos com valor total acima de R$ 500
df_pedidos_premium = (
    df_pedidos
    .filter(
        (F.col("status_pedido") == "concluido") &
        (F.col("valor_total") > 500.0)
    )
    .select(
        "id_pedido",
        "id_cliente",
        "categoria",
        "valor_total",
        "regiao",
        "data_pedido",
    )
)

print("Pedidos concluídos com valor > R$ 500:")
print(f"  Total filtrado: {df_pedidos_premium.count():,} registros")
df_pedidos_premium.show(5)
```

```python
# Célula 6 — Agrupamentos e Agregações (equivalente ao GROUP BY do SQL)

# Receita total e ticket médio por categoria e região
df_receita_categoria = (
    df_pedidos
    .filter(F.col("status_pedido") == "concluido")
    .groupBy("categoria", "regiao")
    .agg(
        F.count("id_pedido").alias("total_pedidos"),
        F.sum("valor_total").alias("receita_total"),
        F.avg("valor_total").alias("ticket_medio"),
        F.countDistinct("id_cliente").alias("clientes_unicos"),
    )
    .withColumn("receita_total", F.round("receita_total", 2))
    .withColumn("ticket_medio", F.round("ticket_medio", 2))
    .orderBy(F.desc("receita_total"))
)

print("Receita por Categoria e Região (pedidos concluídos):")
df_receita_categoria.show(15)
```

```python
# Célula 7 — Funções de Janela (Window Functions)
# Calcular o ranking de receita por categoria dentro de cada região
from pyspark.sql.window import Window

janela_regiao = Window.partitionBy("regiao").orderBy(F.desc("receita_total"))

df_ranking = (
    df_receita_categoria
    .withColumn("ranking_na_regiao", F.rank().over(janela_regiao))
    .filter(F.col("ranking_na_regiao") <= 3)  # Top 3 categorias por região
    .orderBy("regiao", "ranking_na_regiao")
)

print("Top 3 categorias por receita em cada região:")
df_ranking.show(20)
```

```python
# Célula 8 — Criação de Colunas Derivadas e Transformações

df_enriquecido = (
    df_pedidos
    .withColumn(
        # Extrair o mês da data do pedido
        "mes_pedido", F.month("data_pedido")
    )
    .withColumn(
        # Extrair o ano
        "ano_pedido", F.year("data_pedido")
    )
    .withColumn(
        # Classificar o pedido por faixa de valor
        "faixa_valor",
        F.when(F.col("valor_total") < 100, "Baixo")
         .when(F.col("valor_total") < 500, "Médio")
         .when(F.col("valor_total") < 1500, "Alto")
         .otherwise("Premium")
    )
    .withColumn(
        # Flag para pedidos com avaliação positiva (4 ou 5 estrelas)
        "avaliacao_positiva",
        F.when(F.col("avaliacao_cliente") >= 4, True).otherwise(False)
    )
)

print("DataFrame enriquecido com colunas derivadas:")
df_enriquecido.select(
    "id_pedido", "valor_total", "faixa_valor",
    "mes_pedido", "ano_pedido", "avaliacao_positiva"
).show(10)
```

---

### Passo 5 — Plano de Execução e Otimização

```python
# Célula 9 — Visualização do Plano de Execução (Catalyst Optimizer)
# O Spark usa o Catalyst Optimizer para transformar o plano lógico
# em um plano físico otimizado antes de executar qualquer operação.

print("=== Plano de Execução Lógico (não otimizado) ===")
df_receita_categoria.explain(mode="simple")

print("\n=== Plano de Execução Físico (otimizado pelo Catalyst) ===")
df_receita_categoria.explain(mode="cost")
```

```python
# Célula 10 — Cache de DataFrames para Reutilização
# Quando um DataFrame é usado múltiplas vezes, o cache evita
# que o Spark releia os dados do MinIO a cada operação.

print("Armazenando DataFrame em cache...")
inicio = time.time()
df_pedidos.cache()
df_pedidos.count()  # Força a materialização do cache
duracao_cache = time.time() - inicio
print(f"  Cache materializado em {duracao_cache:.2f}s")

# Segunda contagem — agora vem do cache (muito mais rápida)
inicio = time.time()
df_pedidos.count()
duracao_cache_hit = time.time() - inicio
print(f"  Leitura do cache: {duracao_cache_hit:.4f}s")
print(f"  Speedup: {duracao_cache / duracao_cache_hit:.0f}x mais rápido com cache")
```

---

### Passo 6 — Gravação dos Resultados no MinIO

```python
# Célula 11 — Gravação do resultado processado de volta no MinIO
# Os resultados são gravados como Parquet particionado por categoria

CAMINHO_SAIDA = "s3a://bronze/ecommerce_processado/"

print(f"Gravando resultados em: {CAMINHO_SAIDA}")
inicio = time.time()

(
    df_enriquecido
    .filter(F.col("status_pedido") == "concluido")
    .write
    .mode("overwrite")
    .partitionBy("ano_pedido", "mes_pedido")  # Particionamento físico no S3
    .parquet(CAMINHO_SAIDA)
)

duracao = time.time() - inicio
print(f"✅ Dados gravados em {duracao:.2f}s")
print(f"   Particionado por: ano_pedido / mes_pedido")
print(f"   Formato: Parquet + Snappy (padrão do Spark)")

# Verificar os arquivos criados
df_verificacao = spark.read.parquet(CAMINHO_SAIDA)
print(f"\n   Registros gravados: {df_verificacao.count():,}")
print(f"   Partições físicas criadas:")
df_verificacao.select("ano_pedido", "mes_pedido").distinct().orderBy("ano_pedido", "mes_pedido").show(5)
```

---

### Verificação Final da Atividade 1

Ao concluir esta atividade, o aluno deve ser capaz de:

1. Criar uma `SparkSession` configurada para se conectar ao MinIO via protocolo S3A
2. Explicar a diferença entre **transformações** (lazy) e **ações** (eager) no Spark
3. Executar filtros, seleções, agrupamentos e funções de janela em PySpark
4. Visualizar o plano de execução do Catalyst Optimizer e explicar o que é *predicate pushdown*
5. Gravar DataFrames Spark de volta no MinIO com particionamento físico por colunas

---

## Atividade 2 — Consultas Analíticas com DuckDB

### Objetivo

Configurar o DuckDB e utilizá-lo para executar consultas SQL analíticas de alta performance diretamente sobre arquivos Parquet armazenados no MinIO, sem necessidade de carregar os dados em memória ou em um servidor de banco de dados. Esta atividade demonstra por que o DuckDB se tornou a ferramenta preferida para análise exploratória de dados em escala moderada, substituindo o Spark em muitos cenários modernos.

### Contexto

O DuckDB é um sistema de gerenciamento de banco de dados analítico *in-process* (OLAP) que executa dentro do processo Python, sem servidor externo[[2]](#ref2). Sua arquitetura colunar vetorizada permite processar dezenas de gigabytes de dados Parquet com performance comparável ao Spark, mas com configuração trivial — basta um `pip install duckdb`. O DuckDB suporta leitura direta de arquivos Parquet locais e remotos (S3/MinIO), além de integração nativa com DataFrames Pandas e Arrow.

A tabela abaixo compara os dois motores para ajudar na escolha da ferramenta certa para cada cenário:

| Critério | Apache Spark | DuckDB |
|---|---|---|
| **Escala de dados** | Terabytes a Petabytes | Gigabytes a Terabytes |
| **Configuração** | Complexa (JVM, cluster) | Trivial (`pip install`) |
| **Linguagem principal** | Python, Scala, Java | SQL, Python |
| **Modo de execução** | Distribuído (cluster) | In-process (single-node) |
| **Latência de startup** | Alta (segundos a minutos) | Baixa (milissegundos) |
| **Ideal para** | Pipelines de produção em escala | Análise exploratória, ETL moderado |

---

### Passo 1 — Instalação e Configuração do DuckDB

```bash
cd ~/engenharia-dados-curso
source .venv/bin/activate

# Instalar o DuckDB com suporte a httpfs (S3/MinIO)
pip install duckdb

# Verificar a instalação
python -c "import duckdb; print(f'DuckDB versão: {duckdb.__version__}')"
```

Crie um novo notebook `notebooks/aula3_duckdb.ipynb` no Jupyter Lab.

---

### Passo 2 — Configuração da Conexão com o MinIO

```python
# Célula 1 — Configuração do DuckDB com suporte ao MinIO
import duckdb
import pandas as pd
import time

# Criar uma conexão DuckDB persistente (o arquivo .duckdb armazena
# metadados e tabelas locais; os dados Parquet permanecem no MinIO)
con = duckdb.connect("../data/curso_analytics.duckdb")

# Instalar e carregar a extensão httpfs (HTTP File System)
# Necessária para acessar arquivos em S3/MinIO
con.execute("INSTALL httpfs;")
con.execute("LOAD httpfs;")

# Configurar as credenciais do MinIO
# O DuckDB usa as mesmas configurações do protocolo S3
con.execute("""
    SET s3_endpoint = 'localhost:9000';
    SET s3_access_key_id = 'minioadmin';
    SET s3_secret_access_key = 'minioadmin123';
    SET s3_use_ssl = false;
    SET s3_url_style = 'path';
""")

print("✅ DuckDB configurado com suporte ao MinIO!")
print(f"   Versão: {duckdb.__version__}")
print(f"   Banco de dados local: ../data/curso_analytics.duckdb")
```

---

### Passo 3 — Consultas Diretas sobre Parquet no MinIO

```python
# Célula 2 — Consulta direta sobre arquivo Parquet no MinIO
# Não é necessário importar os dados — o DuckDB lê diretamente do S3!

print("Consultando Parquet diretamente no MinIO (sem importação):\n")

inicio = time.time()

resultado = con.execute("""
    SELECT
        categoria,
        COUNT(*)                          AS total_pedidos,
        ROUND(SUM(valor_total), 2)        AS receita_total,
        ROUND(AVG(valor_total), 2)        AS ticket_medio,
        ROUND(MIN(valor_total), 2)        AS menor_pedido,
        ROUND(MAX(valor_total), 2)        AS maior_pedido
    FROM read_parquet('s3://bronze/ecommerce_sintetico/**/*.parquet')
    WHERE status_pedido = 'concluido'
    GROUP BY categoria
    ORDER BY receita_total DESC
""").df()  # .df() converte o resultado para um DataFrame Pandas

duracao = time.time() - inicio

print(f"Tempo de execução: {duracao:.3f}s  (lendo 1.000.000 registros do MinIO!)\n")
print(resultado.to_string(index=False))
```

```python
# Célula 3 — Consulta com múltiplas fontes Parquet (JOIN entre datasets)
# DuckDB pode fazer JOIN entre arquivos Parquet de diferentes origens

resultado_join = con.execute("""
    WITH pedidos AS (
        SELECT
            regiao,
            categoria,
            status_pedido,
            valor_total,
            avaliacao_cliente
        FROM read_parquet('s3://bronze/ecommerce_sintetico/**/*.parquet')
    ),
    resumo_regiao AS (
        SELECT
            regiao,
            COUNT(*)                           AS total_pedidos,
            ROUND(SUM(valor_total), 2)         AS receita_total,
            ROUND(AVG(valor_total), 2)         AS ticket_medio,
            ROUND(
                100.0 * COUNT(*) FILTER (WHERE status_pedido = 'cancelado')
                / COUNT(*), 2
            )                                  AS taxa_cancelamento_pct,
            ROUND(
                AVG(avaliacao_cliente)
                FILTER (WHERE avaliacao_cliente IS NOT NULL), 2
            )                                  AS nota_media_clientes
        FROM pedidos
        GROUP BY regiao
    )
    SELECT *
    FROM resumo_regiao
    ORDER BY receita_total DESC
""").df()

print("Resumo por Região — Receita, Cancelamentos e Satisfação:")
print(resultado_join.to_string(index=False))
```

---

### Passo 4 — Análise Temporal com Funções de Janela

```python
# Célula 4 — Análise de tendência temporal com window functions SQL

resultado_temporal = con.execute("""
    WITH vendas_mensais AS (
        SELECT
            DATE_TRUNC('month', data_pedido)   AS mes,
            categoria,
            COUNT(*)                           AS pedidos_mes,
            ROUND(SUM(valor_total), 2)         AS receita_mes
        FROM read_parquet('s3://bronze/ecommerce_sintetico/**/*.parquet')
        WHERE status_pedido = 'concluido'
        GROUP BY 1, 2
    ),
    com_crescimento AS (
        SELECT
            mes,
            categoria,
            pedidos_mes,
            receita_mes,
            LAG(receita_mes) OVER (
                PARTITION BY categoria
                ORDER BY mes
            )                                  AS receita_mes_anterior,
            ROUND(
                100.0 * (receita_mes - LAG(receita_mes) OVER (
                    PARTITION BY categoria ORDER BY mes
                )) / NULLIF(LAG(receita_mes) OVER (
                    PARTITION BY categoria ORDER BY mes
                ), 0), 2
            )                                  AS crescimento_pct
        FROM vendas_mensais
    )
    SELECT *
    FROM com_crescimento
    WHERE mes >= '2022-01-01'
      AND mes < '2022-04-01'   -- Primeiros 3 meses para visualização
    ORDER BY categoria, mes
""").df()

print("Crescimento Mensal de Receita por Categoria (Jan-Mar 2022):")
print(resultado_temporal.to_string(index=False))
```

---

### Passo 5 — Criação de Views Persistentes

```python
# Célula 5 — Criar views persistentes no DuckDB
# As views ficam salvas no arquivo .duckdb e podem ser reutilizadas
# em sessões futuras sem reconfigurar as credenciais S3

con.execute("""
    CREATE OR REPLACE VIEW vw_pedidos_bronze AS
    SELECT *
    FROM read_parquet('s3://bronze/ecommerce_sintetico/**/*.parquet')
""")

con.execute("""
    CREATE OR REPLACE VIEW vw_countries_bronze AS
    SELECT *
    FROM read_parquet('s3://bronze/restcountries_api/**/*.parquet')
""")

con.execute("""
    CREATE OR REPLACE VIEW vw_pokemon_bronze AS
    SELECT *
    FROM read_parquet('s3://bronze/pokeapi/**/*.parquet')
""")

# Verificar as views criadas
views = con.execute("""
    SELECT table_name, table_type
    FROM information_schema.tables
    WHERE table_schema = 'main'
    ORDER BY table_name
""").df()

print("Views e tabelas disponíveis no DuckDB:")
print(views.to_string(index=False))
```

```python
# Célula 6 — Consulta usando as views criadas
# Agora podemos consultar os dados como se fossem tabelas locais

resultado_pokemon = con.execute("""
    SELECT
        tipo_primario,
        COUNT(*)                        AS total_pokemon,
        ROUND(AVG(hp_base), 1)          AS hp_medio,
        ROUND(AVG(ataque_base), 1)      AS ataque_medio,
        ROUND(AVG(defesa_base), 1)      AS defesa_media,
        MAX(nome)                       AS exemplo
    FROM vw_pokemon_bronze
    WHERE tipo_primario IS NOT NULL
    GROUP BY tipo_primario
    ORDER BY hp_medio DESC
    LIMIT 10
""").df()

print("Top 10 tipos de Pokémon por HP médio:")
print(resultado_pokemon.to_string(index=False))
```

---

### Passo 6 — Exportação de Resultados para Parquet

```python
# Célula 7 — Exportar resultado de consulta diretamente para Parquet no MinIO
# O DuckDB pode escrever resultados diretamente em S3 com COPY TO

con.execute("""
    COPY (
        SELECT
            categoria,
            regiao,
            DATE_TRUNC('month', data_pedido)  AS mes_referencia,
            COUNT(*)                          AS total_pedidos,
            ROUND(SUM(valor_total), 2)        AS receita_total,
            ROUND(AVG(valor_total), 2)        AS ticket_medio,
            COUNT(DISTINCT id_cliente)        AS clientes_unicos
        FROM vw_pedidos_bronze
        WHERE status_pedido = 'concluido'
        GROUP BY 1, 2, 3
        ORDER BY mes_referencia, categoria, regiao
    )
    TO 's3://bronze/ecommerce_agregado/resumo_mensal.parquet'
    (FORMAT PARQUET, COMPRESSION SNAPPY)
""")

# Verificar o arquivo criado
info = con.execute("""
    SELECT COUNT(*) AS linhas, MIN(mes_referencia) AS inicio, MAX(mes_referencia) AS fim
    FROM read_parquet('s3://bronze/ecommerce_agregado/resumo_mensal.parquet')
""").df()

print("✅ Arquivo exportado para o MinIO!")
print(info.to_string(index=False))
```

---

### Verificação Final da Atividade 2

Ao concluir esta atividade, o aluno deve ser capaz de:

1. Configurar o DuckDB com a extensão `httpfs` para acessar arquivos Parquet no MinIO
2. Executar consultas SQL analíticas complexas (GROUP BY, CTEs, window functions) diretamente sobre Parquet no S3, sem importar os dados
3. Criar views persistentes no DuckDB que encapsulam a leitura dos arquivos S3
4. Comparar o tempo de execução do DuckDB com o Spark para o mesmo conjunto de dados e identificar quando cada ferramenta é mais adequada
5. Exportar resultados de consultas diretamente para Parquet no MinIO com `COPY TO`

---

## Atividade 3 — Data Lakehouse com Apache Iceberg

### Objetivo

Converter dados da camada Bronze para o formato **Apache Iceberg**, transformando o Data Lake em um **Data Lakehouse** com suporte a transações ACID, evolução de schema e *time travel*. Esta atividade demonstra como o Iceberg resolve os problemas clássicos de consistência de dados em Data Lakes — como leituras inconsistentes durante escritas e a impossibilidade de atualizar ou deletar registros individuais.

### Contexto

O Apache Iceberg é um formato de tabela aberto para datasets analíticos de grande escala[[3]](#ref3). Diferentemente do Parquet puro (que é apenas um formato de arquivo), o Iceberg é uma **especificação de tabela** que adiciona uma camada de metadados sobre os arquivos Parquet, habilitando:

| Funcionalidade | Parquet Puro | Apache Iceberg |
|---|---|---|
| **Transações ACID** | ❌ Não | ✅ Sim (snapshot isolation) |
| **Atualização de registros** | ❌ Não (reescrever tudo) | ✅ Sim (merge-on-read ou copy-on-write) |
| **Deleção de registros** | ❌ Não | ✅ Sim |
| **Time Travel** | ❌ Não | ✅ Sim (consultar versões anteriores) |
| **Evolução de schema** | ❌ Não | ✅ Sim (adicionar/renomear colunas) |
| **Partition Evolution** | ❌ Não | ✅ Sim (mudar estratégia sem reescrever) |
| **Leituras concorrentes** | ✅ Sim | ✅ Sim |

---

### Passo 1 — Instalação das Dependências do Iceberg

```bash
cd ~/engenharia-dados-curso
source .venv/bin/activate

# Instalar PyIceberg com suporte a S3 e DuckDB
pip install "pyiceberg[s3fs,duckdb,pandas]"

# Verificar a instalação
python -c "import pyiceberg; print(f'PyIceberg versão: {pyiceberg.__version__}')"
```

Crie um novo notebook `notebooks/aula3_iceberg.ipynb`.

---

### Passo 2 — Configuração do Catálogo Iceberg

O Iceberg requer um **catálogo** para gerenciar os metadados das tabelas (localização dos arquivos, histórico de snapshots, schema atual). Para o ambiente local, utilizaremos o catálogo baseado em arquivo SQL (SQLite), que armazena os metadados localmente:

```python
# Célula 1 — Configuração do Catálogo Iceberg
from pyiceberg.catalog.sql import SqlCatalog
import pyarrow as pa
import pandas as pd
import os
from datetime import datetime, timezone

# Criar o diretório para os metadados do catálogo
os.makedirs("../data/iceberg_catalog", exist_ok=True)

# Configurar o catálogo SQLite local
# Em produção, o catálogo seria um banco de dados externo (PostgreSQL, Hive Metastore)
# ou um serviço gerenciado (AWS Glue, Nessie, Polaris)
catalog = SqlCatalog(
    "curso_lakehouse",
    **{
        "uri": "sqlite:///../data/iceberg_catalog/catalog.db",
        "warehouse": "s3://silver",  # As tabelas Iceberg serão armazenadas no bucket silver
        "s3.endpoint": "http://localhost:9000",
        "s3.access-key-id": "minioadmin",
        "s3.secret-access-key": "minioadmin123",
        "s3.path-style-access": "true",
    },
)

# Criar o namespace (equivalente a um schema/database)
try:
    catalog.create_namespace("bronze_processado")
    print("✅ Namespace 'bronze_processado' criado!")
except Exception:
    print("ℹ️  Namespace já existe, continuando...")

print(f"\nNamespaces disponíveis: {catalog.list_namespaces()}")
```

### Final da aula de 21/05/2026

---

### Passo 3 — Criação de uma Tabela Iceberg

```python
# Célula 2 — Definição do schema e criação da tabela Iceberg

from pyiceberg.schema import Schema
from pyiceberg.types import (
    NestedField, IntegerType, StringType, DoubleType,
    TimestampType, BooleanType, LongType
)
from pyiceberg.partitioning import PartitionSpec, PartitionField
from pyiceberg.transforms import MonthTransform, IdentityTransform

# Definir o schema da tabela (fortemente tipado)
schema_pedidos = Schema(
    NestedField(field_id=1,  name="id_pedido",      field_type=LongType(),      required=True),
    NestedField(field_id=2,  name="id_cliente",     field_type=LongType(),      required=True),
    NestedField(field_id=3,  name="id_produto",     field_type=LongType(),      required=True),
    NestedField(field_id=4,  name="categoria",      field_type=StringType(),    required=False),
    NestedField(field_id=5,  name="valor_unitario", field_type=DoubleType(),    required=False),
    NestedField(field_id=6,  name="quantidade",     field_type=IntegerType(),   required=False),
    NestedField(field_id=7,  name="valor_total",    field_type=DoubleType(),    required=False),
    NestedField(field_id=8,  name="status_pedido",  field_type=StringType(),    required=False),
    NestedField(field_id=9,  name="regiao",         field_type=StringType(),    required=False),
    NestedField(field_id=10, name="data_pedido",    field_type=TimestampType(), required=False),
    NestedField(field_id=11, name="avaliacao_cliente", field_type=IntegerType(), required=False),
    # Metadados de rastreabilidade
    NestedField(field_id=12, name="_fonte",         field_type=StringType(),    required=False),
    NestedField(field_id=13, name="_ingerido_em",   field_type=StringType(),    required=False),
)

# Definir a estratégia de particionamento
# MonthTransform particiona por mês da coluna data_pedido
spec_particao = PartitionSpec(
    PartitionField(
        source_id=10,           # Campo data_pedido (field_id=10)
        field_id=1000,
        transform=MonthTransform(),
        name="data_pedido_mes",
    )
)

# Criar a tabela no catálogo
NOME_TABELA = "bronze_processado.pedidos_ecommerce"

try:
    tabela = catalog.create_table(
        identifier=NOME_TABELA,
        schema=schema_pedidos,
        partition_spec=spec_particao,
        properties={
            "write.format.default": "parquet",
            "write.parquet.compression-codec": "snappy",
            "write.metadata.compression-codec": "gzip",
        },
    )
    print(f"✅ Tabela Iceberg criada: {NOME_TABELA}")
except Exception:
    tabela = catalog.load_table(NOME_TABELA)
    print(f"ℹ️  Tabela já existe, carregada: {NOME_TABELA}")

print(f"\nSchema da tabela:")
print(tabela.schema())
print(f"\nEspecificação de particionamento:")
print(tabela.spec())
```

---

### Passo 4 — Inserção de Dados (Snapshot 1)

```python
# Célula 3 — Carregar dados do Bronze e inserir na tabela Iceberg

import boto3
import io
import pyarrow.parquet as pq

# Ler os dados do MinIO (camada Bronze)
s3_client = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",  // ou http://host.docker.internal:9000
    aws_access_key_id="minioadmin",
    aws_secret_access_key="minioadmin123",
    region_name="us-east-1",
)

print("Lendo dados da camada Bronze...")
response = s3_client.list_objects_v2(
    Bucket="bronze", Prefix="ecommerce_sintetico/"
)
arquivos = [
    obj["Key"] for obj in response.get("Contents", [])
    if obj["Key"].endswith(".parquet")
]

# Ler o primeiro arquivo Parquet (amostra de 50.000 registros para a demo)
obj = s3_client.get_object(Bucket="bronze", Key=arquivos[0])
df_bronze = pd.read_parquet(io.BytesIO(obj["Body"].read()))

# Selecionar apenas os primeiros 50.000 registros para a demonstração
df_amostra = df_bronze.head(50_000).copy()

# Ajustar tipos para compatibilidade com o schema Iceberg
df_amostra["id_pedido"] = df_amostra["id_pedido"].astype("int64")
df_amostra["id_cliente"] = df_amostra["id_cliente"].astype("int64")
df_amostra["id_produto"] = df_amostra["id_produto"].astype("int64")
df_amostra["avaliacao_cliente"] = pd.to_numeric(
    df_amostra["avaliacao_cliente"], errors="coerce"
).astype("Int32")

# Converter para PyArrow Table (formato nativo do Iceberg)
tabela_arrow = pa.Table.from_pandas(
    df_amostra[[
        "id_pedido", "id_cliente", "id_produto", "categoria",
        "valor_unitario", "quantidade", "valor_total", "status_pedido",
        "regiao", "data_pedido", "avaliacao_cliente", "_fonte", "_ingerido_em"
    ]],
    schema=tabela.schema().as_arrow(),
    preserve_index=False,
)

# Inserir os dados na tabela Iceberg (cria o Snapshot 1)
print(f"Inserindo {len(df_amostra):,} registros na tabela Iceberg...")
import time
inicio = time.time()

tabela.append(tabela_arrow)

duracao = time.time() - inicio
print(f"✅ Snapshot 1 criado em {duracao:.2f}s")
print(f"   Registros inseridos: {len(df_amostra):,}")
```

---

### Passo 5 — Demonstração de Time Travel

```python
# Célula 4 — Inspecionar o histórico de snapshots

print("=== Histórico de Snapshots da Tabela Iceberg ===\n")

for snapshot in tabela.history():
    print(f"  Snapshot ID:    {snapshot.snapshot_id}")
    print(f"  Timestamp:      {datetime.fromtimestamp(snapshot.timestamp_ms / 1000, tz=timezone.utc)}")
    print(f"  Operação:       {snapshot.summary.get('operation', 'N/A')}")
    print(f"  Arquivos adicionados: {snapshot.summary.get('added-data-files', '0')}")
    print(f"  Registros adicionados: {snapshot.summary.get('added-records', '0')}")
    print()
```

```python
# Célula 5 — Inserir mais dados para criar o Snapshot 2

# Simular uma segunda carga de dados (próximo lote)
df_lote2 = df_bronze.iloc[50_000:100_000].copy()
df_lote2["id_pedido"] = df_lote2["id_pedido"].astype("int64")
df_lote2["id_cliente"] = df_lote2["id_cliente"].astype("int64")
df_lote2["id_produto"] = df_lote2["id_produto"].astype("int64")
df_lote2["avaliacao_cliente"] = pd.to_numeric(
    df_lote2["avaliacao_cliente"], errors="coerce"
).astype("Int32")

tabela_arrow_lote2 = pa.Table.from_pandas(
    df_lote2[[
        "id_pedido", "id_cliente", "id_produto", "categoria",
        "valor_unitario", "quantidade", "valor_total", "status_pedido",
        "regiao", "data_pedido", "avaliacao_cliente", "_fonte", "_ingerido_em"
    ]],
    schema=tabela.schema().as_arrow(),
    preserve_index=False,
)

tabela.append(tabela_arrow_lote2)
print(f"✅ Snapshot 2 criado: +{len(df_lote2):,} registros inseridos")

# Recarregar a tabela para ver o histórico atualizado
tabela = catalog.load_table(NOME_TABELA)
historico = list(tabela.history())
print(f"\nTotal de snapshots: {len(historico)}")
for snap in historico:
    ts = datetime.fromtimestamp(snap.timestamp_ms / 1000, tz=timezone.utc)
    print(f"  Snapshot {snap.snapshot_id}: {ts.strftime('%H:%M:%S')} — {snap.summary.get('added-records', '0')} registros adicionados")
```

```python
# Célula 6 — Time Travel: consultar o estado da tabela em um snapshot anterior

# Obter o ID do primeiro snapshot
snapshot_inicial = historico[-1]  # O mais antigo é o último na lista
snapshot_id_v1 = snapshot_inicial.snapshot_id

print(f"=== Time Travel — Consultando Snapshot {snapshot_id_v1} ===\n")

# Ler a tabela no estado do snapshot inicial (apenas os primeiros 50.000 registros)
scan_v1 = tabela.scan(snapshot_id=snapshot_id_v1)
df_v1 = scan_v1.to_pandas()

# Ler a tabela no estado atual (todos os 100.000 registros)
scan_atual = tabela.scan()
df_atual = scan_atual.to_pandas()

print(f"  Snapshot inicial (v1): {len(df_v1):,} registros")
print(f"  Estado atual:          {len(df_atual):,} registros")
print(f"  Diferença:             +{len(df_atual) - len(df_v1):,} registros adicionados")
print()
print("💡 O Time Travel permite auditar o estado dos dados em qualquer")
print("   ponto do passado — essencial para debugging de pipelines e")
print("   reprodutibilidade de experimentos de Machine Learning.")
```

---

### Passo 6 — Evolução de Schema

```python
# Célula 7 — Evolução de Schema: adicionar uma nova coluna sem reescrever os dados

from pyiceberg.schema import Schema
from pyiceberg.types import NestedField, BooleanType

print("=== Evolução de Schema ===\n")
print(f"Schema ANTES da evolução:")
print(tabela.schema())

# Adicionar uma nova coluna à tabela Iceberg
# Em Parquet puro, isso exigiria reescrever TODOS os arquivos
# No Iceberg, é uma operação de metadados — instantânea!
with tabela.update_schema() as update:
    update.add_column(
        path="pedido_internacional",
        field_type=BooleanType(),
        doc="Indica se o pedido foi realizado por cliente de outro país",
    )

# Recarregar a tabela para ver o schema atualizado
tabela = catalog.load_table(NOME_TABELA)

print(f"\nSchema APÓS a evolução:")
print(tabela.schema())
print()
print("✅ Nova coluna 'pedido_internacional' adicionada!")
print("   Os arquivos Parquet existentes NÃO foram reescritos.")
print("   O Iceberg retorna NULL para a nova coluna nos registros antigos.")
```

---

### Passo 7 — Consulta com DuckDB sobre a Tabela Iceberg

```python
# Célula 8 — Consultar a tabela Iceberg com DuckDB
# O DuckDB tem suporte nativo ao Iceberg via extensão

import duckdb

con_duck = duckdb.connect()
con_duck.execute("INSTALL iceberg; LOAD iceberg;")
con_duck.execute("INSTALL httpfs; LOAD httpfs;")
con_duck.execute("""
    SET s3_endpoint = 'localhost:9000';
    SET s3_access_key_id = 'minioadmin';
    SET s3_secret_access_key = 'minioadmin123';
    SET s3_use_ssl = false;
    SET s3_url_style = 'path';
""")

# Obter o caminho do metadata.json da tabela Iceberg
# O PyIceberg armazena os metadados no bucket silver
metadata_location = tabela.metadata_location
print(f"Localização dos metadados Iceberg: {metadata_location}\n")

# Consultar a tabela Iceberg via DuckDB
resultado = con_duck.execute(f"""
    SELECT
        categoria,
        regiao,
        COUNT(*)                        AS total_pedidos,
        ROUND(SUM(valor_total), 2)      AS receita_total,
        ROUND(AVG(avaliacao_cliente), 2) AS satisfacao_media
    FROM iceberg_scan('{metadata_location}')
    WHERE status_pedido = 'concluido'
    GROUP BY categoria, regiao
    ORDER BY receita_total DESC
    LIMIT 10
""").df()

print("Consulta DuckDB sobre tabela Iceberg:")
print(resultado.to_string(index=False))
```

---

### Passo 8 — Verificação dos Arquivos de Metadados no MinIO

```python
# Célula 9 — Inspecionar a estrutura de arquivos do Iceberg no MinIO

import boto3

s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="minioadmin",
    aws_secret_access_key="minioadmin123",
    region_name="us-east-1",
)

print("=== Estrutura de Arquivos do Iceberg no MinIO (bucket: silver) ===\n")

response = s3.list_objects_v2(Bucket="silver", Prefix="bronze_processado/")
objetos = response.get("Contents", [])

# Agrupar por tipo de arquivo
metadados = [o for o in objetos if "/metadata/" in o["Key"]]
dados = [o for o in objetos if "/data/" in o["Key"]]

print(f"📁 Arquivos de METADADOS ({len(metadados)} arquivos):")
for obj in metadados:
    tipo = "snapshot" if "snap-" in obj["Key"] else \
           "schema" if "schema" in obj["Key"] else \
           "manifest" if "manifest" in obj["Key"] else "metadata"
    print(f"   [{tipo:10s}] {obj['Key'].split('/')[-1]}  ({obj['Size'] / 1024:.1f} KB)")

print(f"\n📁 Arquivos de DADOS ({len(dados)} arquivos Parquet):")
for obj in dados:
    print(f"   [parquet   ] {obj['Key'].split('/')[-1]}  ({obj['Size'] / 1024:.1f} KB)")

print(f"""
💡 Estrutura do Iceberg:
   metadata/  → Histórico de snapshots, schemas e manifests (metadados)
   data/      → Arquivos Parquet com os dados reais

   O Iceberg NUNCA modifica arquivos de dados existentes.
   Cada operação de escrita cria NOVOS arquivos e um NOVO snapshot,
   garantindo leituras consistentes mesmo durante escritas concorrentes.
""")
```

---

### Verificação Final da Atividade 3

Ao concluir esta atividade, o aluno deve ser capaz de:

1. Explicar a diferença entre um Data Lake (Parquet puro) e um Data Lakehouse (Iceberg/Delta Lake) em termos de funcionalidades e casos de uso
2. Configurar um catálogo Iceberg local com PyIceberg e criar tabelas com schema fortemente tipado e particionamento declarativo
3. Demonstrar o *time travel* consultando a tabela no estado de um snapshot anterior e explicar sua importância para auditoria e reprodutibilidade de experimentos de ML
4. Realizar evolução de schema (adição de coluna) sem reescrever os arquivos de dados existentes
5. Consultar tabelas Iceberg com DuckDB e inspecionar a estrutura de metadados no MinIO

---

## Consolidação da Aula 3

As três atividades desta aula completaram o ciclo de processamento sobre a camada Bronze, introduzindo os dois motores analíticos que serão utilizados ao longo do curso (Spark e DuckDB) e o formato de tabela que eleva o Data Lake ao nível de Data Lakehouse (Apache Iceberg). A tabela abaixo resume quando utilizar cada ferramenta:

| Cenário | Ferramenta Recomendada |
|---|---|
| Dataset > 100 GB, cluster disponível | Apache Spark |
| Dataset < 50 GB, análise exploratória | DuckDB |
| Necessidade de ACID, time travel, evolução de schema | Apache Iceberg |
| Pipeline de produção com atualizações frequentes | Iceberg + Spark ou Iceberg + DuckDB |
| Prototipagem rápida, ambiente local | DuckDB + PyIceberg |

Na **Aula 4**, os dados processados serão formalizados em transformações documentadas e testadas utilizando o **dbt (Data Build Tool)**, construindo a camada Silver com modelos `staging` e `intermediate` que seguem as melhores práticas de engenharia de software aplicadas a dados.

---

