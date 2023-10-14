docker run -d -v "./volume":/app/volume --name wikiloader dandiego235/wikiloader:12
docker run -d -p 3000:3000 --name wikiui dandiego235/wikiui:8
docker run -d -p 5000:5000 -p 8000:8000 --name wikiapi dandiego235/wikiapi:8