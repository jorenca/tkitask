# tkitask


## Setting up for local development

### Create a virtual env
Use your favourite virtual env manager to setup an environment with `python>=3.10`
```bash
pyenv install 3.10.16
pyenv virtualenv 3.10.16 tkitask-env
pyenv activate tkitask-env
```

### Install dependencies
```bash
pip install poetry
poetry install
```

### Install PostgreSQL DB
```bash
sudo apt install postgresql
```

### Prepare questions dataset
Pull the questions:
```bash
cd dataset
curl https://raw.githubusercontent.com/russmatney/go-jeopardy/refs/heads/master/JEOPARDY_CSV.csv -o dataset.csv
```



