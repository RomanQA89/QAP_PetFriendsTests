import os

from dotenv import load_dotenv

load_dotenv()

"""Валидные данные"""
valid_email = os.getenv('valid_email')
valid_password = os.getenv('valid_password')

"""Невалидные данные"""
unvalid_email = os.getenv('invalid_email')
unvalid_password = os.getenv('invalid_password')
unvalid_auth_key = {'key': '54fdcd2eb6981a423591c0d93dff6199678a4141fcc23c2a5d61c09d'}