from flask import Flask
import os
app = Flask(__name__)

app.config['SECRET_KEY']="271faea3aee44b3d1011bd01be4dca553a654a8fae852641"


from IPL_Predictions import routes