# Full Stack Products Shop Final Project (Capstone)
## Introductions
This project was made to practice how to implement a backend application, implementing endpoints for `GET,POST,PATCH,DELETE`
most of the endpoint need an authorization, and of course it has a test file in which is tested each endpoint in success and failure state.
## Overview
Welcome to Products Shop Project.

This project is capable of creating products and updated or delete your own products,each product should have a unique title and an image of the product,description of the product,price of the product and mobile number.

## Pre-requisites
Developers using this project should already have Docker installed on their local machines.

## Getting Started

The system is containerized by Docker and you need to run following command to start with:

```
   # build images
    docker-compose build

    # run images
    docker-compose up -d
```
Then, you can see both backend and frontend on following urls

- backend: http://localhost:8080/api/products
- frontend: http://localhost:8080/
###### In the production:
- backend: http://productsshop-env.eba-upn2jai5.eu-central-1.elasticbeanstalk.com/api/products
## Testing

For testing you need to go to [`./backend/database/models.py`](./backend/database/models.py). And read the comment carefully

##### If you want test with `test_app.py` you have to Follow the instructions Bellow:
1. go to [`./backend/.env`](./backend/.env) file and in `DATABASE_URL_TEST` make sure to add your name of your database and password(if you have one)
2. got to the [`./backend/database/models.py`](./backend/database/models.py) and there you will find comment with numbers (1),(2),(3)
3. in the models file uncomment (`1`) and comment (`2`) and make sure you uncomment (`3`)
4. open your command line and cd to `./backend`
5. run this command in your CMD  `python test_app.py`

##### If You want test with `postman collection` you have to Follow the instructions Bellow:

1. First make sure server is running by using this command:
    - docker-compose up
2. got to the [`./backend/database/models.py`](./backend/database/models.py) and there you will find comment with numbers (1),(2),(3).
3. in the models file comment (`1`) and uncomment (`2`) and make sure you uncomment (`3`).
> Node: import and runner you can find them above on left side of the application
4. open your `postman application` and import  this file [`./backend/capstone.postman_collection.json`](./backend/capstone.postman_collection.json)
5. make sure to add at least one product and one announcement for successfully testing.
6. After that run the file with postman.


## API Reference
The backend is hosted at http://localhost:8080/api/

### Error Handling

There are five types of errors the API will return`;

- 400 - bad request
- 404 - File Not Found
- 422 - unprocessable
- 401- unauthorized

### Endpoints
`Note: We are gonna use Postman if you want to use curl it's up to you`

If you want run your endpoint with production use this url `http://productsshop-env.eba-upn2jai5.eu-central-1.elasticbeanstalk.com/api/products` instead of `localhost:8080/api/products`

So before we are gonna start make sure you put the authentication token in postman
from Authorization choose type Bearer token  and add the token
you can get the authentication token from  http://localhost:8080/profile make sure you login first.

##### POST '/products'

- create new product
- sample: 
    - Add this url `localhost:8080/api/products?name=admin` in postman and make sure you select `POST`.
    - In the body choose raw and make sure type of data will be `JSON` And add this data below or you can add whatever you want
```
{
    "title": "Car",
    "description": "Beautiful car",
    "price": "1500",
    "imageUrl": "https://i.ytimg.com/vi/-Yb7SMMZdWc/maxresdefault.jpg",
    "imageId":"samples/maxresdefault",
    "imageName":"maxresdefault.jpg",
    "mobile": 77338843215
}
```    
_Response:_

```
{
  "products": [
    {
      "created": "Fri, 10 Jul 2020 14:40:55 GMT",
      "description": "Beautiful car",
      "id": 2,
      "imageName": "maxresdefault.jpg",
      "imageUrl": "https://i.ytimg.com/vi/-Yb7SMMZdWc/maxresdefault.jpg",
      "mobile": 77338843215,
      "owner": "admin",
      "price": "1500$",
      "public_id": "samples/maxresdefault",
      "title": "Car",
      "user_id": 1
    }
  ],
  "success": true
}
```

##### GET '/products'
- get all products and announcements(if found)
- sample: 
    - Add this url `localhost:8080/api/products` in postman and make sure you select `GET`.
    
_Response:_

```
{
  "announcements": [],
  "products": [
    {
      "created": "Fri, 10 Jul 2020 14:40:55 GMT",
      "id": 2,
      "imageUrl": "https://i.ytimg.com/vi/-Yb7SMMZdWc/maxresdefault.jpg",
      "owner": "admin",
      "price": "1500$",
      "title": "Car",
      "user_id": 1
    }
  ],
  "success": true
}
```
##### GET '/products/<int:product_id>'
- get a specific product
- sample:
    - Add this url `localhost:8080/api/products/2` in postman and make sure you select `GET`.

_Response:_

