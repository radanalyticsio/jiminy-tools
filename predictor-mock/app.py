"""a mock predictor service for the jiminy project"""
import flask
import flask_restful as flaskr
import jsonschema as js


app = flask.Flask(__name__)
api = flaskr.Api(app)

ratings_store = {}
rankings_store = {}

class ServerInfo(flaskr.Resource):
    def get(self):
        return {
            'application': {
                'name': 'jiminy-mock-predictor',
                'version': '0.0.0'
                }
            }


rating_request_schema = {
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


rank_request_schema = {
    "type": "object",
    "properties": {
        "user": {"type": "string"},
        "topk": {"type": "integer"},
        },
    "required": ["user", "topk"]
    }


class RankingsPredictions(flaskr.Resource):
    def post(self):
        data = flask.request.json
        try:
            js.validate(data, rank_request_schema)
            resp = {
                    "id": str(len(rankings_store) + 1),
                    "user": data["user"],
                    "topk": data["topk"],
                    "products": []
                }
            rankings_store[resp["id"]] = {
                    "id": resp["id"],
                    "user": resp["user"],
                    "products": [ {"id": i+1, "rating": 5.0}
                                for i in range(resp["topk"])]
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


class RankingsPredictionResponse(flaskr.Resource):
    def get(self, p_id):
        if str(p_id) not in rankings_store:
            return {
                    "errors": [
                        {
                            "status": 404,
                            "title": "not found",
                            "details": "the requested ranking id {} "
                            "cannot be found".format(p_id)
                            }
                        ]
                }, 404
        return rankings_store[p_id]


class RatingsPredictions(flaskr.Resource):
    def post(self):
        data = flask.request.json
        try:
            js.validate(data, rating_request_schema)
            resp = {
                    "id": str(len(ratings_store) + 1),
                    "user" : data["user"],
                    "products": [p for p in data["products"]]
                }
            ratings_store[resp["id"]] = {
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


class RatingsPredictionResponse(flaskr.Resource):
    def get(self, p_id):
        if str(p_id) not in ratings_store:
            return {
                    "errors": [
                        {
                            "status": 404,
                            "title": "not found",
                            "details": "the requested ratings id {} "
                            "cannot be found".format(p_id)
                            }
                        ]
                }, 404
        return ratings_store[p_id]



if __name__ == '__main__':
    api.add_resource(ServerInfo, '/')
    api.add_resource(RatingsPredictions, '/predictions/ratings')
    api.add_resource(RatingsPredictionResponse, '/predictions/ratings/<p_id>')
    api.add_resource(RankingsPredictions, '/predictions/ranks')
    api.add_resource(RankingsPredictionResponse, '/predictions/ranks/<p_id>')
    app.run(debug=True)
