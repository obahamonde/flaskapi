from flaskapi.resources import *
from flask import Flask, render_template, jsonify, send_from_directory, send_file
from orjson import loads
from flaskapi.websocket import useSocketIO


class FlaskAPI(Flask):
    def __init__(self):
        super().__init__(__name__)
        for name, model in prisma_models:
            self.register_blueprint(Resource(model.schema, model, name))
            self.secret_key = 'secret'

        @self.route('/api')
        def docs():
            responses = []
            schemas_ = [loads(model.schema_json())
                        for name, model in prisma_models]
            for schema in schemas_:
                schema_name = schema['$ref'].replace('#/definitions/', '')
                schema_content = schema['definitions'][schema_name]

                responses.append({
                    'name': schema_name,
                    'schema': schema_content
                })
            return jsonify(responses)

        @self.route('/app')
        def app_page():
            return render_template('app.html')

        @self.route('/')
        def index():
            return render_template('index.html')

        @self.route('/assets/<path:path>')
        def send_assets(path):
            return send_from_directory('templates/assets', path)

        @self.route('/images/<path:path>')
        def send_images(path):
            return send_from_directory('templates/images', path)

        @self.route('/favicon.ico')
        def favicon():
            return send_file('templates/favicon.svg')

        @self.route('/favicon.svg')
        def favicon_svg():
            return send_file('templates/favicon.svg')

        self = useSocketIO(self)
