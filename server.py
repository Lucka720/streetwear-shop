from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_root():
    # Читаем твой файл index.html и выплевываем в браузер
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>ГДЕ INDEX.HTML, СУКА?!</h1>"

@app.post("/order")
def create_order(item: str, price: int):
    print(f"!!! ПРИШЛО БАБЛО: {item} за {price}$ !!!")
    return {"status": "Success", "message": "Order received!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
