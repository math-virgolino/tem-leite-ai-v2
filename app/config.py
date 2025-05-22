import os

class Config:
    # Configuração do Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave-secreta-padrao-para-desenvolvimento'
    
    # Configuração do SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///instance/tem_leite_ai.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuração de upload de arquivos
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    
    # Configuração de geolocalização
    NOMINATIM_USER_AGENT = "tem_leite_ai_app"
    MAX_DISTANCE_KM = 50  # Distância máxima para busca de doadores em km
