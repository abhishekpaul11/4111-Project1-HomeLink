from dataclasses import dataclass
from typing import Optional


@dataclass
class Apartment:
    apt_id: int
    apt_address: str
    apt_rent: int
    apt_rooms: int
    suburb: str
    apt_owner: int  # Foreign key to Users(user_id)
    apt_manager: int  # Foreign key to Users(user_id)
    distance_frm_fin: Optional[int] = None
    apt_tenant: Optional[int] = None  # Foreign key to Users(user_id), unique (One-to-One)
    apt_rented_date: Optional[str] = None  # Store date as string (could use datetime type if needed)
    apt_rented_duration: Optional[int] = None  # Duration in months or years

    def __repr__(self):
        return f"Apartment(apt_id={self.apt_id}, apt_address='{self.apt_address}', apt_rent={self.apt_rent}, " \
               f"apt_rooms={self.apt_rooms}, suburb='{self.suburb}', distance_frm_fin={self.distance_frm_fin}, " \
               f"apt_owner={self.apt_owner}, apt_manager={self.apt_manager}, apt_tenant={self.apt_tenant}, " \
               f"apt_rented_date='{self.apt_rented_date}', apt_rented_duration={self.apt_rented_duration})"

    def __str__(self):
        return f"Apartment ID: {self.apt_id}, Address: {self.apt_address}, Rent: {self.apt_rent}, " \
               f"Rooms: {self.apt_rooms}, Suburb: {self.suburb}, Rented Duration: {self.apt_rented_duration} months"