```
{
  "product": {
    "created": "Fri, 10 Jul 2020 14:40:55 GMT",
    "description": "Beautiful car",
    "id": 2,
    "imageName": "maxresdefault.jpg",
    "imageUrl": "https://i.ytimg.com/vi/-Yb7SMMZdWc/maxresdefault.jpg",
    "mobile": 77338843215,
    "owner": "admin",
    "price": "1500$",
    "public_id": "samples/maxresdefault",
    "title": "Car",
    "user_id": 1
  },
  "success": true
}
```

##### GET '/products/my-products'
- get all products that user was made
- sample:
    - Add this url `localhost:8080/api/products/my-products?name=admin` in postman and make sure you select `GET`.

_Response:_
```
{
  "products": [
    {
      "created": "Fri, 10 Jul 2020 14:40:55 GMT",
      "description": "Beautiful car",
      "id": 2,
      "imageName": "maxresdefault.jpg",
      "imageUrl": "https://i.ytimg.com/vi/-Yb7SMMZdWc/maxresdefault.jpg",
      "mobile": 77338843215,
      "owner": "admin",
      "price": "1500$",
      "public_id": "samples/maxresdefault",
      "title": "Car",
      "user_id": 1
    }
  ],
  "success": true
}
```
##### PATCH '/products/<int:product_id>'
- update a specific product
- sample:
    - Add this url `localhost:8080/api/products/2` in postman and make sure you select `PATCH`.
    - In the body choose raw and make sure type of data will be `JSON` And add this data below
    
```
{
    "title": "Cool Car",
    "description": "",
    "price": "2500",
    "imageUrl": "",
    "imageId":"",
    "imageName":"",
    "mobile": 77338843215
}
```

_Response:_

```
{
  "products": [
    {
      "created": "Fri, 10 Jul 2020 15:16:51 GMT",
      "description": "Beautiful car",
      "id": 2,
      "imageName": "maxresdefault.jpg",
      "imageUrl": "https://i.ytimg.com/vi/-Yb7SMMZdWc/maxresdefault.jpg",
      "mobile": 77338843215,
      "owner": "admin",
      "price": "2500",
      "public_id": "samples/maxresdefault",
      "title": "Cool Car",
      "user_id": 1
    }
  ],
  "success": true,
  "updated": 2
}
```
##### DELETE '/products/<int:product_id>'
- delete a specific product
-sample:
    - Add this url `localhost:8080/api/products/2` in postman and make sure you select `DELETE`.

_Response:_

```
{
  "deleted": 2,
  "success": true
}
```
##### POST '/announcement'
- create an announcement this only works with admin user
- sample:
    - Add this url `localhost:8080/api/announcement` in postman and make sure you select `POST`.
    - In the body choose raw and make sure type of data will be `JSON` And add this data below
    
```
{
    "announcement": "Discount 40% for two days"
}
```
_Response:_

```
{
  "announcement": {
    "announcement": "Discount 40% for two days",
    "id": 1
  },
  "success": true
}
```

##### GET '/announcement/<int:ad_id>'
- get a specific announcement
- sample:
    - Add this url `localhost:8080/api/announcement/1` and make sure you select `GET`.

_Response:_

```
{
  "announcement": {
    "announcement": "Discount 40% for two days",
    "id": 1
  },
  "success": true
}
```

##### PATCH '/announcement/<int:ad_id>'
- update a specific announcement
- sample:
    - Add this url `localhost:8080/api/announcement/1` and make sure you select `PATCH`.
    - In the body choose raw and make sure type of data will be `JSON` And add this data below

```
{
    "announcement": "Discount 80% for three days"
}
```
_Response:_

```
{
  "announcements": [
    {
      "announcement": "Discount 80% for three days",
      "id": 1
    }
  ],
  "success": true,
  "updated": 1
}
```

##### DELETE '/announcement/<int:ad_id>'
- delete a specific announcement
- sample:
    - Add this url `localhost:8080/api/announcement/1` in postman and make sure you select `DELETE`.

_Response:_

```
{
  "deleted": 1,
  "success": true
}
```
## Permissions

Permissions|Details
---|---
get:specific-product|get specific product from DB
get:my-product|get user's products from DB
get:specific-announcement|get specific announcement from DB
post:product|create new product
post:announcement|create announcement for all users
patch:product|update the product from DB
patch:announcement|update announcement from DB
delete:product|delete product from DB
delete:announcement|delete announcement from DB


## Roles

Role|Permissions
---|---
admin| `get:specific-product`, `get:my-product`, `post:product`, `patch:product`, `delete:product`, `get:specific-announcement`, `post:announcement`, `patch:announcement`, `delete:announcement`
user| `get:specific-product`, `get:my-product`, `post:product`, `patch:product`, `delete:product`