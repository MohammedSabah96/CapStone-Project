import os
from itertools import product

from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json

from database.models import setup_db, Product, User
from auth.auth import requires_auth, AuthError


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    return app


APP = create_app()


@APP.route("/products", methods=['GET'])
def get_products():
    all_products = Product.query.all()
    products = [prod.format_data_short() for prod in all_products]
    if len(products) == 0:
        abort(404)
    return jsonify({
        'success': True,
        'products': products
    })


@APP.route('/products-detail', methods=['GET'])
@requires_auth("get:product-detail")
def get_specific_product(payload):
    available_products = Product.query.all()
    products = [prod.format_data_long() for prod in available_products]
    if len(products) == 0:
        abort(404)
    return jsonify({
        'success': True,
        'products': products
    })


@APP.route("/products", methods=['POST'])
@requires_auth("post:product")
def add_product(payload):
    data = request.get_json()
    username = request.args.get('name')
    if username is None:
        abort(400)
    check_user = User.query.filter_by(name=username).one_or_none()
    if check_user is None:
        newuser = User(name=username)
        User.insert(newuser)
        user_name = newuser
    else:
        user_name = check_user
    if_duplicate = Product.query.filter_by(title=data['title']).all()
    if len(if_duplicate) > 0:
        abort(422)
    newproduct = Product(title=data['title'], price=data['price'],
                         description=data['description'],
                         imageUrl=data['imageUrl'], user=user_name)
    Product.insert(newproduct)
    get_all_products = Product.query.all()
    products = [prod.format_data_long() for prod in get_all_products]
    if len(products) == 0:
        abort(404)
    return jsonify({
        'success': True,
        'products': products
    })


@APP.route('/products/<int:product_id>', methods=['PATCH'])
@requires_auth("patch:product")
def update_product(payload, product_id):
    get_product = Product.query.filter_by(id=product_id).first()
    if not get_product:
        abort(400)
    data = request.get_json()
    get_product.title = data['title'] if data['title'] else get_product.title
    get_product.price = data['price'] if data['price'] else get_product.price
    get_product.description = data['description'] if data['description'] else get_product.description
    get_product.imageUrl = data['imageUrl'] if data['imageUrl'] else get_product.imageUrl
    get_product.update()
    get_all_products = Product.query.all()
    products = [prod.format_data_long() for prod in get_all_products]
    return jsonify({
        'success': True,
        'updated': product_id,
        'products': products
    })


@APP.route('/products/<int:product_id>', methods=['DELETE'])
@requires_auth("delete:product")
def delete_product(payload, product_id):
    del_product = Product.query.get(product_id)
    if not del_product:
        abort(404)
    del_product.delete()

    return jsonify({
        'success': True,
        'Deleted': product_id
    })


@APP.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


@APP.errorhandler(404)
def file_not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'File Not Found'
    }), 404


@APP.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@APP.errorhandler(AuthError)
def auth_error(error):
    error_code = error.error
    error_status_code = error.status_code
    return jsonify({
        'success': False,
        'error': error_code['code'],
        'error_number': error_status_code,
        'message': error_code['description'],
    }), error_status_code


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
