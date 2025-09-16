import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.chart import BarChart, Reference, LineChart, ScatterChart, Series
from openpyxl.chart.marker import Marker
from scipy import stats

# Create output directory if it doesn't exist
os.makedirs('../analysis', exist_ok=True)
os.makedirs('../reports', exist_ok=True)

# Load the data
baseline_df = pd.read_csv('../data/baseline_data.csv')
post_df = pd.read_csv('../data/post_intervention_data.csv')

# Merge the datasets
merged_df = pd.merge(baseline_df, post_df, on=['Zone', 'Area', 'Area_ID', 'Population'])

# Calculate key metrics
merged_df['Response_Time_Reduction'] = merged_df['Baseline_Response_Time_Minutes'] - merged_df['Post_Response_Time_Minutes']
merged_df['Response_Time_Reduction_Percent'] = (merged_df['Response_Time_Reduction'] / merged_df['Baseline_Response_Time_Minutes']) * 100
merged_df['Preparedness_Score_Improvement'] = merged_df['Post_Preparedness_Score'] - merged_df['Baseline_Preparedness_Score']
merged_df['Preparedness_Score_Improvement_Percent'] = (merged_df['Preparedness_Score_Improvement'] / merged_df['Baseline_Preparedness_Score']) * 100
merged_df['Participation_Rate'] = (merged_df['Participants'] / merged_df['Population']) * 100

# Calculate zone-level and overall statistics
zone_stats = merged_df.groupby('Zone').agg({
    'Response_Time_Reduction_Percent': 'mean',
    'Preparedness_Score_Improvement_Percent': 'mean',
    'Participation_Rate': 'mean',
    'Population': 'sum',
    'Participants': 'sum'
}).reset_index()

overall_stats = {
    'Response_Time_Reduction_Percent': merged_df['Response_Time_Reduction_Percent'].mean(),
    'Preparedness_Score_Improvement_Percent': merged_df['Preparedness_Score_Improvement_Percent'].mean(),
    'Participation_Rate': (merged_df['Participants'].sum() / merged_df['Population'].sum()) * 100,
    'Total_Population': merged_df['Population'].sum(),
    'Total_Participants': merged_df['Participants'].sum(),
    'Total_Areas': len(merged_df),
    'Total_Drills': merged_df['Drills_Conducted'].sum()
}

# Statistical analysis
# Calculate standard deviation, confidence intervals, etc.
merged_df['Response_Time_SD'] = merged_df.groupby('Zone')['Response_Time_Reduction_Percent'].transform('std')
merged_df['Preparedness_Score_SD'] = merged_df.groupby('Zone')['Preparedness_Score_Improvement_Percent'].transform('std')

# T-test for significance of response time reduction
t_stat_response, p_val_response = stats.ttest_rel(merged_df['Baseline_Response_Time_Minutes'], 
                                                 merged_df['Post_Response_Time_Minutes'])

# T-test for significance of preparedness score improvement
t_stat_prep, p_val_prep = stats.ttest_rel(merged_df['Baseline_Preparedness_Score'], 
                                         merged_df['Post_Preparedness_Score'])

# Correlation analysis
correlation_matrix = merged_df[['Population', 'Response_Time_Reduction_Percent', 
                               'Preparedness_Score_Improvement_Percent', 
                               'Participation_Rate', 'Drills_Conducted']].corr()

# Create Excel workbook with analysis
wb = Workbook()

# Style definitions
header_font = Font(bold=True, size=12)
header_fill = PatternFill(start_color="DDEBF7", end_color="DDEBF7", fill_type="solid")
border = Border(left=Side(style='thin'), right=Side(style='thin'), 
                top=Side(style='thin'), bottom=Side(style='thin'))

# Raw Data Sheet
ws_raw = wb.active
ws_raw.title = "Raw Data"

# Add headers
headers = ['Zone', 'Area', 'Area_ID', 'Population', 
           'Baseline_Response_Time', 'Post_Response_Time', 'Response_Time_Reduction', 'Response_Time_Reduction_%',
           'Baseline_Preparedness', 'Post_Preparedness', 'Preparedness_Improvement', 'Preparedness_Improvement_%',
           'Drills_Conducted', 'Participants', 'Participation_Rate_%']

for col_num, header in enumerate(headers, 1):
    cell = ws_raw.cell(row=1, column=col_num, value=header)
    cell.font = header_font
    cell.fill = header_fill
    cell.border = border
    cell.alignment = Alignment(horizontal='center', vertical='center')

