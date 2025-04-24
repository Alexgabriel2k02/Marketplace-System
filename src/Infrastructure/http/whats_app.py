import random
from twilio.rest import Client
import datetime

account_sid = "sua conta "  # Substitua pelo seu account_sid do Twilio
auth_token = "seu token"  # Substitua pelo seu token de autenticação do Twilio
client = Client(account_sid, auth_token)
twilio_numero_whats = "whatsapp:+14155238886"


def send_whatsapp_message(phone_number, message):
    try:
        message = client.messages.create(
            from_=twilio_numero_whats, body=message, to=f"whatsapp:{phone_number}"
        )
        print(f"Mensagem enviada para {phone_number} com sucesso")
        return True
    except Exception as e:
        print(f"Erro ao enviar mensagem via WhatsApp: {e}")
        return False


def generate_activation_code():
    return str(random.randint(1000, 9999))


def send_verification_code(phone_number, verification_code):
    message_body = (
        "Olá,\n"
        "Este é seu código de verificação: " + verification_code + "\n"
        "Válido por 45 minutos"
    )
    try:
        # Certifique-se de que o número é uma string
        if isinstance(phone_number, list):
            phone_number = phone_number[0]  # Extrai o número da lista, se necessário

        # Envia a mensagem
        message = client.messages.create(
            from_=twilio_numero_whats,
            body=message_body,
            to=f"whatsapp:{phone_number}",  # Certifique-se de que o número está no formato correto
        )
        print(f"Mensagem enviada para {phone_number} com sucesso. SID: {message.sid}")

        # Busca o status da mensagem
        message_status = client.messages(message.sid).fetch().status
        print(f"Status da mensagem: {message_status}")
        return True
    except Exception as e:
        print(f"Erro ao enviar mensagem ou buscar status: {e}")
        return False


if __name__ == "__main__":
    phone_number = "+5511975682004"  # Substitua pelo número de telefone de destino
    verification_code = generate_activation_code()
    if send_verification_code(phone_number, verification_code):
        print("Mensagem enviada com sucesso!")
    else:
        print("Falha ao enviar a mensagem.")
