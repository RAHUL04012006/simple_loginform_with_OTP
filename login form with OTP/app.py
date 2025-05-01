from flask import Flask, g, session
from models.user import db
from routes.auth import auth
import os
from flask import render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Register blueprints
app.register_blueprint(auth)

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        from models.user import User
        g.user = User.query.get(session['user_id'])

@app.context_processor
def inject_user():
    return dict(current_user=g.user)

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 