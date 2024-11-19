from collections import OrderedDict
from datetime import datetime

import streamlit as st

apt_info_displayable = {
    'apt_address': 'Address',
    'apt_rent': 'Monthly Rent',
    'apt_rooms': 'Number of Rooms',
    'distance_frm_fin': 'Distance from Financial District',
    'suburb': 'Suburb',
    'owner_name': 'Name',
    'owner_email': 'Email',
    'owner_phone': 'Phone',
    'tenant_name': 'Name',
    'tenant_email': 'Email',
    'tenant_phone': 'Phone',
    'apt_rented_date': 'Rented Date',
    'apt_rented_duration': 'Rented Duration',
}


def format_date(value):
    dt_object = datetime.strptime(str(value), "%a, %d %b %Y %H:%M:%S %Z")
    return dt_object.strftime("%a, %d %b %Y")

def display_apartment_for_broker(apt_info):
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
    st.subheader(f"Apartment {apt_info['apt_id']}")

    st.markdown('<div class="box">', unsafe_allow_html=True)

    tenant_id = apt_info['apt_tenant']

    apt_info_ordered = OrderedDict()
    for key in apt_info_displayable.keys():
        apt_info_ordered[key] = apt_info.get(key)

    for key, value in apt_info_ordered.items():

        if key == 'apt_rent':
            value = f"$ {value}"
        elif key == 'apt_rented_duration':
            value = f"{value} months"
        elif key == 'distance_frm_fin':
            value = f"{value} kms"
        elif key == 'apt_rented_date' and value is not None:
            value = format_date(value)

        key_to_be_displayed = apt_info_displayable[key].upper()

        if key_to_be_displayed is not None:

            if key == 'owner_name':
                st.markdown(f'<div class="sub-field"><span class="key">OWNER DETAILS</span></div>', unsafe_allow_html=True)

            if key == 'tenant_name':
                if tenant_id is not None:
                    st.markdown(f'<div class="sub-field"><span class="key">TENANT DETAILS</span></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="sub-field"><span class="key">TENANT DETAILS</span><span class="value"><i>Apartment not occupied</i></span></div></div>', unsafe_allow_html=True)

            tenant_key_list = ['tenant_name', 'tenant_email', 'tenant_phone', 'apt_rented_date', 'apt_rented_duration']
            manager_key_list = ['owner_name', 'owner_email', 'owner_phone']

            if key in tenant_key_list or key in manager_key_list:
                if key in manager_key_list:
                    st.markdown(
                        f'<div class="field"><span class="sub-key">{key_to_be_displayed}</span> <span class="value">{value}</span></div>',
                        unsafe_allow_html=True)

                if key in tenant_key_list and tenant_id is not None:
                    st.markdown(
                        f'<div class="field"><span class="sub-key">{key_to_be_displayed}</span> <span class="value">{value}</span></div>',
                        unsafe_allow_html=True)
            else:
                st.markdown(
                    f'<div class="field"><span class="key">{key_to_be_displayed}</span> <span class="value">{value}</span></div>',
                    unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
