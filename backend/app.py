from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from database.models import setup_db, Product, User, Announcement
from auth.auth import requires_auth, AuthError
from cloudinary import config, api
import os

# This is going to config the cloudinary server for upload an image
config(
    cloud_name=os.environ.get('CLOUD_NAME'),
    api_key=os.environ.get('API_KEY'),
    api_secret=os.environ.get('API_SECRET')
)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    # this method is gonna get all the products and announcements that inside database and return it as json
    # does not require an authentication

    @app.route("/products", methods=['GET'])
    def get_products():
        all_products = Product.query.all()
        products = [prod.format_data_short() for prod in all_products]
        if len(products) == 0:
            abort(404)

        all_announcement = Announcement.query.all()
        announcements = [ad.format() for ad in all_announcement]

        return jsonify({
            'success': True,
            'products': products,
            'announcements': announcements
        })

    # this method is gonna get a specific product and return that specific product as json
    # this method require an authentication

    @app.route('/products/<int:product_id>', methods=['GET'])
    @requires_auth("get:specific-product")
    def get_specific_product(payload, product_id):
        get_specific_prod = Product.query.get(product_id)
        if get_specific_prod is None:
            abort(404)
        return jsonify({
            'success': True,
            'product': get_specific_prod.format_data_long()
        })

    # this method is gonna get all products of the user that login and return these products as json
    # of course need require an authentication

    @app.route('/products/my-products', methods=['GET'])
    @requires_auth("get:my-product")
    def get_my_products(payload):
        owner = request.args.get('name')
        if owner is None:
            abort(400)
        get_all_my_products = Product.query.filter_by(owner=owner).all()
        get_all_my_products_formatted = [prod.format_data_long() for prod in get_all_my_products]
        if len(get_all_my_products_formatted) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'products': get_all_my_products_formatted
        })

    # this method is gonna create a product and return all products as json
    # this method require an authentication

    @app.route("/products", methods=['POST'])
    @requires_auth("post:product")
    def add_product(payload):
        data = request.get_json()
        username = request.args.get('name')
        if username is None:
            abort(400)

        check_user = User.query.filter_by(name=username).one_or_none()
        if check_user is None:
            new_user = User(name=username)
            User.insert(new_user)
            user_name = new_user
        else:
            user_name = check_user
        if_duplicate = Product.query.filter_by(title=data['title']).all()
        if len(if_duplicate) > 0:
            abort(422)
        new_product = Product(title=data['title'], price=data['price'] + "$",
                              description=data['description'],
                              imageUrl=data['imageUrl'],
                              public_id_image=data['imageId'],
                              imageName=data['imageName'],
                              owner=username,
                              mobile=data['mobile'],
                              user=user_name)
        Product.insert(new_product)
        get_all_products = Product.query.all()
        products = [prod.format_data_long() for prod in get_all_products]
        if len(products) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'products': products
        })

    # this method is gonna updated a specific product and return all products as json
    # this method require an authentication

    @app.route('/products/<int:product_id>', methods=['PATCH'])
    @requires_auth("patch:product")
    def update_product(payload, product_id):
        get_product = Product.query.filter_by(id=product_id).first()
        if not get_product:
            abort(404)
        data = request.get_json()
        if data['imageUrl'] != "":
            to_delete_old_image = get_product.public_id_image
            api.delete_resources(to_delete_old_image)

        get_product.title = data['title'] if data['title'] else get_product.title
        get_product.price = data['price'] if data['price'] else get_product.price
        get_product.description = data['description'] if data['description'] else get_product.description
        get_product.imageUrl = data['imageUrl'] if data['imageUrl'] else get_product.imageUrl
        get_product.public_id_image = data['imageId'] if data['imageId'] else get_product.public_id_image
        get_products.imageName = data['imageName'] if data['imageName'] else get_product.imageName
        get_product.mobile = data['mobile'] if data['mobile'] else get_product.mobile
        get_product.update()
        get_all_products = Product.query.all()
        products = [prod.format_data_long() for prod in get_all_products]
        return jsonify({
            'success': True,
            'updated': product_id,
            'products': products
        })

    # this method is gonna delete a specific product and return a product_id
    # this method require an authentication

    @app.route('/products/<int:product_id>', methods=['DELETE'])
    @requires_auth("delete:product")
    def delete_product(payload, product_id):
        del_product = Product.query.get(product_id)

        if not del_product:
            abort(404)

        get_public_id = del_product.format_data_long()['public_id']
        api.delete_resources(get_public_id)
        del_product.delete()

        return jsonify({
            'success': True,
            'deleted': product_id
        })

    # this method is gonna get a specific announcement and return it as json
    # this method require an authentication with admin

    @app.route('/announcement/<int:ad_id>', methods=['GET'])
    @requires_auth("get:specific-announcement")
    def get_specific_announcement(payload, ad_id):
        get_specific_announce = Announcement.query.get(ad_id)
        if get_specific_announce is None:
            abort(404)
        return jsonify({
            'success': True,
            'announcement': get_specific_announce.format()
        })

    # this method is gonna create an announcement and return it as json
    # this method require an authentication with admin

    @app.route('/announcement', methods=['POST'])
    @requires_auth("post:announcement")
    def add_announcement(payload):
        new_announcement = request.get_json()
        if new_announcement['announcement'] == "":
            abort(400)
        announcement = Announcement(announcement=new_announcement['announcement'])
        announcement.insert()

        return jsonify({
            'success': True,
            'announcement': announcement.format()
        })

    # this method is gonna update a specific an announcement and return it as json
    # this method require an authentication with admin

    @app.route('/announcement/<int:ad_id>', methods=['PATCH'])
    @requires_auth("patch:announcement")
    def update_announcement(payload, ad_id):
        get_new_announcement = request.get_json()
        old_announcement = Announcement.query.get(ad_id)
        if not old_announcement:
            abort(404)

        old_announcement.announcement = get_new_announcement['announcement'] if get_new_announcement[
            'announcement'] else old_announcement.announcement
        old_announcement.update()
        get_all_announcement = Announcement.query.all()
        announcements = [announcement.format() for announcement in get_all_announcement]
        return jsonify({
            'success': True,
            'updated': ad_id,
            'announcements': announcements
        })

    # this method is gonna delete a specific an announcement and return ad_id
    # this method require an authentication with admin

    @app.route('/announcement/<int:ad_id>', methods=['DELETE'])
    @requires_auth("delete:announcement")
    def delete_announcement(payload, ad_id):
        del_announcement = Announcement.query.get(ad_id)
        if del_announcement is None:
            abort(404)
        del_announcement.delete()

        return jsonify({
            'success': True,
            'deleted': ad_id
        })

    # this method is gonna handler bad request

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    # this method is gonna handler file not found

    @app.errorhandler(404)
    def file_not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'File Not Found'
        }), 404

    # this method is gonna handler unprocessable

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    # this method is gonna handler AuthError

    @app.errorhandler(AuthError)
    def auth_error(error):
        error_code = error.error
        error_status_code = error.status_code
        return jsonify({
            'success': False,
            'error': error_code['code'],
            'error_number': error_status_code,
            'message': error_code['description'],
        }), error_status_code

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=os.environ.get('DEBUG', False))
