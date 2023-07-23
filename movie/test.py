from random import randint
import requests, json

url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&primary_release_year=2014&sort_by=popularity.desc&with_genres=Horror"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhMmM1ODVmNjY4MjI1NzQwNjQ0Y2M2YzRlN2UxYTRlMiIsInN1YiI6IjY0YTA3YmE1ZDUxOTFmMDBmZjhiYTYwNCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.AQU63lkbX8brlddSJSib0ThxUYpLs6UL8EUKP7N3rFI"
}

response = requests.get(url, headers=headers)
jsonData = response.json()["results"]

randomIndex = randint(1, len(jsonData))
print(jsonData[randomIndex])


