import smtplib
from email.mime.text import MIMEText


def send_mail(customer, teacher, rating, comments):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = 'd5a74d4770f049'
    password = 'a14a52ed6e8c8b'
    message = f"<h3>New Feedback Submission</h3><ul><li>Cellist: {customer}</li><li>Teacher: {teacher}</li><li>Rating: {rating}</li><li>Comments: {comments}</li></ul>"

    sender_email = 'email1@example.com'
    receiver_email = 'email2@example.com'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Cello Lesson Feedback'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
