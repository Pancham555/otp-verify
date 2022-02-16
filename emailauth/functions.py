from django.core.mail import EmailMessage
def sendemail(otp,email,hostemail):
    sendmail = EmailMessage(
            'Email Verification',
            f'''Please verify your email with the otp given below.\n {otp} 
            This otp is valid only for 5 minutes. \n Please ignore if you din't send this
            Thank you.''',
            hostemail,
            [email or 'panchamb63@gmail.com']
        )
        # sendmail.attach_file('templates/index.html')
    sendmail.fail_silently = False
    sendmail.send()