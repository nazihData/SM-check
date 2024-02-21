import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import re


def main():
    st.set_page_config(page_title="Security Check Analysis")

    # Page Title
    st.markdown("<h1 style='text-align: center; font-size: 45px;'>Candidates Security Analysis</h1>", unsafe_allow_html=True)
    
    # File uploader for uploading data file
    uploaded_file = st.file_uploader("Upload Data File", type=['csv', 'xlsx'])

    if uploaded_file is not None:
        # Load data from the uploaded file
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            else:
                st.error("Unsupported file format. Please upload a CSV or Excel file.")
                return
        except Exception as e:
            st.error(f"Error occurred while loading the file: {str(e)}")
            return


    # security = pd.read_excel("C:/Users/Surface/Desktop/Security check analysis/Security Report.xlsx")
    security = df[df['Security date'] >= '2023-01-01 00:00:00']
    stat_sec = security.groupby(by=['TA Team'], as_index=False)['Security status\nAccepted / Not Accepted'].count()
    
    # Create bubble plot
    fig = px.scatter(stat_sec, x='TA Team', y='Security status\nAccepted / Not Accepted', title='Candidates count per TA team member', size='Security status\nAccepted / Not Accepted', text='Security status\nAccepted / Not Accepted', color='TA Team', width=1400, height=800)
    fig.update_traces(textfont_size=20, textfont_color='black')
    fig.update_layout(legend=dict(font=dict(size=20)), xaxis=dict(tickfont=dict(size=20,color='black')), yaxis=dict(tickfont=dict(size=20, color='black')))
    fig.update_layout(yaxis_title="<b>Candidates Count</b>", yaxis_title_font=dict(size=22, color='black'))
    fig.update_layout(xaxis_title="", xaxis_title_font=dict(size=22, color='black'))
    fig.for_each_trace(lambda t:t.update(textfont_color=t.marker.color, textposition='top center'))
    st.plotly_chart(fig)
    
    
    # status till accepted
    acc_sector = security.groupby(by=['Sector/Bank/Club/Company','Security status\nAccepted / Not Accepted'], as_index=False)['Name'].count()
    bargp_chart = px.bar(acc_sector, x='Sector/Bank/Club/Company', y='Name', color='Security status\nAccepted / Not Accepted', barmode='stack', width=1400, height=800, orientation='v', text_auto=True, log_y=True, title="Status for each Sector")
    bargp_chart.update_traces(textfont_size=20, textfont_color='white')
    bargp_chart.update_layout(legend=dict(font=dict(size=20)), xaxis=dict(tickfont=dict(size=20,color='black')), yaxis=dict(tickfont=dict(size=20, color='black')))
    bargp_chart.update_layout(xaxis_title="", xaxis_title_font=dict(size=22, color='black'), legend=dict(x=0.70, y=1.2, xanchor='center', yanchor='top'),legend_orientation='h')
    bargp_chart.update_layout(yaxis_title="<b>Candidates Count</b>", yaxis_title_font=dict(size=22, color='black'))
    st.plotly_chart(bargp_chart)
    
    # Duration
    security_accepted = security[security['Security status\nAccepted / Not Accepted'] == 'Accepted']
    sec_nona =security_accepted.dropna(subset=['Duration'])
    
    pos_box = px.box(sec_nona, x='Sector/Bank/Club/Company', y='Duration', title='Average Daily Working Hours per Position', color='Sector/Bank/Club/Company', template='plotly', width=1400, height=800)
    pos_box.update_layout(legend=dict(font=dict(size=20)), xaxis=dict(tickfont=dict(size=20,color='black')), yaxis=dict(tickfont=dict(size=20, color='black')))
    pos_box.update_layout(yaxis_title="<b>Days Count</b>", yaxis_title_font=dict(size=22, color='black'))
    pos_box.update_layout(xaxis_title="", xaxis_title_font=dict(size=22, color='black'))
    pos_box.update_layout(showlegend=False)
    st.plotly_chart(pos_box)

    
    


    

if __name__ == "__main__":
    main()
