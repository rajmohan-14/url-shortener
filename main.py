from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ids import generator
from database import get_db
from models import URL
from utils import encode_base62
from cache import redis_client, CACHE_TTL_SECONDS

app = FastAPI()

class URLRequest(BaseModel):
    original_url: str

@app.get("/")
def read_root():
    return {"message": "URL Shortener API is running"}

@app.post("/shorten")
def shorten_url(request: URLRequest, db: Session = Depends(get_db)):
    new_id = generator.next_id()
    new_url = URL(
        id=new_id,
        short_code=encode_base62(new_id),
        original_url=request.original_url,
    )
    db.add(new_url)
    db.commit()

    return {"short_code": new_url.short_code, "original_url": new_url.original_url}

@app.get("/{short_code}")
def redirect_to_url(short_code: str, db: Session = Depends(get_db)):
    cached_url = redis_client.get(short_code)
    if cached_url:
        return RedirectResponse(url=cached_url)

    url_entry = db.query(URL).filter(URL.short_code == short_code).first()
    if not url_entry:
        raise HTTPException(status_code=404, detail="Short URL not found")

    redis_client.set(short_code, url_entry.original_url, ex=CACHE_TTL_SECONDS)
    return RedirectResponse(url=url_entry.original_url)