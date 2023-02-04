import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import datetime
import requests

st.set_page_config(  # Alternate names: setup_page, page, layout
	layout="centered",  # Can be "centered" or "wide". In the future also "dashboard", etc.
	initial_sidebar_state="expanded",  # Can be "auto", "expanded", "collapsed"
	page_title="COMO: Finanční vizualizace",  # String or None. Strings get appended with "• Streamlit". 
	page_icon=None,  # String, anything supported by st.image, or None.
)

gross_amount = st.number_input("Vložte vaší měsíční hrubou mzdu (uvedená na smlouvě)")
number_of_child = st.number_input("Kolik máte dětí")
invalidity_first_level = st.checkbox("Invalidita 1. nebo 2. stupně")
invalidity_third_level = st.checkbox("Invalidita 3. stupně")
ztp_hold = st.checkbox("Jste držitelem ZTP/P")
student = st.checkbox("Jste student?")

discount_payee = 30840
discount_husband = 24840
discount_husband_ztp = 49680
discount_first_second_invalidity = 2520
disocunt_third_invalidity = 5040
discount_ztp_holder = 16140
discount_student = 4020
tax_discount_first_child = 15204
tax_discount_second_child = 22320
tax_discount_third_after_child = 27840
tax_discount_child_ztp = 30408
tax_discount_second_child_ztp = 44640
tax_discount_thir_child_ztp = 55680
discount_placing_child = 16200
discount_EET = 5000