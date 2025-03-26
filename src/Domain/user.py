class UserDomain:
    def __init__(self, name, cnpj, email, phone, password, status="Inativo"):
        self.name = name
        self.cnpj = cnpj
        self.email = email
        self.phone = phone
        self.password = password
        self.status = status
        self.activation_code = None
    
    def to_dict(self):
        return {
            "name": self.name,
            "cnpj": self.cnpj,
            "email": self.email,
            "phone": self.phone,
            "password": self.password,
            "status": self.status
        }
    
    