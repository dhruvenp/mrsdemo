from fastapi import FastAPI, Request
import pickle
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import JSONResponse

app = FastAPI()

# Load data and similarity matrix
df = pickle.load(open('df.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Mount the static files directory
#app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/static", StaticFiles(directory="static"), name="static")
# Initialize Jinja2Templates for rendering HTML templates
templates = Jinja2Templates(directory="static")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    songs = df['song'].tolist()  # Assuming 'song' is the column containing song names
    return templates.TemplateResponse("index.html", {"request": request, "songs": songs})


@app.post("/recommend/")
async def recommend_music(request: Request):
    data = await request.json()
    song_name = data.get('song_name')

    def recommendation(song):
        # Check if df is not empty
        if not df.empty:
            # Filter DataFrame to rows where 'song' column matches the input
            filtered_df = df[df['song'] == song]
            if not filtered_df.empty:
                # Retrieve the index of the first matching row
                idx = filtered_df.index[0]
                # Compute recommendations based on the index
                distances = sorted(list(enumerate(similarity[idx])), reverse=True, key=lambda x: x[1])
                songs = [df.iloc[i[0]]['song'] for i in distances[1:6]]
                return songs
            else:
                return [f"No songs found matching '{song}'."]
        else:
            return ["DataFrame is empty."]

    recommendations = recommendation(song_name)
    return JSONResponse(content=recommendations)


@app.put("/")
async def put():
    return {"message": "hello from the put"}




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
