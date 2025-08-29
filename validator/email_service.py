from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class EmailService:
    """Servicio para el envío de correos electrónicos de validación de titularidad"""
    
    #! EMAIL DE CANALES PARA QUEMARLO
    ADMIN_EMAIL = 'analista.canales@congente.coop'
    
    @staticmethod
    def send_approval_emails(user_info: dict, user_answers: dict, monto_aprobado: str = None):
        """
        Envía correos de aprobación tanto al asociado como al administrador.
        
        Args:
            user_info (dict): Información del usuario (debe incluir 'mail')
            user_answers (dict): Respuestas del usuario validadas como correctas
            monto_aprobado (str): Monto aprobado obtenido del procedimiento
        """
        try:
            #* Envío al asociado
            EmailService._send_approval_user_email(user_info, user_answers)
            
            #* Envío al administrador
            EmailService._send_approval_admin_email(user_info, user_answers, monto_aprobado)
            
            logger.info(f"Correos de aprobación enviados exitosamente para cédula: {user_info.get('cedula')}")
            
        except Exception as e:
            logger.error(f"Error al enviar correos de aprobación: {e}", exc_info=True)
            raise
    
    @staticmethod
    def send_rejection_emails(user_info: dict):
        """
        Envía correos de rechazo tanto al asociado como al administrador.
        
        Args:
            user_info (dict): Información del usuario (debe incluir 'mail')
        """
        try:
            #* Envío al asociado
            EmailService._send_rejection_user_email(user_info)
            
            #* Envío al administrador
            EmailService._send_rejection_admin_email(user_info)
            
            logger.info(f"Correos de rechazo enviados exitosamente para cédula: {user_info.get('cedula')}")
            
        except Exception as e:
            logger.error(f"Error al enviar correos de rechazo: {e}", exc_info=True)
            raise
    
    @staticmethod
    def _send_approval_user_email(user_info: dict, user_answers: dict):
        """Envía correo de aprobación al asociado"""
        user_email = user_info.get('mail')
        if not user_email:
            logger.warning("No se puede enviar correo al usuario: email no disponible")
            return
        
        subject = "✅ Validación de Titularidad Aprobada - ConGente"
        
        #* Contexto para el template
        context = {
            'nombre': user_info.get('nombre', 'Estimado(a) Asociado(a)'),
            'cedula': user_info.get('cedula'),
            'user_answers': user_answers,
            'fecha': user_info.get('fecha_expedicion')
        }
        
        #* Renderizar template HTML
        html_message = render_to_string('emails/approval_user.html', context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            html_message=html_message,
            fail_silently=False
        )
        
        logger.info(f"Correo de aprobación enviado al usuario: {user_email}")
    
    @staticmethod
    def _send_approval_admin_email(user_info: dict, user_answers: dict, monto_aprobado: str):
        """Envía correo de aprobación al administrador"""
        subject = f"✅ Validación Aprobada - {user_info.get('nombre')} ({user_info.get('cedula')})"
        
        context = {
            'nombre': user_info.get('nombre'),
            'cedula': user_info.get('cedula'),
            'email_usuario': user_info.get('mail'),
            'telefono_opcional': user_info.get('telefono'),
            'user_answers': user_answers,
            'monto_aprobado': monto_aprobado,
            'fecha_expedicion': user_info.get('fecha_expedicion')
        }
        
        html_message = render_to_string('emails/approval_admin.html', context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[EmailService.ADMIN_EMAIL],
            html_message=html_message,
            fail_silently=False
        )
        
        logger.info(f"Correo de aprobación enviado al administrador para usuario: {user_info.get('cedula')}")
    
    @staticmethod
    def _send_rejection_user_email(user_info: dict):
        """Envía correo de rechazo al asociado"""
        user_email = user_info.get('mail')
        if not user_email:
            logger.warning("No se puede enviar correo al usuario: email no disponible")
            return
        
        subject = "🔒 Validación de Titularidad - Información Requerida - ConGente"
        
        context = {
            'nombre': user_info.get('nombre', 'Estimado(a) Asociado(a)'),
            'cedula': user_info.get('cedula')
        }
        
        html_message = render_to_string('emails/rejection_user.html', context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            html_message=html_message,
            fail_silently=False
        )
        
        logger.info(f"Correo de rechazo enviado al usuario: {user_email}")
    
    @staticmethod
    def _send_rejection_admin_email(user_info: dict):
        """Envía correo de rechazo al administrador"""
        subject = f"❌ Validación Fallida - {user_info.get('nombre')} ({user_info.get('cedula')})"
        
        context = {
            'nombre': user_info.get('nombre'),
            'cedula': user_info.get('cedula'),
            'email_usuario': user_info.get('mail'),
            'fecha_expedicion': user_info.get('fecha_expedicion')
        }
        
        html_message = render_to_string('emails/rejection_admin.html', context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[EmailService.ADMIN_EMAIL],
            html_message=html_message,
            fail_silently=False
        )
        
        logger.info(f"Correo de rechazo enviado al administrador para usuario: {user_info.get('cedula')}")