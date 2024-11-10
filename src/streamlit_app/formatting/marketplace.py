from collections import OrderedDict

import streamlit as st

apartment_info_displayable = {
    'apt_address': 'ADDRESS',
    'apt_id': 'APARTMENT ID',
    'apt_manager': None,
    'apt_owner': None,
    'apt_rent': 'RENT',
    'apt_rented_date': None,
    'apt_rented_duration': None,
    'apt_rooms': 'NUMBER OF ROOMS',
    'apt_tenant': None,
    'owner_id': None,
    'manager_id': None,
    'distance_frm_fin': 'DISTANCE FROM FINANCIAL DISTRICT',
    'suburb': 'SUBURB',
    'owner_name': 'NAME',
    'owner_phone': 'PHONE',
    'owner_email': 'EMAIL',
    'manager_name': 'NAME',
    'manager_phone': 'PHONE',
    'manager_email': 'EMAIL'
}

def format_value(value):
    return value if value is not None else "Not Available"

def display_apt(apartment_info):
    st.markdown(
        """
        <style>
        .box {
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 2px;
            background-color: #ccc;
        }
        .field {
            margin-bottom: 5px;
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
            left: 400px;
            position: absolute;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="box">', unsafe_allow_html=True)

    owner_id = apartment_info['owner_id']
    manager_id = apartment_info['manager_id']

    apartment_info_ordered = OrderedDict()
    for key in apartment_info_displayable.keys():
        apartment_info_ordered[key] = apartment_info[key]

    apartment_info_ordered['owner_id'] = owner_id

    for key, value in apartment_info_ordered.items():
        if key == 'distance_frm_fin':
            value = f"{value} kms"
        elif key == 'apt_rent':
            value = f"$ {value}"

        key_to_be_displayed = apartment_info_displayable[key]
        if key_to_be_displayed is not None:
            if key in ['manager_name'] and owner_id != manager_id:
                st.markdown(
                    f'<div class="sub-field"><span class="key">MANAGER DETAILS</span></div>',unsafe_allow_html=True)
            elif key in ['owner_name']:
                st.markdown(
                    f'<div class="sub-field"><span class="key">OWNER DETAILS</span></div>', unsafe_allow_html=True)

            if owner_id != manager_id:
                key_list = ['owner_name', 'owner_phone', 'owner_email', 'manager_name', 'manager_phone', 'manager_email']
                ignored_key_list = []
            else:
                key_list = ['owner_name', 'owner_phone', 'owner_email']
                ignored_key_list = ['manager_name', 'manager_phone', 'manager_email']

            if key in key_list:
                st.markdown(f'<div class="field"><span class="sub-key">{key_to_be_displayed}</span> <span class="value">{value}</span></div>', unsafe_allow_html=True)
            elif key not in ignored_key_list:
                st.markdown(f'<div class="field"><span class="key">{key_to_be_displayed}</span> <span class="value">{value}</span></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)