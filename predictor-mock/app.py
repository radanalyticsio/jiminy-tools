"""a mock predictor service for the jiminy project"""
import flask
import flask_restful as flaskr
import jsonschema as js


app = flask.Flask(__name__)
api = flaskr.Api(app)

datastore = {}

class ServerInfo(flaskr.Resource):
    def get(self):
        return {
            'application': {
                'name': 'jiminy-mock-predictor',
                'version': '0.0.0'
                }
            }


prediction_request_schema = {
    "type": "object",
    "properties": {
        "user": {"type": "string"},
        "products": {
            "type": "array",
            "minItems": 1,
            "items": {"type": "string"}
            }
        },
    "required": ["user", "products"]
    }


class Predictions(flaskr.Resource):
    def post(self):
        data = flask.request.json
        try:
            js.validate(data, prediction_request_schema)
            resp = {
                    "id": str(len(datastore) + 1),
                    "user" : data["user"],
                    "products": [p for p in data["products"]]
                }
            datastore[resp["id"]] = {
                    "id": resp["id"],
                    "user" : resp["user"],
                    "products": [
                        {"id": p, "rating": 5.0} for p in data["products"]]
                }
            return resp, 201
        except js.ValidationError as ex:
            return {
                    "errors": [
                        {
                            "status": 400,
                            "title": "invalid request format",
                            "details": ex.message
                            }
                        ]
                    }, 400


class PredictionResponse(flaskr.Resource):
    def get(self, p_id):
        if str(p_id) not in datastore:
            return {
                    "errors": [
                        {
                            "status": 404,
                            "title": "not found",
                            "details": "the requested prediction id {} "
                            "cannot be found".format(p_id)
                            }
                        ]
                }, 404
        return datastore[p_id]



if __name__ == '__main__':
    api.add_resource(ServerInfo, '/')
    api.add_resource(Predictions, '/predictions')
    api.add_resource(PredictionResponse, '/predictions/<p_id>')
    app.run(debug=True)
