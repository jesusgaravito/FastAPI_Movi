from models.movie import Movie as MovieModel
class MovieServices():
    def __init__(self, db) -> None:
        self.db = db
        
    def get_movies(self):
        result = self.db.query(MovieModel).all()
        return result
    
    def get_movie(self, id):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return result
        
    def delete_movie(self, id: int):
        self.db.query(MovieModel).filter(MovieModel.id == id).delete()
        self.db.commit()
        return
    