# 🌦️ Pipeline Weather

Pipeline ETL que extrai dados climáticos da **OpenWeather API**, normaliza e transforma com **Pandas** e prepara a carga no **PostgreSQL** (em desenvolvimento).

## Etapas
1. **Extract** (`src/extract_data.py`): consulta a API, valida a resposta e salva o JSON bruto
2. **Transform** (`src/transform_data.py`): normaliza o JSON, renomeia e remove colunas e converte tipos
3. **Load** *(em desenvolvimento)*: gravação no PostgreSQL via SQLAlchemy
4. **Análise** em `notebooks/analysis_data.ipynb`

## Stack
Python 3.12 · uv · Requests · Pandas · SQLAlchemy · PostgreSQL · logging

## Como rodar
```bash
uv sync
echo "API_KEY=sua_chave_openweather" > .env
uv run python src/extract_data.py
uv run python src/transform_data.py
```
