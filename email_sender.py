from email.message import EmailMessage
import ssl
import smtplib

def send_questions_email(email_sender, email_password, user_email, questions):
    print("👻", questions)
    formatted_questions = "\n".join(questions)

    body = f"""
    Hello,

    Here are the questions you've asked:

    {formatted_questions}
    Thank you for using VA

    Regards,
    Your Virtual Assistant
    """

    em = EmailMessage()
    em['From'] = 'pythontestingphase3@gmail.com'
    em['To'] = user_email
    em['Subject'] = "Your Asked Questions"
    em.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.send_message(em)
