# Convenção de Nomenclatura — Camada Bronze
 
## Estrutura de Caminhos
 
bronze/
└── {sistema_origem}/
    └── {entidade}/
        └── ano={YYYY}/
            └── mes={MM}/
                └── dia={DD}/
                    └── {entidade}_{timestamp_unix}.parquet
 
## Exemplos
 
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
 
## Regras
 
1. Nomes em snake_case, letras minúsculas, sem espaços ou caracteres especiais.
2. O timestamp no nome do arquivo é Unix timestamp (segundos desde epoch).
3. Particionamento obrigatório por ano/mês/dia da DATA DE INGESTÃO (não da data do dado).
4. Cada arquivo deve conter os metadados: _fonte, _ingerido_em, _versao_schema.
5. Nunca sobrescrever arquivos existentes na camada Bronze — apenas acrescentar.
