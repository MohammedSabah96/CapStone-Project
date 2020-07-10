import os
import unittest
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from database.models import setup_db, User, Product, Announcement
from dotenv import load_dotenv

# this is going to let us using the variables that defined in .env file
load_dotenv()
# this variable has an admin token so all the test pass
ADMIN_TOKEN = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkxDMDl5czMzdGs4d1FuaGNiM0dyQyJ9.eyJpc3MiOiJodHRwczovL2NvZmZlLXNoby5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVmMDM2N2NhN2MzYzUwMDE5ZDBiYzg5IiwiYXVkIjpbInByb2R1Y3QiLCJodHRwczovL2NvZmZlLXNoby5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTk0MzY5NDM1LCJleHAiOjE1OTQ0NTU4MzUsImF6cCI6IlZxVTc3R0UxQzFxbmllQk1DdnpKM254ZXhBOUw0UExEIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphbm5vdW5jZW1lbnQiLCJkZWxldGU6cHJvZHVjdCIsImdldDpteS1wcm9kdWN0IiwiZ2V0OnNwZWNpZmljLWFubm91bmNlbWVudCIsImdldDpzcGVjaWZpYy1wcm9kdWN0IiwicGF0Y2g6YW5ub3VuY2VtZW50IiwicGF0Y2g6cHJvZHVjdCIsInBvc3Q6YW5ub3VuY2VtZW50IiwicG9zdDpwcm9kdWN0Il19.hFuqRhdzxNOuJhjxjKiz8VnAOtYTk3nKFGMJYcmoOOrPyirsJRgdP3yxk6fS4a-6tjzcTs7ZYOysEsehpSIHazxo6cMJk-HmRfOmlOK1C0sbBNI66ICvpo7xc6-paxptAmsnlRYS8C8U0Tv_a4_WwFDkyvmqJZdG8yMbHS7vUmiahRucg3sesni66J2iMFCA-A-yjBXovwVS4K7ZbD4niRJ2lhrbO8q9Yhji6qhFPePACb8LtE_37b43tlui31OZybV5bXjVofryiDLdtE14lCBPSl6ZoxyZMjnVH98VmQRhi6lrnm6-sBR5StdrWWLkg9NgLSucaanoXRkNOC_KTg"


