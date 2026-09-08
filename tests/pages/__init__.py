"""
Package init for pages module.
"""
from .base_page import BasePage
from .login_page import LoginPage
from .dashboard_page import DashboardPage
from .pim_page import PIMPage

__all__ = ["BasePage", "LoginPage", "DashboardPage", "PIMPage"]
