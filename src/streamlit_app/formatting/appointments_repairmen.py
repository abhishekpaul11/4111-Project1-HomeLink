from collections import OrderedDict
from datetime import datetime

import streamlit as st

appointment_info_displayable = {
    'appointment_date': 'Date',
    'charges': 'Charges',
    'duration': 'Duration',
    'issue_id': 'Issue ID',
    'issue_description': 'Description',
    'apartment_id': 'ID',
    'apartment_address': 'Address',
    'apartment_suburb': 'Suburb',
    'tenant_name': 'Name',
    'tenant_email': 'Email',
    'tenant_phone': 'Phone'
}

def format_date(value):
    dt_object = datetime.strptime(str(value), "%a, %d %b %Y %H:%M:%S %Z")
    return dt_object.strftime("%a, %d %b %Y")

def display_appointment_for_repairmen(appointment_info):
    st.markdown(
        """
            <style>
            .box {
                border: 1px solid #ddd;
                border-radius: 10px;
                padding: 2px;
                background-color: #f9f9f9;
            }
            .field {
                margin-bottom: 8px;
                font-size: 16px;
                font-weight: 900;
            }
            .sub-field {
                height: 50px;
                display: flex;
                flex-direction: column;
                justify-content: flex-end;
                font-size: 16px;
                font-weight: 900;
                color: #6f42c1;
            }
            .key {
                color: #6f42c1;
            }
            .sub-key {
                color: #6f42c1;
                margin-left: 20px;
            }
            .value {
                position: absolute;
                left: 400px;
                font-weight: 900;
            }
            </style>
        """,
        unsafe_allow_html=True
    )

    st.subheader(f"Appointment {appointment_info['appointment_id']}")

    st.markdown('<div class="box">', unsafe_allow_html=True)

    apt_info_ordered = OrderedDict()
    for key in appointment_info_displayable.keys():
        apt_info_ordered[key] = appointment_info.get(key)

    for key, value in apt_info_ordered.items():
        if key == 'appointment_date' and value is not None:
            value = format_date(value)
        elif key == 'charges':
            value = f"$ {value}"
        elif key == 'duration':
            value = f"{value} hour(s)"

        if key == 'tenant_name':
            st.markdown('<div class="sub-field">TENANT DETAILS</div>', unsafe_allow_html=True)

        if key == 'apartment_id':
            st.markdown('<div class="sub-field">APARTMENT DETAILS</div>', unsafe_allow_html=True)

        field_label = appointment_info_displayable[key].upper()
        tenant_key_list = ['tenant_name', 'tenant_email', 'tenant_phone']
        apt_key_list = ['apartment_id', 'apartment_address', 'apartment_suburb']

        if key in tenant_key_list or key in apt_key_list:
            st.markdown(
                f'<div class="field"><span class="sub-key">{field_label}</span> <span class="value">{value}</span></div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="field"><span class="key">{field_label}</span><span class="value">{value}</span></div>',
                unsafe_allow_html=True
            )

    st.markdown('</div>', unsafe_allow_html=True)
