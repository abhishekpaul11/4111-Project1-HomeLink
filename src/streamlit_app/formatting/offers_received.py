from collections import OrderedDict
import streamlit as st

offer_info_displayable = {
    'offer_id': 'OFFER ID',
    'offered_price': 'OFFERED PRICE',
    'tenant_id': 'TENANT ID',
    'apt_id': 'APARTMENT ID',
    'duration': 'DURATION'
}


def format_value(value):
    return value if value is not None else "Not Available"


def display_offer(offer_info):
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

    offer_info_ordered = OrderedDict()
    for key in offer_info_displayable.keys():
        offer_info_ordered[key] = offer_info[key]

    for key, value in offer_info_ordered.items():
        if key == 'offered_price':
            value = f"$ {value}"
        elif key == 'duration':
            value = f"{value} month(s)"

        key_to_be_displayed = offer_info_displayable[key]

        st.markdown(
            f'<div class="field"><span class="key">{key_to_be_displayed}</span> <span class="value">{value}</span></div>',
            unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
