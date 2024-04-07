from json import dump, load
from quart import Quart, render_template, request, Markup
from chessEngine import start_game
from settings_json_handler import build_settings

app = Quart(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True  # dev

def write_json_to_file(data, file_path, **args):
    with open(file_path, 'w') as f:
        dump(data, f, **args)

def read_json_from_file(file_path, **args):
    with open(file_path, 'r') as f:
        return load(f, **args)

@app.route('/')
async def run():
    my_config_html = Markup(build_settings())  # Mark HTML string as safe
    return await render_template("index.html",
                                 chess_board=start_game(),
                                 cell_size=56,
                                 my_config=my_config_html,
                                 color_1="#ffffff",
                                 color_2="#ff0000")

@app.route('/settings', methods=["GET", "POST"])
async def settings():
    if request.method == "POST":
        await post_settings_config()
    my_config_html = Markup(build_settings())  # Mark HTML string as safe
    return await render_template("settings.html",
                                 dfs=dfs,
                                 my_config=my_config_html)


@app.route("/reset_settings", methods=["POST", "GET"])
async def reset_settings():
    default_settings = await read_json_from_file("default_config.json")
    write_json_to_file(default_settings, "config.json")


@app.route('/get-settings', methods=["GET"])
async def get_settings():
    config = read_json_from_file("config.json")
    return config


@app.route("/update_settings", methods=["POST"])
async def post_settings_config():
    data = await request.form
    updated_config = await get_settings()
    for key, value in data.items():
        # Convert string representation of bool to actual bool
        if value.lower() == 'true':
            value = True
        elif value.lower() == 'false':
            value = False
        updated_config[key] = value

    # Write updated config to config.json
    write_json_to_file(updated_config, "config.json")


if __name__ == '__main__':
    app.run(debug=True)
