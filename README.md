# CMIMC Online
A website for the CMIMC Programming Competition and CMIMC 2021, which will be held online.

## Setup Instructions
1. Make sure you have [Python](https://www.python.org/downloads/) (and pip) installed on your computer.
2. Clone this repository: `git clone https://github.com/CMU-Math/cmimc-online.git`. The rest of the commands should be run within the newly created folder.
3. Install [MariaDB](https://mariadb.com/) and create a root user (make sure to remember the password!)
4. Run `mysql -u root -p` and enter the root password from the previous step.
5. In the MariaDB shell, run ```CREATE DATABASE `cmimc`;```
6. Create a .env file with the following:
'''
DEBUG=true
DB_NAME=cmimc
DB_USERNAME=your_username
DB_PASSWORD=your_password
'''
7. Install pipenv with `pip install pipenv`, then install the rest of the dependencies with `pipenv install`
8. Activate pipenv's virtual environment with `pipenv shell`. The rest of the commands should be run within this virtual environment.
9. Then run Django migrations: `python manage.py migrate`
10. Start the Django development server: `python manage.py runserver`
11. Go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser, and you should see the home page.

### Accessing Djanog Admin
1. First, create a super user account: `python manage.py createsuperuser`. You can enter any name, email, and password.
2. You can now access the Django Admin at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) using the account you just created.
3. From this admin page, you can modify all the objects in the database.