# Add data
for row_num, row_data in enumerate(merged_df.itertuples(), 2):
    ws_raw.cell(row=row_num, column=1, value=row_data.Zone)
    ws_raw.cell(row=row_num, column=2, value=row_data.Area)
    ws_raw.cell(row=row_num, column=3, value=row_data.Area_ID)
    ws_raw.cell(row=row_num, column=4, value=row_data.Population)
    ws_raw.cell(row=row_num, column=5, value=row_data.Baseline_Response_Time_Minutes)
    ws_raw.cell(row=row_num, column=6, value=row_data.Post_Response_Time_Minutes)
    ws_raw.cell(row=row_num, column=7, value=row_data.Response_Time_Reduction)
    ws_raw.cell(row=row_num, column=8, value=round(row_data.Response_Time_Reduction_Percent, 2))
    ws_raw.cell(row=row_num, column=9, value=row_data.Baseline_Preparedness_Score)
    ws_raw.cell(row=row_num, column=10, value=row_data.Post_Preparedness_Score)
    ws_raw.cell(row=row_num, column=11, value=row_data.Preparedness_Score_Improvement)
    ws_raw.cell(row=row_num, column=12, value=round(row_data.Preparedness_Score_Improvement_Percent, 2))
    ws_raw.cell(row=row_num, column=13, value=row_data.Drills_Conducted)
    ws_raw.cell(row=row_num, column=14, value=row_data.Participants)
    ws_raw.cell(row=row_num, column=15, value=round(row_data.Participation_Rate, 2))

# Set fixed column widths instead of dynamic calculation to avoid MergedCell error
column_widths = {
    'A': 15,  # Zone
    'B': 15,  # Area
    'C': 10,  # Area_ID
    'D': 12,  # Population
    'E': 20,  # Baseline_Response_Time
    'F': 20,  # Post_Response_Time
    'G': 20,  # Response_Time_Reduction
    'H': 22,  # Response_Time_Reduction_%
    'I': 20,  # Baseline_Preparedness
    'J': 20,  # Post_Preparedness
    'K': 22,  # Preparedness_Improvement
    'L': 25,  # Preparedness_Improvement_%
    'M': 18,  # Drills_Conducted
    'N': 15,  # Participants
    'O': 20,  # Participation_Rate_%
}

for col_letter, width in column_widths.items():
    ws_raw.column_dimensions[col_letter].width = width

# Summary Statistics Sheet
ws_summary = wb.create_sheet(title="Summary Statistics")

# Add headers
summary_headers = ['Metric', 'Overall', 'Thane East Zone', 'Thane West Zone']
for col_num, header in enumerate(summary_headers, 1):
    cell = ws_summary.cell(row=1, column=col_num, value=header)
    cell.font = header_font
    cell.fill = header_fill
    cell.border = border
    cell.alignment = Alignment(horizontal='center', vertical='center')

# Add summary data
metrics = [
    'Average Response Time Reduction (%)',
    'Average Preparedness Score Improvement (%)',
    'Average Participation Rate (%)',
    'Total Population Covered',
    'Total Participants',
    'Number of Areas',
    'Number of Drills Conducted'
]

# Get zone values
thane_east_stats = zone_stats[zone_stats['Zone'] == 'Thane East'].iloc[0]
thane_west_stats = zone_stats[zone_stats['Zone'] == 'Thane West'].iloc[0]

