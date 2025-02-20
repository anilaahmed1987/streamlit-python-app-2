from streamlit.web import bootstrap
from streamlit import config

def handler(event, context):
    config.set_option('server.address', '0.0.0.0')
    config.set_option('server.port', 8501)
    bootstrap.run('../app.py', '', [], {}) 