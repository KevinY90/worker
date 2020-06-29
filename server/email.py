import smtplib, ssl

class EmailGenerator:
    def __init__(self, options):
        self.configure(options)

    def configure(self, options):
        for k, v in options.items():
            setattr(self, k, v)
        print(self.smtp_server, self.worker_email, self.port, self.password)

    def send_email(self, message, destination):
        print('Generate Email')
        smtp_serv, port, context = self.smtp_server, self.port, ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_serv, port, context) as server_conn:
            server_conn.login(self.worker_email, self.password)
            server.sendmail(self.sender.email, destination, message)
