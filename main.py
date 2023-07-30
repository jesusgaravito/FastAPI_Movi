from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from utils.jwt_manager import create_token
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router


app = FastAPI()
app.title = "mi app de prueba con fastapi" #esto cambia el título en la documentación
app.version = "0.1" #version de la app en la documentacion
app.add_middleware(ErrorHandler)
app.include_router(movie_router)
Base.metadata.create_all(bind=engine)
  
    
class User(BaseModel):
    email: str
    password: str
    
movies = [
     {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Accion'  }, 
        {
        'id': 2,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Accion'   
    } 
]

@app.get('/', tags=['home']) #tags le pone titulo a las rutas de la app
def message():
    #return "hellow"
    return HTMLResponse('<h1>Hello </h1>')

@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)

