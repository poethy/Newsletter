from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from app.models import Subscriber
from app import db, mail
import secrets
from flask_mail import Message
import html

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    name = request.form.get('name')
    
    if not email:
        flash('El email es requerido', 'error')
        return redirect(url_for('main.index'))
    
    if Subscriber.query.filter_by(email=email).first():
        flash('Este email ya está suscrito', 'error')
        return redirect(url_for('main.index'))
    
    subscriber = Subscriber(
        email=email,
        name=name,
        unsubscribe_token=secrets.token_urlsafe(32)
    )
    
    db.session.add(subscriber)
    db.session.commit()
    
    # Enviar correo de bienvenida
    try:
        # Codificar el nombre para evitar problemas con caracteres especiales
        safe_name = html.escape(name if name else 'Suscriptor')
        
        msg = Message(
            subject='Bienvenido a nuestro Newsletter',
            sender=current_app.config['MAIL_USERNAME'],
            recipients=[email]
        )
        
        # Mensaje simple sin caracteres especiales
        msg.body = f"""
        Hola {safe_name}!
        
        Gracias por suscribirte a nuestro newsletter.
        
        Para cancelar tu suscripción, usa este enlace:
        {url_for('main.unsubscribe', token=subscriber.unsubscribe_token, _external=True)}
        
        Saludos,
        El equipo de Newsletter
        """
        
        # Versión HTML del mensaje
        msg.html = f"""
        <h2>Hola {safe_name}!</h2>
        
        <p>Gracias por suscribirte a nuestro newsletter.</p>
        
        <p>Para cancelar tu suscripción, haz clic 
        <a href="{url_for('main.unsubscribe', token=subscriber.unsubscribe_token, _external=True)}">aquí</a>.</p>
        
        <p>Saludos,<br>
        El equipo de Newsletter</p>
        """
        
        mail.send(msg)
        flash('¡Gracias por suscribirte! Te hemos enviado un correo de bienvenida.', 'success')
    except Exception as e:
        print(f"Error al enviar correo: {str(e)}")
        flash('¡Gracias por suscribirte! (No se pudo enviar el correo de bienvenida)', 'warning')
    
    return redirect(url_for('main.index'))

@bp.route('/unsubscribe/<token>')
def unsubscribe(token):
    subscriber = Subscriber.query.filter_by(unsubscribe_token=token).first()
    
    if subscriber:
        subscriber.is_active = False
        db.session.commit()
        flash('Te has desuscrito exitosamente', 'success')
    else:
        flash('Token de desuscripción inválido', 'error')
    
    return redirect(url_for('main.index'))