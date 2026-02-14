from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from database import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    JWTManager(app)
    init_db(app)
    
    # Import and register blueprints
    from routes.auth import bp as auth_bp
    from routes.students import bp as students_bp
    from routes.teachers import bp as teachers_bp
    from routes.classes import bp as classes_bp
    from routes.attendance import bp as attendance_bp
    from routes.fees import bp as fees_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(students_bp, url_prefix='/api/students')
    app.register_blueprint(teachers_bp, url_prefix='/api/teachers')
    app.register_blueprint(classes_bp, url_prefix='/api/classes')
    app.register_blueprint(attendance_bp, url_prefix='/api/attendance')
    app.register_blueprint(fees_bp, url_prefix='/api/fees')
    
    @app.route('/')
    def index():
        return jsonify({'message': 'School Management API', 'version': '1.0'})
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)