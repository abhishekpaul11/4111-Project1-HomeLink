from collections import OrderedDict
from datetime import datetime

import streamlit as st

issue_info_displayable = {
    'issue_description': 'DESCRIPTION',
    'issue_date': 'DATE'
}

def format_date(value):
    dt_object = datetime.strptime(str(value), "%a, %d %b %Y %H:%M:%S %Z")
    return dt_object.strftime("%a, %d %b %Y")

def display_issue(issue_info):
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

    st.subheader(f"Issue {issue_info['issue_id']}")
    st.markdown('<div class="box">', unsafe_allow_html=True)

    issue_info_ordered= OrderedDict()
    for key in issue_info_displayable.keys():
        issue_info_ordered[key] = issue_info[key]

    for key, value in issue_info_ordered.items():
        key_to_be_displayed = issue_info_displayable[key]

        if key == 'issue_date' and value is not None:
            value = format_date(value)

        st.markdown(
            f'<div class="field"><span class="key">{key_to_be_displayed}</span> <span class="value">{value}</span></div>',
            unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
