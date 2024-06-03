import bottle

app = bottle.Bottle()


@app.route("/")
def index():
    return "Hello, world!"


def run(
    host="localhost",
    port=8080,
    task_directory: str | Path = None,
    task_files: list[str] = None,
    config: str | Path = "config.json",
):
    # Load task models
    if task_directory:
        load_tasks(task_directory)
    if task_files:
        for task_file in task_files:
            load_task(task_file)
    # Load configuration
    load_config(config)
    # Run the server
    app.run(host=host, port=port)


if __name__ == "__main__":
    app.run()
