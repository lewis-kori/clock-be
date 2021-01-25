# Setup

1. Clone the repository.
2. Change directory to the location of this repository.
3. Create a `.env` file using the included `.env.example` as an example.
4. Create and start your preferred Python virtual environment(python 3.9 >). Install the required libraries.

```bash
pip install -r requirements.txt
```

## Usage

To run locally:

```bash
python manage.py migrate
python manage.py runserver
```

## Development

Pull the latest main version:

```bash
git pull origin main
```

Create local development branch and switch to it:

```bash
git branch <branch_name>
git checkout <branch_name>
```

Make desired changes then commit the branch.

```bash
git add .
git commit -m "changes to <branch_name> branch"
git push origin <branch_name>
```

**other documentation in the various django apps.**
