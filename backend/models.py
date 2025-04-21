# models.py

from datetime import datetime
from app import db  # Importa o objeto db do app.py

class Bookmark(db.Model):
    __tablename__ = 'bookmarks'  # Nome da tabela no banco de dados

    # Definindo as colunas da tabela
    id = db.Column(db.Integer, primary_key=True)  # Coluna de ID (chave primária)
    title = db.Column(db.String(255), nullable=False)  # Coluna de título
    url = db.Column(db.String(255), nullable=False)  # Coluna de URL
    remember_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)  # Coluna de data

    def __repr__(self):
        return f'<Bookmark {self.title}>'
