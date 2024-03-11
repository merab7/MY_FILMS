import requests
import os

class Film_data():
    def __init__(self) -> None:
        self.headers = {
    "accept": "application/json",
    "Authorization": os.environ.get('TOP_FILM_HEADER_AUTHORIZATION')
}
        



    def find_film(self, title):
        url =  f"https://api.themoviedb.org/3/search/movie?query={title}&include_adult=true&language=en-US&page=1"
        response = requests.get(url, headers=self.headers)
        data = response.json()
        return data['results']
    
    def find_with_id(self, id ):
       url = f"https://api.themoviedb.org/3/movie/{id}?language=en-US"
       response = requests.get(url, headers=self.headers)
       data = response.json()
       return data

