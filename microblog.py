# for start app
from app import app, db
from app.models import User, Post


@app.shell_context_processor
def make_shell_context():
    """make context for flask shell"""
    return {'db': db, 'User': User, 'Post': Post}
