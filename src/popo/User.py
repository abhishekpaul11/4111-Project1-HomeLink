from sqlalchemy import Enum


class User:
    def __init__(self, user_id, name, password, email, phone, is_tenant, is_owner, is_broker, is_repairmen, broker_successful_deals):
        self.user_id = user_id
        self.name = name
        self.password = password
        self.email = email
        self.phone = phone
        self.is_tenant = is_tenant
        self.is_owner = is_owner
        self.is_broker = is_broker
        self.is_repairmen = is_repairmen
        self.broker_successful_deals = broker_successful_deals

    def __repr__(self):
        return f"User(user_id={self.user_id}, name='{self.name}', email='{self.email}', phone='{self.phone}', is_tenant={self.is_tenant}, is_owner={self.is_owner}, is_broker={self.is_broker}, is_repairmen={self.is_repairmen}, broker_successful_deals={self.broker_successful_deals})"

    def __str__(self):
        return f"User: {self.name}, Email: {self.email}, Phone: {self.phone}"

    def get_user_type(self):
        """Determine the user type based on the user's attributes."""
        if self.is_tenant:
            return UserType.TENANT
        elif self.is_owner:
            return UserType.OWNER
        elif self.is_broker:
            return UserType.BROKER
        else:
            raise ValueError("Invalid user type")
    
    def get_user_dict(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'password': self.password,
            'email': self.email,
            'phone': self.phone,
            'is_tenant': self.is_tenant,
            'is_owner': self.is_owner,
            'is_broker': self.is_broker,
            'is_repairmen': self.is_repairmen,
            'broker_successful_deals': self.broker_successful_deals
        }

# Define the UserType Enum
class UserType(Enum):
    TENANT = "Tenant"
    OWNER = "Owner"
    BROKER = "Broker"