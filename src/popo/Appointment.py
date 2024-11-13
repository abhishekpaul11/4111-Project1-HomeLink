from dataclasses import dataclass
from typing import Optional
import streamlit as st


@dataclass
class Appointment:
    appointment_id: int
    appointment_date: str
    duration: int
    charges: int
    issue_id: Optional[int]
    apt_id: Optional[int]
    repairmen_id: Optional[int]

    def display_appointment(self, st:st):
        st.text(f"Appointment ID: {self.appointment_id}")
        st.text(f"Date: {self.appointment_date}")
        st.text(f"Duration: {self.duration} minutes")
        st.text(f"Charges: ${self.charges}")
        if self.issue_id:
            st.text(f"Issue ID: {self.issue_id}")
        if self.apt_id:
            st.text(f"Apartment ID: {self.apt_id}")
        if self.repairmen_id:
            st.text(f"Repairman ID: {self.repairmen_id}")
        st.text("")