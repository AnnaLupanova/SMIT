from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def get_home():
    return {'detail': 'some_string'}