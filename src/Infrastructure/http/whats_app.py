import random
from twilio.rest import Client
import datetime

account_sid = 'your account_sid'  # precisamos substituir pelo seu account_sid do Twilio
auth_token = 'your auth_token'  # precisamos substituir pelo seu token de autenticação do Twilio
client = Client(account_sid, auth_token)
twilio_numero_whats = 'whatsapp:+14155238886'

def send_whatsapp_message(phone_number, message):
    try:
        message = client.messages.create(
            from_=twilio_numero_whats,
            body=message,
            to=f'whatsapp:{phone_number}'
        )
        print(f'Mensagem enviada para {phone_number} com sucesso')
        return True
    except Exception as e:
        print(f'Erro ao enviar mensagem via WhatsApp: {e}')
        return False

def generate_activation_code():
    return str(random.randint(1000, 9999))

def send_verification_code(phone_numbers, verification_code):
    message_body = (
        'Olá,\n'
        'Este é seu código de verificação: ' + verification_code + '\n'
        'Válido por 45 minutos'
    )
    for phone_number in phone_numbers:
        if send_whatsapp_message(phone_number, message_body):
            print(f'Mensagem enviada para {phone_number} com sucesso')
            try:
                message_sid = client.messages.list(to=f'whatsapp:{phone_number}', limit=1)[0].sid
                message_status = client.messages(message_sid).fetch().status
                print(f'Status da mensagem: {message_status}')
            except Exception as e:
                print(f'Erro ao buscar status da mensagem: {e}')
        else:
            print(f'Erro ao enviar mensagem para {phone_number}')

if __name__ == "__main__":
    # Lista de números de telefone para os quais você deseja enviar o código de verificação
    phone_numbers = [""]#adicionar os números de telefone

    # Gerar um código de ativação
    verification_code = generate_activation_code()

    # Enviar o código de verificação para os números de telefone
    send_verification_code(phone_numbers, verification_code)