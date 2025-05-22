from flask import Flask
from app.extensions import db, login_manager
import os

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    # Configuração direta sem importar config.py
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'chave-secreta-padrao-para-desenvolvimento'
    
    # Garantir que a pasta instance existe antes de configurar o banco de dados
    # Criar o caminho completo para a pasta instance
    instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'instance')
    os.makedirs(instance_path, exist_ok=True)
    
    # Configurar o caminho do banco de dados com caminho absoluto para evitar problemas no Windows
    db_path = os.path.join(instance_path, 'tem_leite_ai.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
    app.config['NOMINATIM_USER_AGENT'] = "tem_leite_ai_app"
    app.config['MAX_DISTANCE_KM'] = 50  # Distância máxima para busca de doadores em km
    
    # Garantir que a pasta uploads existe
    uploads_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
    os.makedirs(uploads_path, exist_ok=True)
    
    # Inicializar extensões
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    
    # Importar e registrar rotas usando a função init_routes do routes.py
    from app.routes import init_routes
    init_routes(app)
    
    # Criar tabelas do banco de dados
    with app.app_context():
        db.create_all()
    
    return app