class CapstoneTestCase(unittest.TestCase):
    """This class represents the Capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.getenv('DATABASE_URL_TEST')
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

            self.new_announcement_1 = Announcement(announcement="Discount 1%")
            self.new_announcement_1.insert()
            self.new_announcement_2 = Announcement(announcement="Discount 2%")
            self.new_announcement_2.insert()
            self.new_user = User(name="admin")
            self.new_user.insert()
            self.new_product_1 = Product(title="Car 1", description="Cool Car 1", price="1500$",
                                         imageUrl="https://i.ytimg.com/vi/-Yb7SMMZdWc/maxresdefault.jpg",
                                         public_id_image="3njkdng832332", imageName="maxresdefault.jpg", owner="admin",
                                         mobile=7754322264,
                                         user=self.new_user)
            self.new_product_1.insert()
            self.new_product_2 = Product(title="Car 2", description="Cool Car 2", price="2000$",
                                         imageUrl="https://i.ytimg.com/vi/-Yb7SMMZdWc/maxresdefault.jpg",
                                         public_id_image="3njkdng8sad32332", imageName="maxresdefault.jpg",
                                         owner="admin", mobile=77554222264,
                                         user=self.new_user)
            self.new_product_2.insert()

    def tearDown(self):
        """Executed after each test"""
        announcements = Announcement.query.all()
        for ad in announcements:
            ad.delete()

        products = Product.query.all()
        for product in products:
            product.delete()

        users = User.query.all()
        for user in users:
            user.delete()

        pass

    # this method is gonna test for getting all products and announcements and  response with 200

    def test_get_products(self):
        res = self.client().get('/products')
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['products'])
        self.assertTrue(data['announcements'])

    # this method is gonna test for getting a specific product and  response with 200

    def test_get_specific_products(self):
        res = self.client().get('/products/1', headers={
            'Authorization': ADMIN_TOKEN
        })
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['product'])

    # this method is gonna test for getting a specific product without authorization header and response with 401

    def test_get_401_specific_products_authorization_header_missing(self):
        res = self.client().get('/products/1')
        data = res.get_json()
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 'authorization_header_missing')
        self.assertEqual(data['error_number'], 401)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    # this method is gonna test for getting a specific product that does not exists  and  response with 404

    def test_get_404_specific_products(self):
        res = self.client().get('/products/1000', headers={
            'Authorization': ADMIN_TOKEN
        })
        data = res.get_json()
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'File Not Found')

    # this method is gonna test for getting specific products that the user have and response with 200

    def test_get_my_products(self):
        res = self.client().get('/products/my-products?name=admin', headers={
            'Authorization': ADMIN_TOKEN
        })
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['products'])

    # this method is gonna test for getting specific products without give that specific user and response with 400

    def test_get_400_bad_request_my_products(self):
        res = self.client().get('/products/my-products', headers={
            'Authorization': ADMIN_TOKEN
        })
        data = res.get_json()
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')
        self.assertEqual(data['error'], 400)

    # this method is gonna test for getting a specific products that the user have but does not exists
    # and response with 404

    def test_get_404_file_not_found_my_products(self):
        res = self.client().get('/products/my-products?name=evo', headers={
            'Authorization': ADMIN_TOKEN
        })
        data = res.get_json()
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'File Not Found')
        self.assertEqual(data['error'], 404)

    # this method is gonna test for getting specific products that the user have but without authorization header
    # and response with 401

    def test_get_401_authorization_header_missing_my_products(self):
        res = self.client().get('/products/my-products?name=admin')
        data = res.get_json()
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 'authorization_header_missing')
        self.assertEqual(data['error_number'], 401)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    # this method is gonna test for create a product and response with 200

    def test_post_product(self):
        new_product = {
            'title': 'New Car',
            'description': 'Cool Car',
            'price': '2000',
            'imageUrl': 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fstatic.pexels.com%2Fphotos%2F210019%2Fpexels-photo-210019.jpeg&f=1&nofb=1',
            "imageId": "samples/maxresdefault",
            "imageName": "maxresdefault.jpg",
            'mobile': 7763342935,
        }
        res = self.client().post('/products?name=admin', headers={
            'Authorization': ADMIN_TOKEN
        }, json=new_product)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['products'])

    # this method is gonna test for create a product without specify a username in url and response with 400

    def test_post_400_bad_request_product(self):
        new_product = {
            'title': 'New Car',
            'description': 'Cool Car',
            'price': '2000',
            'imageUrl': 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fstatic.pexels.com%2Fphotos%2F210019%2Fpexels-photo-210019.jpeg&f=1&nofb=1',
            "imageId": "samples/maxresdefault",
            "imageName": "maxresdefault.jpg",
            'mobile': 7763342935,
        }
        res = self.client().post('/products', headers={
            'Authorization': ADMIN_TOKEN
        }, json=new_product)
        data = res.get_json()
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')
        self.assertEqual(data['error'], 400)

    # this method is gonna test for create a product without specify authorization header and response with 401

    def test_post_product_401_authorization_header_missing(self):
        new_product = {
            'title': 'New Car',
            'description': 'Cool Car',
            'price': '2000',
            'imageUrl': 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fstatic.pexels.com%2Fphotos%2F210019%2Fpexels-photo-210019.jpeg&f=1&nofb=1',
            "imageId": "samples/maxresdefault",
            "imageName": "maxresdefault.jpg",
            'mobile': 7763342935,
        }
        res = self.client().post('/products?name=admin', json=new_product)
        data = res.get_json()
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 'authorization_header_missing')
        self.assertEqual(data['error_number'], 401)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    # this method is gonna test for update a specific product and response with 200

    def test_patch_product(self):
        update_product = {
            'title': 'Cool Car',
            'description': 'The Beauty Car :D',
            'price': '7000',
            'imageUrl': 'https://i.ytimg.com/vi/-Yb7SMMZdWc/maxresdefault.jpg',
            "imageId": "samples/maxresdefault",
            "imageName": "maxresdefault.jpg",
            'mobile': 7763342935,
        }
        res = self.client().patch('/products/1', headers={
            'Authorization': ADMIN_TOKEN
        }, json=update_product)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated'], 1)
        self.assertTrue(data['products'])

    # this method is gonna test for update a specific product that does not exists and response with 404

    def test_patch_404_file_not_found_product(self):
        update_product = {
            'title': 'Test Car',
            'description': '',
            'price': '',
            'imageUrl': '',
            "imageId": "",
            "imageName": "",
            'mobile': 7763342935,
        }
        res = self.client().patch('/products/1000', headers={
            'Authorization': ADMIN_TOKEN
        }, json=update_product)
        data = res.get_json()
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'File Not Found')
        self.assertEqual(data['error'], 404)

    # this method is gonna test for update a specific product without an authorization header and response with 401

    def test_patch_401_authorization_header_missing_product(self):
        update_product = {
            'title': 'Test',
            'description': '',
            'price': '',
            'imageUrl': '',
            "imageId": "",
            "imageName": "",
            'mobile': 7763342935,
        }
        res = self.client().patch('/products/1000', json=update_product)
        data = res.get_json()
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 'authorization_header_missing')
        self.assertEqual(data['error_number'], 401)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    # this method is gonna test for delete a specific product and response with 200

    def test_delete_product(self):
        res = self.client().delete('/products/2', headers={
            'Authorization': ADMIN_TOKEN
        })
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 2)

    # this method is gonna test for delete a specific product that does not exists and response with 404

    def test_delete_404_file_not_found_product(self):
        res = self.client().delete('/products/1000', headers={
            'Authorization': ADMIN_TOKEN
        })
        data = res.get_json()
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'File Not Found')
        self.assertEqual(data['error'], 404)

    # this method is gonna test for delete a specific product without an authorization header and response with 401

    def test_delete_401_authorization_header_missing_product(self):
        res = self.client().delete('/products/1000')
        data = res.get_json()
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 'authorization_header_missing')
        self.assertEqual(data['error_number'], 401)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    # this method is gonna test for create an announcement (this works only with admin) and response with 200

    def test_post_announcement(self):
        new_announcement = {
            'announcement': "There is a Discount 50% for 5 days"
        }
        res = self.client().post('/announcement', headers={
            'Authorization': ADMIN_TOKEN
        }, json=new_announcement)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['announcement'])

    # this method is gonna test for create an announcement (this works only with admin)
    # without give an announcement to add to database and response with 400

    def test_post_400_bad_request_announcement(self):
        new_announcement = {
            'announcement': ""
        }
        res = self.client().post('/announcement', headers={
            'Authorization': ADMIN_TOKEN
        }, json=new_announcement)
        data = res.get_json()
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')
        self.assertEqual(data['error'], 400)

    # this method is gonna test for create an announcement (this works only with admin)
    # without an authorization header and response with 401

    def test_post_401_authorization_header_missing_announcement(self):
        new_announcement = {
            'announcement': "There is a Discount 50% for 5 days"
        }
        res = self.client().post('/announcement', json=new_announcement)
        data = res.get_json()
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 'authorization_header_missing')
        self.assertEqual(data['error_number'], 401)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    # this method is gonna test for get a specific announcement (this works only with admin) and response with 200

    def test_get_specific_announcement(self):
        res = self.client().get('/announcement/1', headers={
            'Authorization': ADMIN_TOKEN
        })
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['announcement'])

    # this method is gonna test for get a specific announcement (this works only with admin)
    # that does not exists and response with 404

    def test_get_404_file_not_found_announcement(self):
        res = self.client().get('/announcement/1000', headers={
            'Authorization': ADMIN_TOKEN
        })
        data = res.get_json()
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'File Not Found')
        self.assertEqual(data['error'], 404)

    # this method is gonna test for get a specific announcement (this works only with admin)
    # that does not have an authorization header and response with 401

    def test_get_401_authorization_header_missing_announcement(self):
        res = self.client().get('/announcement/1')
        data = res.get_json()
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 'authorization_header_missing')
        self.assertEqual(data['error_number'], 401)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    # this method is gonna test for update a specific announcement (this works only with admin)
    # and response with 200

    def test_patch_announcement(self):
        new_announcement = {
            'announcement': "There is a Discount 80% for 12 days"
        }
        res = self.client().patch('/announcement/1', headers={
            'Authorization': ADMIN_TOKEN
        }, json=new_announcement)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated'], 1)

    # this method is gonna test for update a specific announcement (this works only with admin)
    # that does not have an authorization header and response with 401

    def test_patch_401_authorization_header_missing_announcement(self):
        new_announcement = {
            'announcement': "There is a Discount 80% for 12 days"
        }
        res = self.client().patch('/announcement/1', json=new_announcement)
        data = res.get_json()
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 'authorization_header_missing')
        self.assertEqual(data['error_number'], 401)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    # this method is gonna test for update a specific announcement (this works only with admin)
    # that does not exists and response with 404

    def test_patch_404_file_not_found_announcement(self):
        new_announcement = {
            'announcement': "There is a Discount 80% for 12 days"
        }
        res = self.client().patch('/announcement/1000', headers={
            'Authorization': ADMIN_TOKEN
        }, json=new_announcement)
        data = res.get_json()
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'File Not Found')
        self.assertEqual(data['error'], 404)

    # this method is gonna test for delete a specific announcement (this works only with admin)
    # and response with 200

    def test_delete_announcement(self):
        res = self.client().delete('/announcement/2', headers={
            'Authorization': ADMIN_TOKEN
        })
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 2)

    # this method is gonna test for delete a specific announcement (this works only with admin)
    # that does not exists and response with 404

    def test_delete_404_file_not_found_announcement(self):
        res = self.client().delete('/announcement/1000', headers={
            'Authorization': ADMIN_TOKEN
        })
        data = res.get_json()
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'File Not Found')
        self.assertEqual(data['error'], 404)

    # this method is gonna test for delete a specific announcement (this works only with admin)
    # that does not have an authorization header and response with 401

    def test_delete_401_authorization_header_missing_announcement(self):
        res = self.client().delete('/announcement/2')
        data = res.get_json()
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 'authorization_header_missing')
        self.assertEqual(data['error_number'], 401)
        self.assertEqual(data['message'], 'Authorization header is expected.')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
