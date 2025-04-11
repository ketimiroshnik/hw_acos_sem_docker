from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from app.db import get_db, add_url, get_url_by_short_id
from app.utils import generate_short_id, get_redis, cache_url, get_cached_url

app = FastAPI()
db = get_db()
redis = get_redis()

@app.get("/", response_class=HTMLResponse)
def index():
    return '''
    <html>
        <head><title>Link Shortener</title></head>
        <body>
            <h1>Shorten a URL</h1>
            <form action="/shorten" method="post">
                <input type="text" name="url" placeholder="Enter URL here" size="50"/>
                <button type="submit">Shorten</button>
            </form>
        </body>
    </html>
    '''

@app.post("/shorten", response_class=HTMLResponse)
async def shorten_url_form(url: str = Form(...)):
    short_id = generate_short_id()
    add_url(db, short_id, url)
    return f'''
    <html>
        <body>
            <p>Shortened URL: <a href="/{short_id}">/{short_id}</a></p>
        </body>
    </html>
    '''

@app.post("/shorten_json")
async def shorten_url(request: Request):
    data = await request.json()
    original_url = data.get("url")
    if not original_url:
        raise HTTPException(status_code=400, detail="URL is required")

    short_id = generate_short_id()
    add_url(db, short_id, original_url)
    return {"short_id": short_id}

@app.get("/{short_id}")
async def redirect(short_id: str):
    cached = get_cached_url(redis, short_id)
    if cached:
        return RedirectResponse(cached)

    url = get_url_by_short_id(db, short_id)
    if url:
        cache_url(redis, short_id, url)
        return RedirectResponse(url)
    raise HTTPException(status_code=404, detail="URL not found")