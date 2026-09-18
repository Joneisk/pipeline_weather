import pandas as pd
from pathlib import Path
import json

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


path_name = Path(__file__).parent / 'data' / 'weather_data.json'




columns_name_to_drop = ['weather', 'weather_icon', 'sys.type']

columns_name_to_rename  = {

        "base": "base",
        "visibilty": "visibility",
        "dt": "datetime",
        "timezone": "timezone",
        "id": "city_id",
        "name": "city_name",
        "cod": "code",
        "coord.lon": "longitude",
        "coord.lat": "latitude",
        "main.temp": "temperature",
        "main.feels_like": "feels_like",
        "main.temp_min": "temp_min",
        "main.temp_max": "temp_max",
        "main.pressure": "pressure",
        "main.humidity": "humidity",
        "main.sea_level": "sea_level",
        "main.grnd_level": "ground_level",
        "wind.speed": "wind_speed",
        "wind.deg": "wind_direction",
        "wind.gust": "wind_gust",
        "clouds.all": "clouds",
        "sys.type": "sys_type",
        'sys.id': 'sys_id',
        "sys.country": "country",
        "sys.sunrise": "sunrise",
        "sys.sunset": "sunset",
}
columns_to_normalize_datetime = ['datetime','sunrise', 'sunset']


def create_dataframe(path_name:str) -> pd.DataFrame:
    path = path_name

    if not path.exists():
        logging.error(f"Arquivo {path} não encontrado.")
        raise FileNotFoundError(f"Arquivo {path} não encontrado.")


    with open(path, 'r') as f:
        data = json.load(f)

    df = pd.json_normalize(data)
    logging.info(f"DataFrame criado com sucesso a partir de {path}.")
    return df

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df_weather = pd.json_normalize(df['weather'].apply(lambda x: x[0]))

    df_weather = df_weather.rename(columns={
        'id': 'weather_id',
        'main': 'weather_main',
        'description': 'weather_description',
        'icon': 'weather_icon'
    })

    df = pd.concat([df,df_weather], axis=1)
    logging.info("Colunas normalizadas com sucesso.")

    return df

def drop_columns(df: pd.DataFrame, columns_name: list[str]) -> pd.DataFrame:

    df = df.drop(columns=columns_name)
    logging.info(f"Colunas {columns_name} removidas com sucesso.")
    return df

def rename_columns(df: pd.DataFrame, columns_name: dict[str, str]) -> pd.DataFrame:
    df = df.rename(columns=columns_name)
    logging.info("Colunas renomeadas com sucesso.")
    return df

def normalize_datetime_columns(df: pd.DataFrame, columns_name: list[str]) -> pd.DataFrame:
    for column in columns_name:
        df[column] = pd.to_datetime(df[column], unit='s', utc=True).dt.tzconvert('America/Sao_Paulo')
    logging.info(f"Colunas {columns_name} normalizadas para datetime com sucesso.")
    return df


def data_transformation():
    print("Iniciando transformação de dados...")
    df = create_dataframe(path_name)
    df = normalize_columns(df)
    df = drop_columns(df, columns_name_to_drop)
    df = rename_columns(df, columns_name_to_rename)
    df = normalize_datetime_columns(df, columns_to_normalize_datetime)
    logging.info("Transformação de dados concluída com sucesso.")

    return df