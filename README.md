# Thrifty Ecommerce Website

This is an ecommerce website built using HTML, CSS, and JavaScript in the frontend, and Python and Django in the backend.

## Features

The website includes the following features:

- User registration and login
- Cart functionality for both logged in and logged out users
- Custom checkout and shipping functionality for both logged in and logged out users
- Order history and status tracking
- Authentication functionalities such as password reset and email verification

## Installation

To install and run the website locally, follow these steps:

1. Clone the repository:

```
git clone https://github.com/Happy-huh/ecommerce-website.git
```

2. Create a virtual environment and activate it:

```
cd e_com
python -m venv env
source env/bin/activate
```

3. Install the required packages:

```
pip install -r requirements.txt
```

4. Create the database and run migrations:

```
python manage.py migrate
```

5. Create a superuser:

```
python manage.py createsuperuser
```

6. Run the server:

```
python manage.py runserver
```

7. Open your browser and navigate to `http://localhost:8000` to view the website.

## Usage

To use the website, you can:

- Create an account and log in
- Browse products and add them to your cart (cart functionality available for both logged in and logged out users)
- Proceed to checkout and enter your shipping details (custom checkout and shipping functionality available for both logged in and logged out users)
- Enter your payment details and complete your order
- View your order history and status

## Contributing

If you'd like to contribute to the project, feel free to submit a pull request or create an issue.

## Credits

This website was built by [Onyedika Akujieze](https://github.com/Happy-huh).

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).