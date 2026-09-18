from urllib import response
import requests

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

import json
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("API_KEY")

url = f'https://api.openweathermap.org/data/2.5/weather?q=Curitiba,BR&units=metric&appid={api_key}'


def extract_data(url:str) -> list:
    try:
        response = requests.get(url)
        data = response.json()  #dicionario

        if response.status_code != 200:
            logging.error(f"Erro na requisição de {url}. Status code: {response.status_code}")
            raise ValueError(f"Erro na requisição de {url}. Status code: {response.status_code}")
        if not data:
            logging.warning(f"Nenhum dado retornado de {url}.")
            raise ValueError(f"Nenhum dado retornado de {url}.")
        
        output_path = 'data/weather_data.json'
        output_dir = Path(output_path).parent     #reconhece nivel acima
        output_dir.mkdir(parents=True, exist_ok=True)  #Cria Pasta

        with open(output_path, 'w') as f:
            json.dump(data, f, indent=4)

        logging.info(f"Dados extraídos e salvos em {output_path}")
        return data
    
    except Exception as e:
        logging.error(f"Erro ao extrair dados de {url}: {e}")
        raise ValueError(f"Erro ao extrair dados de {url}: {e}") 

extract_data(url)