"""Shared dashboard data, controls, and visual styling — EcoNexus AI."""

from pathlib import Path
import pandas as pd
import streamlit as st
import yaml
from src.data_loader import load_data
from ui.styles import inject_styles
from ui.layout import global_filters as _global_filters, get_data, get_config, page_chrome
from ui.cards import section_header
from ui.charts import show

inject_styles()


def filtered_data():
    """Legacy-compatible filter function wrapping the new design system."""
    return _global_filters()


def hero(title, subtitle):
    """Legacy hero — delegates to page_chrome."""
    page_chrome(title, subtitle)


def trend(data, columns, title):
    """Legacy trend chart — uses new chart system."""
    from ui.charts import trend_line
    fig = trend_line(data, x="timestamp", y=columns, title=title)
    show(fig)
