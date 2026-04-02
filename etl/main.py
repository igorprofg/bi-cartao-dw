from sqlalchemy import create_engine
import pandas as pd 
import os 

pasta_csv = "data/raw"

# Lista todos os arquivos 

arquivos = os.listdir(pasta_csv)

dataframes = []

for arquivo in arquivos:
    if arquivo.endswith(".csv"): 
        caminho = os.path.join(pasta_csv, arquivo)
        print ("Lendo:", arquivo)

        df = pd.read_csv(
            caminho,
            sep=";",
            encoding="utf8"
        )

        dataframes.append(df)

# junta todos os csv em um único dataframe 

df_final = pd.concat(dataframes, ignore_index=True)

df_final.columns = [
    "data_compra",
    "nome_titular",
    "final_cartao",
    "categoria",
    "descricao",
    "parcela",
    "valor_usd",
    "cotacao",
    "valor_brl"
]

print("Total de registros:", len(df_final))

print(df_final.head())  



df_final["data_compra"] = pd.to_datetime(
    df_final["data_compra"],
    format="%d/%m/%Y"
)

print(df_final.dtypes)




# DIMENSÕES DE DATA

df_final["ano"] = df_final["data_compra"].dt.year
df_final["mes"] = df_final["data_compra"].dt.month
df_final["dia"] = df_final["data_compra"].dt.day
df_final["trimestre"] = df_final["data_compra"].dt.quarter
df_final["dia_semana"] = df_final["data_compra"].dt.day_name()

print(df_final.head())



# Corrigindo valores numericos: 
# se tiver lixo → vira NaN com o coerce 

df_final["valor_brl"] = pd.to_numeric(df_final["valor_brl"], errors="coerce")
df_final["valor_usd"] = pd.to_numeric(df_final["valor_usd"], errors="coerce")
df_final["cotacao"] = pd.to_numeric(df_final["cotacao"], errors="coerce")



# Limpando categorias: 

df_final["categoria"] = df_final["categoria"].replace("-","Nao categorizado")

df_final["categoria"] = df_final["categoria"].fillna("Nao categorizado")



# Separando as parcelas: 

def separar_parcela(valor): 
    if pd.isna(valor): 
        return pd.Series([None, None])
    
    valor = str(valor).strip()

    if valor.lower() == "única" or valor.lower() == "única": 
        return pd.Series([1, 1])
    
    if "/" in valor: 
        partes = valor.split("/")
        return pd.Series([int(partes[0]), int(partes[1])])
    
    return pd.series([None, None])


df_final[["num_parcela", "total_parcelas"]] = df_final["parcela"].apply(separar_parcela)  

print(df_final[["parcela","num_parcela","total_parcelas"]].head(10))



# Criando as DIMENSÕES: 
# DIM DATA

df_dim_data = df_final[
    ["data_compra", "dia", "mes", "trimestre", "ano", "dia_semana"]
].drop_duplicates()

df_dim_data = df_dim_data.rename(columns={
    "data_compra" : "data"
})

print("DIM_DATA:")
print(df_dim_data.head())



# DIM TITULAR:

df_dim_titular = df_final[
    ["nome_titular", "final_cartao"]
].drop_duplicates()

print("DIM_TITULAR:")
print(df_dim_titular.head())


# DIM CATEGORIA: 

df_dim_categoria = df_final[
    ["categoria"]
].drop_duplicates()

df_dim_categoria = df_dim_categoria.rename(columns={
    "categoria": "nome_categoria"
})

print("DIM_CATEGORIA:")
print(df_dim_categoria.head())



# DIM ESTABELECIMENTO:

df_dim_estabelecimento = df_final[
    ["descricao"]
].drop_duplicates()

df_dim_estabelecimento = df_dim_estabelecimento.rename(columns={
    "descricao": "nome_estabelecimento" 
})

print("DIM_ESTABELECIMENTO:")
print(df_dim_estabelecimento.head())



# Criando os IDs nas dimensões: 

df_dim_data = df_dim_data.reset_index(drop=True)
df_dim_data["id_data"] = df_dim_data.index + 1

df_dim_titular = df_dim_titular.reset_index(drop=True)
df_dim_titular["id_titular"] = df_dim_titular.index + 1 

df_dim_categoria = df_dim_categoria.reset_index(drop=True)
df_dim_categoria["id_categoria"] = df_dim_categoria.index + 1

df_dim_estabelecimento = df_dim_estabelecimento.reset_index(drop=True)
df_dim_estabelecimento["id_estabelecimento"] = df_dim_estabelecimento.index + 1



# Fazer merge com DIM_DATA: 

df_fato = df_final.merge(
    df_dim_data[["id_data", "data"]],
    left_on="data_compra",
    right_on="data",
    how="left"
)

# Merge com DIM_TITULAR: 

df_fato = df_fato.merge(
    df_dim_titular,
    on = ["nome_titular", "final_cartao"],
    how = "left"
)

# Merge com DIM_CATEGORIA: 

df_fato = df_fato.merge(
    df_dim_categoria,
    left_on= "categoria",
    right_on="nome_categoria",
    how="left"  
)

# Merge com DIM_ESTABELECIMENTO:

df_fato = df_fato.merge(
    df_dim_estabelecimento,
    left_on = "descricao",
    right_on = "nome_estabelecimento",
    how="left"
)

# TABELA FATO: 

df_fato_transacao = df_fato[
    [
        "id_data",
        "id_titular",
        "id_categoria",
        "id_estabelecimento",
        "valor_brl",
        "valor_usd",
        "cotacao",
        "parcela",
        "num_parcela", 
        "total_parcelas"
    ]
]

print("FATO_TRANSACAO:")
print(df_fato_transacao.head())
print("Total registros fato:", len(df_fato_transacao))


# Ajustando nome das colunas: 

df_dim_data = df_dim_data[
    ["id_data","data","dia","mes","trimestre","ano","dia_semana"]
]

df_dim_titular = df_dim_titular[
    ["id_titular","nome_titular","final_cartao"]
]

df_dim_categoria = df_dim_categoria[
    ["id_categoria","nome_categoria"]
]

df_dim_estabelecimento = df_dim_estabelecimento[
    ["id_estabelecimento","nome_estabelecimento"]
]


# Eviando as dimensões para o PostgreSQL: 

df_dim_data.to_sql(
    "dim_data",
    engine,
    if_exists="append",
    index=False
)

df_dim_titular.to_sql(
    "dim_titular",
    engine,
    if_exists="append",
    index=False
)

df_dim_categoria.to_sql(
    "dim_categoria",
    engine,
    if_exists="append",
    index=False
)

df_dim_estabelecimento.to_sql(
    "dim_estabelecimento",
    engine,
    if_exists="append",
    index=False
)

# Enviando a tabela Fato: 

df_fato_transacao.to_sql(
    "fato_transacao",
    engine,
    if_exists="append",
    index=False
)


