from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import get_db
from models import URL
from utils import encode_base62

app = FastAPI()

class URLRequest(BaseModel):
    original_url: str

@app.get("/")
def read_root():
    return {"message": "URL Shortener API is running"}

@app.post("/shorten")
def shorten_url(request: URLRequest, db: Session = Depends(get_db)):
    new_url = URL(original_url=request.original_url, short_code="")
    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    new_url.short_code = encode_base62(new_url.id)
    db.commit()

    return {"short_code": new_url.short_code, "original_url": new_url.original_url}

@app.get("/{short_code}")
def redirect_to_url(short_code: str, db: Session = Depends(get_db)):
    url_entry = db.query(URL).filter(URL.short_code == short_code).first()

    if not url_entry:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return RedirectResponse(url=url_entry.original_url)