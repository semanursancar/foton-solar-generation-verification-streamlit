import streamlit as st
import pandas as pd
import altair as alt
import plotly.graph_objects as go


from functions import MonthlyAverageSolarGeneration

st.set_page_config(layout="wide")

def main():
    st.markdown("""
    <style>
    /* CSS style to center-align the title */
    .title {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 class='title'>Coordinate Based Monthly Solar Generation</h1>", unsafe_allow_html=True)

    lat = st.number_input('Latitude:', min_value=0.0, max_value=90.0, value=37.019148, step=0.0001)
    lon = st.number_input('Longitude:', min_value=0.0, max_value=180.0, value=36.116237, step=0.0001)
    peak_power = st.number_input('Installed Power [kW]:', min_value=1.0, value=1000.0, step=1.0)

    if st.button('Get Average Generation'):
        try:           
            table, user_note = MonthlyAverageSolarGeneration(lat, lon, peak_power)
            
            # Custom CSS to center-align table headers
            custom_css = """
            <style>
            th {
                text-align: center;
            }
            table {
                border-collapse: separate;
                border-spacing: 0;
                border-radius: 10px;
                overflow: hidden;
            }
            td, th {
                border: 1px solid #dddddd;
                padding: 8px;
            }
            </style>
            """
            st.write(custom_css, unsafe_allow_html=True)

            # Split the screen into two columns for table and chart
            col1, col2 = st.columns(2)

            # Render the table using HTML and CSS in the first column
            with col1:
                st.subheader('Solar Generation Data')
                st.write(table.to_html(index=False, escape=False), unsafe_allow_html=True)
                st.write(user_note)

            # Create the line chart using Streamlit's st.line_chart function in the second column
            with col2:
                st.subheader('Solar Generation Chart')
                # Create the combined bar chart using Plotly
                fig = go.Figure()

                fig.add_trace(
                    go.Bar(x=table['Months'], y=table['Average Generation [kWh]'], name='Average Generation [kWh]'),
                )

                fig.add_trace(
                    go.Scatter(x=table['Months'], y=table['Max. Generation Capacity [kWh]'], name='Max. Generation Capacity [kWh]', mode='markers', marker=dict(color='red')),
                )

                y_max = max(table['Max. Generation Capacity [kWh]'])  # Find the maximum value in the table
                y_axis_margin = y_max * 0.1  # Add a 10% margin to the y-axis

                fig.update_layout(
                    xaxis_title='Months',
                    yaxis=dict(title='Solar Generation [kWh]', range=[0, y_max + y_axis_margin]),
                    legend=dict(orientation='h', x=0, y=-0.2),  # Move legend to the bottom with horizontal orientation
                    height=570,
                    xaxis=dict(tickmode='linear', dtick=1)
                )

                st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    # Footer
    st.markdown("""
    <style>
    /* CSS style for the footer */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f0f0f0;
        color: #333;
        text-align: center;
        padding: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="footer">Made with 💚 by FOTON     |     Version: 0.0.6</div>', unsafe_allow_html=True)


if __name__ == '__main__':
    main()