# FastAPI

[FastAPI](https://fastapi.tiangolo.com/tutorial/first-steps/) theory and sandbox

## Clone

Clone the repo using Git:

```
git clone git@github.com:DLesmes/fast_api_hw.git
```

## Usage

* Set python venv with the [requirements.txt](https://github.com/DLesmes/fast_api_hw/blob/main/requirements.txt)

```
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```
* Run the server

```
uvicorn main:app --reload
```

### Recommended lectures

* [Documentation](https://hackmd.io/rK8aSVH3Qg-ICKuKGOO01w)
* [https://www.openapis.org/](https://www.openapis.org/)
* GitHub - Redocly/redoc: 📘 [OpenAPI/Swagger-generated API Reference Documentation](https://github.com/Redocly/redoc)
* [API Documentation & Design Tools for Teams | Swagger](https://swagger.io/)
* [Class repo](https://github.com/platzi/curso-fastapi-fundamentos-path-validaciones/blob/request_response_body/main.py)
* [Query params str validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/)
* [Field types - pydantic](https://docs.pydantic.dev/usage/types/#pydantic-types)
