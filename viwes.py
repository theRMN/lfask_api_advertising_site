from app import app, Advertising
from flask import jsonify, request
from flask.views import MethodView
from app import db


class AdvertisingView(MethodView):

    def get(self, advertising_id):
        advertising = Advertising.query.get(advertising_id)

        if not advertising:
            response = jsonify({
                'error': 'advertisings not found'
            })
            response.status_code = 404
            return response

        return jsonify({
            'id': advertising.id,
            'title': advertising.title,
            'description': advertising.description,
            'create_at': advertising.create_at,
            'creator_id': advertising.creator_id
        })

    def post(self):
        data = request.json
        advertising = Advertising(**data)
        db.session.add(advertising)
        db.session.commit()

        return jsonify({
            'id': advertising.id
        })

    def delete(self, advertising_id):
        advertising = Advertising.query.get(advertising_id)
        db.session.delete(advertising)
        db.session.commit()

        return jsonify({
            'status': 200
        })


app.add_url_rule('/advertising/<int:advertising_id>', view_func=AdvertisingView.as_view('advertising_get'), methods=['GET'])
app.add_url_rule('/advertising/<int:advertising_id>', view_func=AdvertisingView.as_view('advertising_delete'), methods=['DELETE'])
app.add_url_rule('/advertising/', view_func=AdvertisingView.as_view('advertising_post'), methods=['POST'])

if __name__ == '__main__':
    app.run()
