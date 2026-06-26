/*
  stg_pedidos.sql
  ───────────────
  Modelo staging para a tabela de pedidos do e-commerce.

  Responsabilidades deste modelo:
    ✅ Renomear colunas para o padrão snake_case do projeto
    ✅ Converter tipos de dados (string → timestamp, string → integer)
    ✅ Padronizar strings (uppercase/lowercase)
    ✅ Remover colunas de metadados de ingestão (prefixo _)
    ✅ Aplicar filtros de qualidade básicos (remover registros completamente nulos)

  NÃO faz:
    ❌ Joins com outras tabelas
    ❌ Agregações ou cálculos de negócio
    ❌ Deduplicação
    ❌ Regras de negócio específicas
*/

with

-- Referência à fonte Bronze via macro source()
-- O dbt rastreia automaticamente a linhagem: stg_pedidos → bronze_ecommerce.pedidos
fonte_bronze as (

    select * from {{ source('bronze_ecommerce', 'pedidos') }}

),

-- Renomeação e conversão de tipos
renomeado as (

    select
        -- Identificadores (mantidos como inteiros)
        cast(id_pedido  as bigint)  as pedido_id,
        cast(id_cliente as bigint)  as cliente_id,
        cast(id_produto as bigint)  as produto_id,

        -- Atributos descritivos (padronizados para lowercase)
        lower(trim(categoria))      as categoria,
        lower(trim(status_pedido))  as status_pedido,
        lower(trim(regiao))         as regiao,

        -- Valores monetários (garantir precisão decimal)
        cast(valor_unitario as decimal(12, 2)) as valor_unitario,
        cast(valor_total    as decimal(12, 2)) as valor_total,
        cast(quantidade     as integer)        as quantidade,

        -- Timestamps (padronizar para UTC)
        cast(data_pedido as timestamp) as pedido_criado_em,

        -- Avaliação do cliente (pode ser nula — pedidos sem avaliação)
        cast(avaliacao_cliente as integer) as avaliacao_cliente,

        -- Metadados de rastreabilidade (preservados para auditoria)
        _fonte          as fonte_origem,
        _ingerido_em    as ingerido_em

    from fonte_bronze

),

-- Filtro de qualidade: remover registros sem identificadores essenciais
-- (não é deduplicação — apenas remoção de linhas completamente inválidas)
filtrado as (

    select *
    from renomeado
    where
        pedido_id  is not null
        and cliente_id is not null
        and valor_total > 0  -- Pedidos com valor zero são considerados inválidos

)

select * from filtrado
