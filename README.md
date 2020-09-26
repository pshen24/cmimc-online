# CMIMC Online
A website for the CMIMC Programming Competition and CMIMC 2021, which will be held online.

## Setup Instructions
1. Make sure you have [Python](https://www.python.org/downloads/) (and pip) installed on your computer.
2. Clone this repository: `git clone https://github.com/CMU-Math/cmimc-online.git`. The rest of the commands should be run within the newly created folder.
3. Follow [these](https://github.com/CMU-Math/cmimc-online#database-setup) instructions to set up the database
4. Copy the `website/example_problem_graders` folder to `website/problem_graders`. The `problem_graders` folder will store graders for the Optimization Round and AI Round problems, and is in the `.gitignore` since it should be kept private. Only the graders in `example_problem_graders` are made public.
5. Install pipenv with `pip install pipenv`, then install the rest of the dependencies with `pipenv install`
6. Activate pipenv's virtual environment with `pipenv shell`. The rest of the commands should be run within this virtual environment.
7. Then run Django migrations: `python manage.py migrate`
8. Start the Django development server: `python manage.py runserver`
9. Go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser, and you should see the home page.
10. Set up the Django Admin with [these](https://github.com/CMU-Math/cmimc-online#accessing-django-admin) instructions.

### Database setup
1. Download and install MariaDB.
    * Windows: Download it [here](https://mariadb.com/downloads/)
    * Mac: Install with Homebrew ([instructions](https://mariadb.com/kb/en/installing-mariadb-on-macos-using-homebrew/)
    * Linux: Install with your distribution's package manager, or from [here](https://mariadb.com/downloads/)
2. Create a root user and password
3. Run `mysql -u root -p` and enter the password from the previous step.
4. In the MariaDB shell, runhttps://github.com/CMU-Math/cmimc-online ```CREATE DATABASE `cmimc`;```
5. Create a `.env` file (at the root of this project's directory) with the following:
```
DEBUG=true
DB_NAME=cmimc
DB_USERNAME=root
DB_PASSWORD=your_password
```
where `your_password` is the password from step 2. Don't worry, `.env` is in the `.gititnore`, so your password won't be committed to git.

### Accessing Django Admin
1. First, create a super user account: `python manage.py createsuperuser`. You can enter any name, email, and password.
2. You can now access the Django Admin at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) using the account you just created.
3. From this admin page, you can modify all the objects in the database.


## Contributing Code
1. On the Trello page, add yourself to any projects you want to work on
2. Each project should have its own branch. Either create a new branch with `git checkout -b new-branch-name` or pull from an existing remote branch.
3. Once the changes are ready to be merged into the main branch, submit a pull request with Github's online interface.
