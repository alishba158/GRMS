from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.urls import reverse

def send_email_async(user, subject, message, link=None):
    """Send email asynchronously (simplified version)"""
    try:
        if link:
            full_message = f"{message}\n\nView here: {link}"
        else:
            full_message = message
        
        send_mail(
            subject,
            full_message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"❌ Email error: {e}")
        return False


def get_full_url(request, path):
    """Get full URL for a given path"""
    if request:
        return f"http://{request.get_host()}{path}"
    return path


def send_email_to_user(subject, message, recipient_email, html_content=None):
    """Send email to a single user"""
    try:
        if html_content:
            msg = EmailMultiAlternatives(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient_email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        else:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient_email], fail_silently=False)
        return True
    except Exception as e:
        print(f"❌ Email error: {e}")
        return False


def send_password_reset_by_admin_email(user, new_password):
    """Send email to user when admin resets password"""
    subject = "🔑 Password Reset by Admin - GRMS"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; }}
            .container {{ max-width: 600px; margin: auto; background: white; padding: 30px; border-radius: 10px; }}
            .header {{ text-align: center; padding-bottom: 20px; border-bottom: 2px solid #2e7d32; }}
            .header h1 {{ color: #2e7d32; }}
            .footer {{ text-align: center; padding-top: 20px; color: #777; font-size: 12px; }}
            .password {{ background: #f0f0f0; padding: 10px; border-radius: 5px; font-family: monospace; font-size: 16px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔑 GRMS</h1>
                <p>Graduate Research Management System</p>
            </div>
            <div style="padding: 20px 0;">
                <h2>Hello {user.get_full_name() or user.username},</h2>
                <p>Your password has been reset by the administrator.</p>
                <p><strong>New Password:</strong></p>
                <p class="password">{new_password}</p>
                <p>Please login and change your password immediately.</p>
                <p style="text-align: center;">
                    <a href="http://localhost:8000/login/" class="btn">Login Now</a>
                </p>
            </div>
            <div class="footer">
                <p>© 2026 GRMS - Federal Urdu University</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    plain_message = f"""
    Password Reset by Admin - GRMS
    
    Hello {user.get_full_name() or user.username},
    
    Your password has been reset by the administrator.
    
    New Password: {new_password}
    
    Please login and change your password immediately.
    
    Thanks,
    GRMS Team
    """
    
    return send_email_to_user(subject, plain_message, user.email, html_content)