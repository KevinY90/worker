import smtplib, ssl

class EmailGenerator:
    def __init__(self, options):
        self.configure(options)

    def configure(self, options):
        for k, v in options.items():
            setattr(self, k, v)

    def send_email(self, message, destination):
        smtp_serv, port, context = self.smtp_server, self.port, ssl.create_default_context()
        with smtplib.SMTP(smtp_serv, port) as email_server:
            email_server.ehlo()
            email_server.starttls(context=context)
            email_server.ehlo()
            email_server.login(self.worker_email, self.password)
            email_server.sendmail(self.worker_email, destination, message)