for row_num, metric in enumerate(metrics, 2):
    ws_summary.cell(row=row_num, column=1, value=metric)
    
    if metric == 'Average Response Time Reduction (%)':
        ws_summary.cell(row=row_num, column=2, value=round(overall_stats['Response_Time_Reduction_Percent'], 2))
        ws_summary.cell(row=row_num, column=3, value=round(thane_east_stats['Response_Time_Reduction_Percent'], 2))
        ws_summary.cell(row=row_num, column=4, value=round(thane_west_stats['Response_Time_Reduction_Percent'], 2))
    elif metric == 'Average Preparedness Score Improvement (%)':
        ws_summary.cell(row=row_num, column=2, value=round(overall_stats['Preparedness_Score_Improvement_Percent'], 2))
        ws_summary.cell(row=row_num, column=3, value=round(thane_east_stats['Preparedness_Score_Improvement_Percent'], 2))
        ws_summary.cell(row=row_num, column=4, value=round(thane_west_stats['Preparedness_Score_Improvement_Percent'], 2))
    elif metric == 'Average Participation Rate (%)':
        ws_summary.cell(row=row_num, column=2, value=round(overall_stats['Participation_Rate'], 2))
        ws_summary.cell(row=row_num, column=3, value=round(thane_east_stats['Participation_Rate'], 2))
        ws_summary.cell(row=row_num, column=4, value=round(thane_west_stats['Participation_Rate'], 2))
    elif metric == 'Total Population Covered':
        ws_summary.cell(row=row_num, column=2, value=overall_stats['Total_Population'])
        ws_summary.cell(row=row_num, column=3, value=int(thane_east_stats['Population']))
        ws_summary.cell(row=row_num, column=4, value=int(thane_west_stats['Population']))
    elif metric == 'Total Participants':
        ws_summary.cell(row=row_num, column=2, value=overall_stats['Total_Participants'])
        ws_summary.cell(row=row_num, column=3, value=int(thane_east_stats['Participants']))
        ws_summary.cell(row=row_num, column=4, value=int(thane_west_stats['Participants']))
    elif metric == 'Number of Areas':
        ws_summary.cell(row=row_num, column=2, value=overall_stats['Total_Areas'])
        ws_summary.cell(row=row_num, column=3, value=len(merged_df[merged_df['Zone'] == 'Thane East']))
        ws_summary.cell(row=row_num, column=4, value=len(merged_df[merged_df['Zone'] == 'Thane West']))
    elif metric == 'Number of Drills Conducted':
        ws_summary.cell(row=row_num, column=2, value=overall_stats['Total_Drills'])
        ws_summary.cell(row=row_num, column=3, value=merged_df[merged_df['Zone'] == 'Thane East']['Drills_Conducted'].sum())
        ws_summary.cell(row=row_num, column=4, value=merged_df[merged_df['Zone'] == 'Thane West']['Drills_Conducted'].sum())

# Set fixed column widths for summary sheet
summary_widths = {
    'A': 35,  # Metric
    'B': 15,  # Overall
    'C': 18,  # Thane East Zone
    'D': 18,  # Thane West Zone
}

for col_letter, width in summary_widths.items():
    ws_summary.column_dimensions[col_letter].width = width

# Statistical Analysis Sheet
ws_stats = wb.create_sheet(title="Statistical Analysis")

# Add headers
ws_stats.cell(row=1, column=1, value="Statistical Test Results").font = header_font
ws_stats.merge_cells('A1:D1')
ws_stats.cell(row=1, column=1).alignment = Alignment(horizontal='center')

# Add t-test results
ws_stats.cell(row=3, column=1, value="T-Test for Response Time Reduction:").font = Font(bold=True)
ws_stats.cell(row=4, column=1, value="t-statistic:")
ws_stats.cell(row=4, column=2, value=round(t_stat_response, 4))
ws_stats.cell(row=5, column=1, value="p-value:")
ws_stats.cell(row=5, column=2, value=round(p_val_response, 6))
ws_stats.cell(row=6, column=1, value="Significance:")
ws_stats.cell(row=6, column=2, value="Statistically Significant" if p_val_response < 0.05 else "Not Significant")

ws_stats.cell(row=8, column=1, value="T-Test for Preparedness Score Improvement:").font = Font(bold=True)
ws_stats.cell(row=9, column=1, value="t-statistic:")
ws_stats.cell(row=9, column=2, value=round(t_stat_prep, 4))
ws_stats.cell(row=10, column=1, value="p-value:")
ws_stats.cell(row=10, column=2, value=round(p_val_prep, 6))
ws_stats.cell(row=11, column=1, value="Significance:")
ws_stats.cell(row=11, column=2, value="Statistically Significant" if p_val_prep < 0.05 else "Not Significant")

# Add correlation matrix
ws_stats.cell(row=13, column=1, value="Correlation Matrix:").font = Font(bold=True)
ws_stats.merge_cells('A13:E13')
ws_stats.cell(row=13, column=1).alignment = Alignment(horizontal='center')

corr_headers = ['Variable', 'Population', 'Response Time Reduction %', 'Preparedness Improvement %', 'Participation Rate %', 'Drills Conducted']
for col_num, header in enumerate(corr_headers, 1):
    cell = ws_stats.cell(row=14, column=col_num, value=header)
    cell.font = Font(bold=True)
    cell.fill = header_fill

corr_rows = ['Population', 'Response Time Reduction %', 'Preparedness Improvement %', 'Participation Rate %', 'Drills Conducted']
for row_num, row_name in enumerate(corr_rows, 15):
    ws_stats.cell(row=row_num, column=1, value=row_name).font = Font(bold=True)
    for col_num, col_name in enumerate(corr_rows, 2):
        i = corr_rows.index(row_name)
        j = corr_rows.index(col_name)
        ws_stats.cell(row=row_num, column=col_num, value=round(correlation_matrix.iloc[i, j], 3))

