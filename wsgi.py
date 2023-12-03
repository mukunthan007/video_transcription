import warnings

from waitress import serve

from app import init_app

# warnings.filterwarnings("ignore")

if __name__ == "__main__":
    app = init_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
