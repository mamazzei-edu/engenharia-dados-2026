## Versão do python 3.12 ##

O dbt exige a versão 3.12 do python para sua instalação.

Para atender esse requisito, é necessário instalar essa versão do python e recriar o ambiente virtual com essa versão.

## Se você já está com o ambiente configurado ##
Atualize o requirements.txt com as bibliotecas instaladas, sem a informação de versões para que você não tenha problemas de incompatibilidade com o python:

```sh
Set-ExecutionPolicy -Scope User -ExecutionPolicy RemoteSigned
pip list --format=freeze | cut -d= -f1 > requirements.txt
```

Remova o diretório .venv e recrie utilizando o python 3.12:

```sh
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r .\scripts\requirements.txt 
```

## Se você precisar reiniciar o ambiente ##

Se você estiver utilizando os equipamento da Mauá, será necessário executar o iniciar_maua.md

Após concluir a inicialização do ambiente, vamos dar continuidade ao processo:

```sh

pip install dbt-core dbt-duckdb
```


