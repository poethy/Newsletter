// Cerrar alertas automáticamente después de 5 segundos
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.remove();
            }, 300);
        }, 5000);
    });
});

// Confirmar antes de enviar un newsletter
function confirmSendNewsletter(event) {
    if (!confirm('¿Estás seguro de que deseas enviar este newsletter a todos los suscriptores?')) {
        event.preventDefault();
    }
}

// Validar formulario de suscripción
function validateSubscriptionForm(event) {
    const email = document.getElementById('email').value;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    if (!emailRegex.test(email)) {
        alert('Por favor, ingresa un correo electrónico válido.');
        event.preventDefault();
    }
}

// Agregar validación al formulario de suscripción
const subscriptionForm = document.querySelector('form[action*="subscribe"]');
if (subscriptionForm) {
    subscriptionForm.addEventListener('submit', validateSubscriptionForm);
}

// Agregar confirmación al botón de enviar newsletter
const sendNewsletterButtons = document.querySelectorAll('a[href*="/send"]');
sendNewsletterButtons.forEach(button => {
    button.addEventListener('click', confirmSendNewsletter);
}); 