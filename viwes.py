from app import app, db, Advertising, Creator
from flask import jsonify, request
from flask.views import MethodView


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

    def patch(self, advertising_id):
        data = request.json
        response = Advertising.query.filter_by(id=advertising_id).update(data)  # True or False expected
        db.session.commit()

        if response:
            return jsonify(data)
        else:
            return jsonify({
                'status': 'object not found'
            })

    def delete(self, advertising_id):
        advertising = Advertising.query.get(advertising_id)
        db.session.delete(advertising)
        db.session.commit()

        return jsonify({
            'status': 204
        })


class CreatorView(MethodView):

    def send_email(self):
        ...


app.add_url_rule('/advertising/<int:advertising_id>', view_func=AdvertisingView.as_view('advertising_get'), methods=['GET'])
app.add_url_rule('/advertising/<int:advertising_id>', view_func=AdvertisingView.as_view('advertising_delete'), methods=['DELETE'])
app.add_url_rule('/advertising/<int:advertising_id>', view_func=AdvertisingView.as_view('advertising_patch'), methods=['PATCH'])
app.add_url_rule('/advertising/', view_func=AdvertisingView.as_view('advertising_post'), methods=['POST'])

if __name__ == '__main__':
    app.run()
