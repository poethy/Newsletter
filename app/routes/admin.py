from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Newsletter, Subscriber
from app import db, mail
from flask_mail import Message
from datetime import datetime
from functools import wraps

bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('No tienes permisos para acceder a esta página', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/dashboard')
@admin_required
def dashboard():
    subscribers = Subscriber.query.filter_by(is_active=True).count()
    newsletters = Newsletter.query.all()
    return render_template('admin/dashboard.html', 
                         subscribers=subscribers,
                         newsletters=newsletters)

@bp.route('/newsletter/new', methods=['GET', 'POST'])
@admin_required
def new_newsletter():
    if request.method == 'POST':
        subject = request.form.get('subject')
        content = request.form.get('content')
        
        if not subject or not content:
            flash('El asunto y el contenido son requeridos', 'error')
            return redirect(url_for('admin.new_newsletter'))
        
        newsletter = Newsletter(
            subject=subject,
            content=content,
            created_by=current_user
        )
        
        db.session.add(newsletter)
        db.session.commit()
        
        flash('Newsletter creado exitosamente', 'success')
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/new_newsletter.html')

@bp.route('/newsletter/<int:id>/send')
@admin_required
def send_newsletter(id):
    newsletter = Newsletter.query.get_or_404(id)
    subscribers = Subscriber.query.filter_by(is_active=True).all()
    
    for subscriber in subscribers:
        msg = Message(
            subject=newsletter.subject,
            sender=current_user.email,
            recipients=[subscriber.email]
        )
        msg.body = newsletter.content
        msg.html = newsletter.content
        
        # Agregar link de desuscripción
        unsubscribe_url = url_for('main.unsubscribe', 
                                 token=subscriber.unsubscribe_token, 
                                 _external=True)
        msg.html += f'<br><br><a href="{unsubscribe_url}">Desuscribirse</a>'
        
        mail.send(msg)
    
    newsletter.sent_at = datetime.utcnow()
    newsletter.status = 'sent'
    db.session.commit()
    
    flash('Newsletter enviado exitosamente', 'success')
    return redirect(url_for('admin.dashboard'))

@bp.route('/subscribers')
@admin_required
def list_subscribers():
    subscribers = Subscriber.query.all()
    return render_template('admin/subscribers.html', subscribers=subscribers)

@bp.route('/subscriber/<int:id>/toggle', methods=['POST'])
@admin_required
def toggle_subscriber(id):
    subscriber = Subscriber.query.get_or_404(id)
    subscriber.is_active = not subscriber.is_active
    db.session.commit()
    
    status = "activado" if subscriber.is_active else "desactivado"
    flash(f'Suscriptor {subscriber.email} {status} exitosamente', 'success')
    return redirect(url_for('admin.list_subscribers'))

@bp.route('/subscriber/<int:id>/delete', methods=['POST'])
@admin_required
def delete_subscriber(id):
    subscriber = Subscriber.query.get_or_404(id)
    db.session.delete(subscriber)
    db.session.commit()
    
    flash(f'Suscriptor {subscriber.email} eliminado exitosamente', 'success')
    return redirect(url_for('admin.list_subscribers'))

@bp.route('/newsletter/<int:id>/delete', methods=['POST'])
@admin_required
def delete_newsletter(id):
    newsletter = Newsletter.query.get_or_404(id)
    db.session.delete(newsletter)
    db.session.commit()
    
    flash('Newsletter eliminado exitosamente', 'success')
    return redirect(url_for('admin.dashboard')) 