from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY']='ldfjsolasfuasdfjsodfusoij4w09r8pswojufsldkfjdf9'

from IPL_Predictions import routes