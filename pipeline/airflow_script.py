from airflow import DAG 
from airflow.operators.python import PythonOperator
import datetime as dt
import pandas as pd 
import mysql.connector as connector 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path

DATA_DIR = Path("/Users/ibrahim/Desktop/automotive-production/pipeline")
DATA_DIR.mkdir(parents=True, exist_ok=True)

def extract_data():

    connection = connector.connect(
    host = 'localhost',
    port = 3306, 
    user= 'root',
    password = 'projektiSQL2026!',
    database = 'automotive_production'
    )

    try:

        cursor = connection.cursor()

        tables = ['production', 'production_measurements', 'process_specifications']

        dataframes = {} #dictionary od pandas dataframes

        for table in tables:
            cursor.execute(f"SELECT * FROM {table}")
            table_columns = [line[0] for line in cursor.description]
            df = pd.DataFrame(cursor.fetchall(), columns = table_columns)
            df.to_csv(DATA_DIR / f"{table}.csv", index=False)

    finally:
        cursor.close()
        connection.close()

    

def transform_data():
    df_production = pd.read_csv(DATA_DIR / "production.csv")
    df_measurements = pd.read_csv(DATA_DIR / "production_measurements.csv")
    df_specifications = pd.read_csv(DATA_DIR / "process_specifications.csv")

    merged_table = df_production.merge(
        df_measurements, 
        on='igef',
        how='inner'
    )

    merged_table = merged_table.merge(
        df_specifications,
        on = 'specification_id',
        how = 'inner'
    )

    merged_table = merged_table.drop(columns = ['model_id_y', 'robot_number'])
    merged_table = merged_table.rename(columns = {'model_id_x':'model_id'})
    merged_table['abs_deviation_percent'] = (merged_table['deviation_percent'].abs())

    model_analysis = (
        merged_table.groupby(['model_id','ubs_line']).agg(
            vehicles=('igef','nunique'),
            measurements=('igef','size'),
            avg_abs_deviation=('abs_deviation_percent','mean'),
            inspection_count=('requires_inspection','sum')
        ).reset_index()
    ) 
    model_analysis['inspection_rate_percent']=(model_analysis['inspection_count']/model_analysis['measurements'] * 100)

    pivot = merged_table.pivot_table(
        index = 'model_id',
        columns = 'ubs_line',
        values = 'abs_deviation_percent',
        aggfunc='mean'
    )

    model_analysis.to_csv('/Users/ibrahim/Desktop/automotive-production/pipeline/model_analysis.csv', index = False)
    pivot.to_csv('/Users/ibrahim/Desktop/automotive-production/pipeline/model_line_pivot.csv')

    merged_table['production_datetime'] = pd.to_datetime(merged_table['production_datetime'])
    merged_table['hour'] = merged_table['production_datetime'].dt.hour

    hourly_production = (
        merged_table.groupby(['hour','ubs_line'])['igef'].nunique().unstack(fill_value=0).reindex(range(24),fill_value=0)
    )

    df_timeline = (
        merged_table[['igef','ubs_line','production_datetime']]
        .drop_duplicates(subset = ['igef'])
        .sort_values('production_datetime')
        .copy()
    )

    df_timeline['time_difference'] = (
        df_timeline.groupby('ubs_line')['production_datetime'].diff().dt.total_seconds() / 60
    )

    interruptions = df_timeline[df_timeline['time_difference'] > 2]

    hourly_production.rename_axis('hour').reset_index().to_csv(DATA_DIR / "hourly_production.csv", index = False)
    interruptions.to_csv(DATA_DIR / "interruptions.csv", index = False)

def visualize_data():
    hourly_production = pd.read_csv(DATA_DIR / "hourly_production.csv").set_index("hour")
    interruptions = pd.read_csv(DATA_DIR / "interruptions.csv")

    interruptions['production_datetime'] = pd.to_datetime(interruptions['production_datetime'])

    ax = hourly_production.plot(
        kind = 'bar',
        figsize = (12,5),
        width = 0.8
    )

    for container in ax.containers:
        ax.bar_label(container, fmt="%.0f", padding=3)

    plt.title('Hourly production line 1 and line 2')
    plt.xlabel('Hour of day')
    plt.ylabel('Vehicles produced')
    plt.xticks(range(24),rotation=0)
    plt.tight_layout()
    plt.savefig('ubs_line_hour.png')
    plt.close()

    hourly_total = hourly_production.sum(axis = 1)
    ax = hourly_total.plot(
        kind = 'bar',
        figsize = (12, 5),
        width = 0.8 
    )

    for container in ax.containers: 
        ax.bar_label(container, fmt="%.0f", padding=3)

    plt.title('Hourly production UBS - total')
    plt.xlabel('Hour of day')
    plt.ylabel('Vehicles produced')
    plt.xticks(range(24), rotation=0)
    plt.tight_layout()
    plt.savefig('ubs_total_hour.png')
    plt.close()

    shifts = [
    ("Nachtschicht", 0, 6),
    ("Frühschicht", 6, 15),
    ("Spätschicht",15,24)
    ]



    for shift, start_hour, end_hour in shifts:
        fig, axes = plt.subplots(2, 1, figsize=(14,5), sharex=True)

        shift_interruptions = interruptions[
            (interruptions['production_datetime'].dt.hour >= start_hour) & 
            (interruptions['production_datetime'].dt.hour < end_hour)
        ]

        for ax, line in zip(axes, [1,2]):
            line_data = shift_interruptions[shift_interruptions['ubs_line']==line]


            ax.scatter(
                line_data['production_datetime'],
                line_data['time_difference'],
                s=50,
                alpha=0.8, 
            )

            ax.axhline(
                y=2,
                color='red',
                linestyle='--',
                linewidth=1.3,
                label='2 minute delay'
            )

            ax.set_title(f"UBS-Linie {line}")
            ax.set_ylabel("Zeitabstand (Minuten)")
            ax.grid(axis='y', alpha=0.3)
            ax.legend()

        axes[1].set_xlabel('Produktionszeit')
        axes[1].xaxis.set_major_locator(mdates.HourLocator(interval=1))
        axes[1].xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

        fig.suptitle(f"Produktionsunterbrechungen: {shift}")
        fig.tight_layout()
        fig.savefig(f"interruption_{shift.lower()}.png")
        plt.close(fig)
    


default_args = {
    'owner':'me',
    'start_date': dt.datetime(2026, 10, 16),
    'retries':1,
    'retry_delay': dt.timedelta(minutes = 5)
}

dag = DAG(
    dag_id = 'automotive_production_pipeline',
    description = 'Pipeline for automotive production (Lack - UBS)',
    default_args = default_args,
    schedule_interval = dt.timedelta(days = 1)
)

extract = PythonOperator(
    task_id = 'extract_data',
    python_callable = extract_data, 
    dag = dag,
)

transform = PythonOperator(
    task_id = 'transform_data',
    python_callable = transform_data,
    dag = dag,
)

visualize = PythonOperator(
    task_id = 'visualize_data',
    python_callable = visualize_data,
    dag = dag, 
)


extract >> transform >> visualize 



