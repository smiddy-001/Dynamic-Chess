# Chess 'i Guess

### made with:
- ❌flask  https://flask.palletsprojects.com
- ✅quart (flask with async events) https://github.com/pallets/quart
- ❌tailwind  https://tailwindui.com/
- ❌material-ui (tailwind)  https://www.material-tailwind.com
- ✅spectre.css https://picturepan2.github.io/spectre/
- ❌tox (ci testing) https://tox.wiki/en/4.14.2/

### Design
minimal and sleek

run with `. venv/bin/activate && python app.py`

## Theming

![img_1.png](img_1.png)

colors, Picks the black, a random colourful one and uses plain white
`#111420, #ee1e0b, #eee52f, #17cc26, #2b68d9, #9828b6`

`{"Rich black":"111420","Off Red":"ee1e0b","Aureolin":"eee52f","Lime green":"17cc26","Celtic Blue":"2b68d9","Dark violet":"9828b6"}`

## Testing

The best way to test Quart is with Tox,

```bash
$ pip install tox
$ tox
```

A minimal Quart example is,

```python
from quart import Quart, render_template, websocket

app = Quart(__name__)

@app.route("/")
async def hello():
    return await render_template("index.html")

@app.route("/api")
async def json():
    return {"hello": "world"}

@app.websocket("/ws")
async def ws():
    while True:
        await websocket.send("hello")
        await websocket.send_json({"hello": "world"})

if __name__ == "__main__":
    app.run()
```

