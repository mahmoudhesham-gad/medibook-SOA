from flask import Flask, jsonify

from config import Config
from errors import register_error_handlers
from routes import bp

app = Flask(__name__)

app.config.from_object(Config)

app.register_blueprint(bp)
register_error_handlers(app)

@app.get("/health")
def health():
    return jsonify({"service": Config.SERVICE_NAME, "status": "UP"})


if __name__ == "__main__":
    app.run(port=Config.PORT, debug=True)
