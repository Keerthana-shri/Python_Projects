# 
FROM python:3.10.6

# 
WORKDIR /pokemon_code_1

# 
COPY ./requirements.txt /pokemon_code_1/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /pokemon_code_1/requirements.txt

COPY .env /pokemon_code_1
# 
COPY ./src /pokemon_code_1/src

# 
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]