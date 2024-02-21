import pandas as pd
import streamlit as st
import plotly.express as px

def load_data(uploaded_file):
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file format. Please upload a CSV or Excel file.")
            return None
    except Exception as e:
        st.error(f"Error occurred while loading the file: {str(e)}")
        return None
    return df

def filter_security_data(df):
    return df[df['Security date'] >= '2023-01-01 00:00:00']

def create_bubble_plot(stat_sec):
    fig = px.scatter(
        stat_sec,
        x='TA Team',
        y='Security status\nAccepted / Not Accepted',
        title='Candidates count per TA team member',
        size='Security status\nAccepted / Not Accepted',
        text='Security status\nAccepted / Not Accepted',
        color='TA Team',
        width=1400,
        height=800
    )
    fig.update_traces(textfont_size=20, textfont_color='black')
    fig.update_layout(
        legend=dict(font=dict(size=20)),
        xaxis=dict(tickfont=dict(size=20, color='black')),
        yaxis=dict(tickfont=dict(size=20, color='black')),
        yaxis_title="<b>Candidates Count</b>",
        yaxis_title_font=dict(size=22, color='black'),
        xaxis_title="",
        xaxis_title_font=dict(size=22, color='black')
    )
    fig.for_each_trace(lambda t: t.update(textfont_color=t.marker.color, textposition='top center'))
    return fig

def create_status_bar_chart(acc_sector):
    bargp_chart = px.bar(
        acc_sector,
        x='Sector/Bank/Club/Company',
        y='Name',
        color='Security status\nAccepted / Not Accepted',
        barmode='stack',
        width=1400,
        height=800,
        orientation='v',
        text_auto=True,
        log_y=True,
        title="Status for each Sector"
    )
    bargp_chart.update_traces(textfont_size=20, textfont_color='white')
    bargp_chart.update_layout(
        xaxis=dict(tickfont=dict(size=20, color='black')),
        yaxis=dict(tickfont=dict(size=20, color='black')),
        xaxis_title="",
        xaxis_title_font=dict(size=22, color='black'),
        legend=dict(x=0.70, y=1.2, xanchor='center', yanchor='top'),
        legend_orientation='h',
        yaxis_title="<b>Candidates Count</b>",
        yaxis_title_font=dict(size=22, color='black')
    )
    return bargp_chart

def create_duration_box_plot(sec_nona):
    pos_box = px.box(
        sec_nona,
        x='Sector/Bank/Club/Company',
        y='Duration',
        title='Average Daily Working Hours per Position',
        color='Sector/Bank/Club/Company',
        template='plotly',
        width=1400,
        height=800
    )
    pos_box.update_layout(
        xaxis=dict(tickfont=dict(size=20, color='black')),
        yaxis=dict(tickfont=dict(size=20, color='black')),
        yaxis_title="<b>Days Count</b>",
        yaxis_title_font=dict(size=22, color='black'),
        xaxis_title="",
        xaxis_title_font=dict(size=22, color='black'),
        showlegend=False
    )
    return pos_box

def main():
    st.set_page_config(page_title="Security Check Analysis")
    st.markdown("<h1 style='text-align: center; font-size: 45px;'>Candidates Security Analysis</h1>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload Data File", type=['csv', 'xlsx'])

    if uploaded_file is not None:
        df = load_data(uploaded_file)
        if df is not None:
            security = filter_security_data(df)
            stat_sec = security.groupby(by=['TA Team'], as_index=False)['Security status\nAccepted / Not Accepted'].count()
            acc_sector = security.groupby(by=['Sector/Bank/Club/Company','Security status\nAccepted / Not Accepted'], as_index=False)['Name'].count()
            security_accepted = security[security['Security status\nAccepted / Not Accepted'] == 'Accepted']
            sec_nona = security_accepted.dropna(subset=['Duration'])

            # Create and display plots
            st.plotly_chart(create_bubble_plot(stat_sec))
            st.plotly_chart(create_status_bar_chart(acc_sector))
            st.plotly_chart(create_duration_box_plot(sec_nona))

if __name__ == "__main__":
    main()
