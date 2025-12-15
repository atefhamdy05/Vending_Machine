A fully featured vending machine API developed using Django and Django Rest Framework.
The system implements JWT-based authentication and role-based authorization to distinguish between buyers and sellers.
Sellers are allowed to create, update, and delete only their own products, while buyers can deposit valid coin denominations, purchase available products, and receive accurate change.
The application enforces business rules such as product price validation, ownership restrictions, and secure password handling, making it suitable for real-world backend architecture and technical assessment


------------------------------ User Endpoints---------------------------


1----Obtain Access Token-----/api/token/
{
  "username": "seller1",
  "password": "password123"
}

{
  "access": "jwt_access_token",
  "refresh": "jwt_refresh_token"
}

2----Create User (Public)---/api/users/

{
  "username": "buyer1",
  "password": "password123",
  "role": "buyer"
}

3--------Get Current Users----------/api/users/

4------Update User (Self Only)--Delete User (Admin Only---/api/users/{id}/



---------------------------------------------------- Product Endpoints--------------------------------


1----------List Products (Public)---------/api/products/

2---------Create Product-----------------/api/products/
{
  "productName": "Cola",
  "cost": 10,
  "amountAvailable": 20
}

3--------Update and Delete Product (Owner Only)----/api/products/{id}/


------------------------------------------------Vending Machine Endpoints(Only Buyers)---------------------------------------

1---------Deposit Money-------/api/deposit/
{
  "coin": 20
}

2-------Buy Product-----
{
  "productId": "productName",
  "amount": 2
}

{
    "total_spent": 100,
    "product": "pro",
    "amount": 2,
    "change": {
        "100": 0,
        "50": 0,
        "20": 0,
        "10": 0,
        "5": 0
    }
}

3-------------Reset Deposit------------/api/reset/












































