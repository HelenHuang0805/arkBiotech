from flask import Blueprint, render_template
import plotly.express as px
import pandas as pd
import psycopg2
from psycopg2 import extras
from .config import Config

dashboard_blueprint = Blueprint("dashboard", __name__, template_folder="templates")

def get_data():
    conn = psycopg2.connect(
        dbname=Config.POSTGRES_DB,
        user=Config.POSTGRES_USER,
        password=Config.POSTGRES_PASSWORD,
        host=Config.POSTGRES_HOST,
        port=Config.POSTGRES_PORT
    )
    cur = conn.cursor(cursor_factory=extras.DictCursor)

    query = "SELECT * FROM public.\"CM_HAM_DO_AI1/Temp_value\""
    cur.execute(query)
    temperature_data = cur.fetchall()

    query = "SELECT * FROM public.\"CM_HAM_PH_AI1/pH_value\""
    cur.execute(query)
    ph_data = cur.fetchall()

    query = "SELECT * FROM public.\"CM_PID_DO/Process_DO\""
    cur.execute(query)
    do_data = cur.fetchall()

    query = "SELECT * FROM public.\"CM_PRESSURE/Output\""
    cur.execute(query)
    pressure_data = cur.fetchall()

    conn.close()
    return temperature_data, ph_data, do_data, pressure_data

def create_plot(data, title, x_label, y_label):
    df = pd.DataFrame(data, columns=["time", "value"])
    fig = px.line(df, x="time", y="value", title=title)
    fig.update_xaxes(title_text=x_label)
    fig.update_yaxes(title_text=y_label)
    return fig.to_html(full_html=False, include_plotlyjs="cdn")

@dashboard_blueprint.route("/")
def index():
    temperature_data, ph_data, do_data, pressure_data = get_data()
    
    temperature_plot = create_plot(temperature_data, "Temperature vs Time", "Time", "Temperature (Celsius)")
    ph_plot = create_plot(ph_data, "pH vs Time", "Time", "pH")
    do_plot = create_plot(do_data, "Distilled Oxygen vs Time", "Time", "Distilled Oxygen (%)")
    pressure_plot = create_plot(pressure_data, "Pressure vs Time", "Time", "Pressure (psi)")

    return render_template("index.html", temperature_plot=temperature_plot, ph_plot=ph_plot, do_plot=do_plot, pressure_plot=pressure_plot)
