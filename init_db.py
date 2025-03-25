from app import create_app, db
from app.models import User

def init_db():
    app = create_app()
    with app.app_context():
        # Crear todas las tablas
        db.create_all()
        
        # Crear usuario administrador si no existe
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@example.com',
                is_admin=True
            )
            admin.set_password('admin123')  # Cambia esta contraseña en producción
            db.session.add(admin)
            db.session.commit()
            print('Usuario administrador creado exitosamente')
        else:
            print('El usuario administrador ya existe')

if __name__ == '__main__':
    init_db() 