import os
import unittest
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from database.models import setup_db, User, Product, Announcement
from dotenv import load_dotenv

load_dotenv()
ADMIN_TOKEN = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkxDMDl5czMzdGs4d1FuaGNiM0dyQyJ9.eyJpc3MiOiJodHRwczovL2NvZmZlLXNoby5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVmMDM2N2NhN2MzYzUwMDE5ZDBiYzg5IiwiYXVkIjpbInByb2R1Y3QiLCJodHRwczovL2NvZmZlLXNoby5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTk0MjAxNDE2LCJleHAiOjE1OTQyODc4MTYsImF6cCI6IlZxVTc3R0UxQzFxbmllQk1DdnpKM254ZXhBOUw0UExEIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphbm5vdW5jZW1lbnQiLCJkZWxldGU6cHJvZHVjdCIsImdldDpteS1wcm9kdWN0IiwiZ2V0OnNwZWNpZmljLWFubm91bmNlbWVudCIsImdldDpzcGVjaWZpYy1wcm9kdWN0IiwicGF0Y2g6YW5ub3VuY2VtZW50IiwicGF0Y2g6cHJvZHVjdCIsInBvc3Q6YW5ub3VuY2VtZW50IiwicG9zdDpwcm9kdWN0Il19.iVUwjbHAinKXuiV4X8fGDS_K01rP4epMAA1nMo1oqn6ZJUK9E2MVURk6YG6r2A-2Ve8ha3egaf6SfwuKmme1e0Mtwwch2q3ptMY13kitpAaS60bT2lmFmy_FmbSAAimVcOLBgDPA9ng6JCJ2_szEITWLPR09Y4innwzoHieLjKy8d_4y3aJ3RHu5aHMIpxMMsuRFcrQ3ObgKWzIlMUbPIMd_8MRfCgynKgmpm_A6CQxZ8uIdf8mFwIXJ64ewvNjAWOw_XroRnNKYMvVdKsxSeZux2RWBrQ0iks-By8hcFsmM3AbZwOluolocKipesqz2SWv87SMocCBIvbjUfly4vw"


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
                                         public_id_image="3njkdng832332", owner="admin", mobile=7754322264,
                                         user=self.new_user)
            self.new_product_1.insert()
            self.new_product_2 = Product(title="Car 2", description="Cool Car 2", price="2000$",
                                         imageUrl="https://i.ytimg.com/vi/-Yb7SMMZdWc/maxresdefault.jpg",
                                         public_id_image="3njkdng8sad32332", owner="admin", mobile=77554222264,
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

    def test_get_products(self):
        res = self.client().get('/products')
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['products'])
        self.assertTrue(data['announcements'])

    def test_get_specific_products(self):
        res = self.client().get('/products/1', headers={
            'Authorization': ADMIN_TOKEN
        })
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['product'])

    def test_get_401_specific_products_authorization_header_missing(self):
        res = self.client().get('/products/1')
        data = res.get_json()
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 'authorization_header_missing')
        self.assertEqual(data['error_number'], 401)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_get_404_specific_products(self):
        res = self.client().get('/products/1000', headers={
            'Authorization': ADMIN_TOKEN
        })
        data = res.get_json()
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'File Not Found')

    def test_get_my_products(self):
        res = self.client().get('/products/my-products?name=admin', headers={
            'Authorization': ADMIN_TOKEN
        })
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['products'])

    def test_get_400_bad_request_my_products(self):
        res = self.client().get('/products/my-products', headers={
            'Authorization': ADMIN_TOKEN
        })
        data = res.get_json()
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')
        self.assertEqual(data['error'], 400)

    def test_get_404_file_not_found_my_products(self):
        res = self.client().get('/products/my-products?name=evo', headers={
            'Authorization': ADMIN_TOKEN
        })
        data = res.get_json()
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'File Not Found')
        self.assertEqual(data['error'], 404)

    def test_get_401_authorization_header_missing_my_products(self):
        res = self.client().get('/products/my-products?name=admin')
        data = res.get_json()
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 'authorization_header_missing')
        self.assertEqual(data['error_number'], 401)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_post_product(self):
        new_product = {
            'title': 'New Car',
            'description': 'Cool Car',
            'price': '2000',
            'imageUrl': 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fstatic.pexels.com%2Fphotos%2F210019%2Fpexels-photo-210019.jpeg&f=1&nofb=1',
            'mobile': 7763342935,
        }
        res = self.client().post('/products?name=admin', headers={
            'Authorization': ADMIN_TOKEN
        }, json=new_product)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['products'])

    def test_post_400_bad_request_product(self):
        new_product = {
            'title': 'New Car',
            'description': 'Cool Car',
            'price': '2000',
            'imageUrl': 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fstatic.pexels.com%2Fphotos%2F210019%2Fpexels-photo-210019.jpeg&f=1&nofb=1',
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

    def test_post_product_401_authorization_header_missing(self):
        new_product = {
            'title': 'New Car',
            'description': 'Cool Car',
            'price': '2000',
            'imageUrl': 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fstatic.pexels.com%2Fphotos%2F210019%2Fpexels-photo-210019.jpeg&f=1&nofb=1',
            'mobile': 7763342935,
        }
        res = self.client().post('/products?name=admin', json=new_product)
        data = res.get_json()
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 'authorization_header_missing')
        self.assertEqual(data['error_number'], 401)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_patch_product(self):
        update_product = {
            'title': 'Cool Car',
            'description': 'The Beauty Car :D',
            'price': '7000',
            'imageUrl': 'https://i.ytimg.com/vi/-Yb7SMMZdWc/maxresdefault.jpg',
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

    def test_patch_404_file_not_found_product(self):
        update_product = {
            'title': 'Test Car',
            'description': '',
            'price': '',
            'imageUrl': '',
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

    def test_patch_401_authorization_header_missing_product(self):
        update_product = {
            'title': 'Test',
            'description': '',
            'price': '',
            'imageUrl': '',
            'mobile': 7763342935,
        }
        res = self.client().patch('/products/1000', json=update_product)
        data = res.get_json()
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 'authorization_header_missing')
        self.assertEqual(data['error_number'], 401)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_delete_product(self):
        res = self.client().delete('/products/2', headers={
            'Authorization': ADMIN_TOKEN
        })
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 2)

    def test_delete_404_file_not_found_product(self):
        res = self.client().delete('/products/1000', headers={
            'Authorization': ADMIN_TOKEN
        })
        data = res.get_json()
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'File Not Found')
        self.assertEqual(data['error'], 404)

    def test_delete_401_authorization_header_missing_product(self):
        res = self.client().delete('/products/1000')
        data = res.get_json()
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 'authorization_header_missing')
        self.assertEqual(data['error_number'], 401)
        self.assertEqual(data['message'], 'Authorization header is expected.')

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

    def test_get_specific_announcement(self):
        res = self.client().get('/announcement/1', headers={
            'Authorization': ADMIN_TOKEN
        })
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['announcement'])

    def test_get_404_file_not_found_announcement(self):
        res = self.client().get('/announcement/1000', headers={
            'Authorization': ADMIN_TOKEN
        })
        data = res.get_json()
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'File Not Found')
        self.assertEqual(data['error'], 404)

    def test_get_401_authorization_header_missing_announcement(self):
        res = self.client().get('/announcement/1')
        data = res.get_json()
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 'authorization_header_missing')
        self.assertEqual(data['error_number'], 401)
        self.assertEqual(data['message'], 'Authorization header is expected.')

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

    def test_delete_announcement(self):
        res = self.client().delete('/announcement/2', headers={
            'Authorization': ADMIN_TOKEN
        })
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 2)

    def test_delete_404_file_not_found_announcement(self):
        res = self.client().delete('/announcement/1000', headers={
            'Authorization': ADMIN_TOKEN
        })
        data = res.get_json()
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'File Not Found')
        self.assertEqual(data['error'], 404)

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
