from apis.product import product_bp
from config.settings import get_config
from flasgger import Swagger
from flask import Flask


def create_app():
    """Flask application factory."""
    app = Flask(__name__)

    # Load configuration based on environment
    app.config.from_object(get_config())

    # Initialize Swagger (for API docs)
    Swagger(app, template_file="swagger/product_swagger.yml")

    # Register blueprints
    app.register_blueprint(product_bp, url_prefix="/grpc")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(
        host=app.config["FLASK_HOST"],
        port=app.config["FLASK_PORT"],
        debug=app.config["DEBUG"],
    )
