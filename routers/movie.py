from fastapi import APIRouter
from fastapi import FastAPI, Body, Path, Query, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Optional, List
from starlette.requests import Request
from utils.jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.error_handler import ErrorHandler
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieServices

movie_router = APIRouter()


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(max_length=15, min_length=3, default='la peli')
    overview: str #se le puede añadir condiciones para el dato de entrada
    year = int
    
    #OJO!, se tuvo que eliminar las condiciones ge y le ya que generaban error 
    #debido a que no estaban bien definidas
        
    rating = float #ge abreviacion de mayor o igual le menor o igual
    category = str
    #esta clase da nombre por defecto a la pelicula
    class Config: 
        schema_extra = {
            "example": {
                "id": 1,
                "title": 'mi peli',
                "overview": "descripcion de la peli",
                "year": 2022,
                "rating": 9,
                "category": 'comedy'
            }
        }



@movie_router.get('/movies', tags=['movies'], dependencies=[Depends(JWTBearer)])
def get_movies():
    db = Session() #activar la base de datos
    result = MovieServices(db).get_movies() #db.query(MovieModel).all() #consulta y donde queremos consultar
    return JSONResponse(content=jsonable_encoder(result))

@movie_router.get('/movies/{id}', tags=['movies'])
def get_movie(id: int = Path(default=1, ge=1, le=2000)):
    db = Session()
    result = MovieServices(db).get_movie(id) #db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result: 
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    """for item in movies:
        if item["id"] == id:
            return JSONResponse(content=item)"""
    return JSONResponse(content=jsonable_encoder(result))

@movie_router.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)): #parametros query
    #Un query parameter es un conjunto de parámetros opcionales los cuales 
    # son añadidos al finalizar la ruta, con el objetivo de definir contenido 
    # o acciones en la url, estos elementos se añaden después de un ?, 
    # para agregar más query parameters utilizamos &.
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    #data = [item for item in movies if item ['catergory'] == category]
    return JSONResponse(content=jsonable_encoder(result)) 

@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(status_code=201, content={"message": "Se ha registrado la película"})
'''
@movie_router.post('/movies', tags=['movies'], response_model=dict)
def create_movie(movie : Movie) -> dict:
    db = Session() #creamos sesion para conectarnos a base de datos
    #new_movie = MovieModel(id=movie.id, title=movie.title, overview=movie.overview, year=movie.year, rating=movie.rating, category=movie.category)
    new_movie = MovieModel(**movie.dict())#convertimos a diccionario para no tener que poner dato x dato
    #el escrito **movie.dict() se encarga de añadir todo
    db.add(new_movie)
    db.commit() #actualizacion para que los datos se guarden
    #movies.append(movie) ----- se elimina ya que se hizo en las dos lineas anteriores
    return JSONResponse(content={"message": "Se ha registrado la peli"})
    
'''

@movie_router.put('/movies/{id}', tags=['movies'], status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': "no se encontro la peli man"})
    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.category = movie.category
    db.commit
    return JSONResponse(content={"message": "Se ha modificado la peli"})

""" for item in movies:
        if item["id"] == id:
            item ["title"] = movie.title
            item ["overview"] = movie.overview
            item ["year"] = movie.year
            item ["rating"] = movie.rating
            item ["category"] = movie.category 
            
            return JSONResponse(content={"message": "Se ha eliminado la peli"})
    """

@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict)
def delete_movie(id: int) -> dict:
    db =  Session()
    result = MovieModel = db.query(MovieModel).filter(MovieModel.id == id).first()#db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': "no se encontro la peli man"})
    MovieServices(db).delete_movie(id) #db.delete(result)
    db.commit()
    return JSONResponse(content={"message": "Se ha eliminao la peli"})