from flask import Flask
import os
app = Flask(__name__)

app.config['SECRET_KEY']=os.environ['SK']


from IPL_Predictions import routes