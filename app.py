"""Start Artify in a browser."""

import threading
import webbrowser

from src.web import create_app


def main() -> None:
    app = create_app()
    url = "http://127.0.0.1:5050"
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    print(f"Artify is running at {url}. Press Ctrl+C to stop it.")
    app.run(host="127.0.0.1", port=5050, debug=False)


if __name__ == "__main__":
    main()
