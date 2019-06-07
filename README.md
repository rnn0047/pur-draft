# flask-vue-spa
Vue.js SPA served over Flask microframework

* Python: 3.6.3
* Vue.js: 2.5.2
* vue-router: 3.0.1
* axios: 0.16.2

Tutorial on how I build this app:
https://medium.com/@oleg.agapov/full-stack-single-page-application-with-vue-js-and-flask-b1e036315532

## Build Setup

``` bash
# install front-end
cd frontend
npm install

# build for production/Flask with minification
npm run build

# install back-end
virtualenv -p python3 venv_vue
OR
python3 -m venv venv_vue
source venv_vue/bin/activate
pip install -r requirements.txt

# setup environment for local run
export PROJ_LOC=pur-draft
export PROJ_ROOT=$HOME/$PROJ_LOC
export MODELDIR=$PROJ_ROOT/xform
export PYTHONPATH=$PROJ_ROOT:$PROJ_ROOT/xform:$PROJ_ROOT/tools:$PROJ_ROOT/xform/src

#run app on localhost:5000 or localhost:8080 (check app.py and frontend/.env)
cd $PROJ_ROOT
python3 app.py
![alt text](tiger-style.png)