# Add statistical formulas explanation
ws_stats.cell(row=22, column=1, value="Statistical Methods and Formulas:").font = Font(bold=True)
ws_stats.merge_cells('A22:E22')
ws_stats.cell(row=22, column=1).alignment = Alignment(horizontal='center')

formulas = [
    "1. Percentage Change Formula: ((Final Value - Initial Value) / Initial Value) × 100",
    "2. Response Time Reduction %: ((Baseline Response Time - Post Response Time) / Baseline Response Time) × 100",
    "3. Preparedness Score Improvement %: ((Post Preparedness Score - Baseline Preparedness Score) / Baseline Preparedness Score) × 100",
    "4. Participation Rate %: (Number of Participants / Total Population) × 100",
    "5. T-test for Paired Samples: t = (mean of differences) / (standard error of differences)",
    "6. Standard Error: SE = s / √n, where s is the sample standard deviation and n is the sample size",
    "7. Pearson Correlation Coefficient: r = Σ((X - μX)(Y - μY)) / (σX σY)",
    "8. Confidence Interval (95%): mean ± (1.96 × standard error)"
]

for i, formula in enumerate(formulas, 23):
    ws_stats.cell(row=i, column=1, value=formula)
    ws_stats.merge_cells(f'A{i}:E{i}')

# Set fixed column widths for stats sheet
stats_widths = {
    'A': 40,
    'B': 20,
    'C': 20,
    'D': 20,
    'E': 20,
}

for col_letter, width in stats_widths.items():
    ws_stats.column_dimensions[col_letter].width = width

# Charts Sheet
ws_charts = wb.create_sheet(title="Charts")

# Add data for charts
chart_data_start_row = 2
ws_charts.cell(row=1, column=1, value="Zone")
ws_charts.cell(row=1, column=2, value="Response Time Reduction %")
ws_charts.cell(row=1, column=3, value="Preparedness Score Improvement %")

for i, zone in enumerate(zone_stats['Zone'], chart_data_start_row):
    ws_charts.cell(row=i, column=1, value=zone)
    ws_charts.cell(row=i, column=2, value=round(zone_stats.loc[zone_stats['Zone'] == zone, 'Response_Time_Reduction_Percent'].values[0], 2))
    ws_charts.cell(row=i, column=3, value=round(zone_stats.loc[zone_stats['Zone'] == zone, 'Preparedness_Score_Improvement_Percent'].values[0], 2))

ws_charts.cell(row=4, column=1, value="Overall")
ws_charts.cell(row=4, column=2, value=round(overall_stats['Response_Time_Reduction_Percent'], 2))
ws_charts.cell(row=4, column=3, value=round(overall_stats['Preparedness_Score_Improvement_Percent'], 2))

# Create bar chart for response time reduction
chart1 = BarChart()
chart1.title = "Response Time Reduction by Zone (%)"
chart1.style = 10
chart1.x_axis.title = "Zone"
chart1.y_axis.title = "Reduction Percentage"

data = Reference(ws_charts, min_col=2, min_row=1, max_row=4, max_col=2)
cats = Reference(ws_charts, min_col=1, min_row=2, max_row=4)
chart1.add_data(data, titles_from_data=True)
chart1.set_categories(cats)
chart1.shape = 4
ws_charts.add_chart(chart1, "A6")

# Create bar chart for preparedness score improvement
chart2 = BarChart()
chart2.title = "Preparedness Score Improvement by Zone (%)"
chart2.style = 10
chart2.x_axis.title = "Zone"
chart2.y_axis.title = "Improvement Percentage"

data = Reference(ws_charts, min_col=3, min_row=1, max_row=4, max_col=3)
cats = Reference(ws_charts, min_col=1, min_row=2, max_row=4)
chart2.add_data(data, titles_from_data=True)
chart2.set_categories(cats)
chart2.shape = 4
ws_charts.add_chart(chart2, "A21")

# Add area-level data for scatter plot
ws_charts.cell(row=1, column=5, value="Area")
ws_charts.cell(row=1, column=6, value="Drills Conducted")
ws_charts.cell(row=1, column=7, value="Response Time Reduction %")

for i, row in enumerate(merged_df.itertuples(), chart_data_start_row):
    ws_charts.cell(row=i, column=5, value=row.
(Content truncated due to size limit. Use line ranges to read in chunks)