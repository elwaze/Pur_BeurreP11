# PurBeurre_P10
Openclassrooms DA-Python P10 Pur Beurre: 
Déployez votre application sur un serveur comme un pro

### Déploiement du P8 sur un serveur, intégration continue et monitoring

### projet déployé : http://165.22.199.87/

### Constraints
tests included in the project

use of PostgreSql to deploy the project with Heroku

include a page with "Mentions Légales"

PEP8 compliant

Github versioning

code written in english

agile methodology

### How to use this program

You can find this program deployed on Heroku : https://elwaze-purbeurre.herokuapp.com/

You can also fork this repository :
```bash
git clone "https://github.com/elwaze/PurBeurre_P8.git"
```

Use requirements.txt to install the program environment:
```bash
pip install -r requirements.txt
```

Setting environment variables 
```bash
DATABASE_URL
ENV="PRODUCTION"
SECRET_KEY
```

Populating DB
```bash
python manage.py off_db
```

Running the program
```bash
python manage.py runserver
```

### Testing

#### Coverage

**Remove coverage_html_report folder** to ensure no previous generated files remains.

**.coveragerc** file has been created to finely tune the coverage behavior.

```bash
coverage erase
coverage run manage.py test tests.apps --settings=pur_beurre.settings.test_settings
coverage h
```
