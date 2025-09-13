import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import numpy as np
from typing import Dict, List, Any, Optional
import json

class PatientTimelineVisualization:
    """Comprehensive patient timeline visualization system for nephrology data"""
    
    def __init__(self):
        self.color_palette = {
            'creatinine': '#e74c3c',
            'gfr': '#3498db',
            'bun': '#f39c12',
            'albumin': '#27ae60',
            'hemoglobin': '#9b59b6',
            'phosphorus': '#e67e22',
            'potassium': '#34495e',
            'calcium': '#16a085',
            'medications': '#8e44ad',
            'procedures': '#2c3e50',
            'hospitalizations': '#c0392b',
            'dialysis': '#d35400'
        }
        
    def create_comprehensive_timeline(self, patient_data: Dict[str, Any]) -> go.Figure:
        """Create a comprehensive timeline visualization"""
        try:
            # Create subplots with secondary y-axis
            fig = make_subplots(
                rows=4, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.08,
                subplot_titles=(
                    'Key Laboratory Values Over Time',
                    'Kidney Function Trends',
                    'Clinical Events & Interventions',
                    'Risk Scores & Predictions'
                ),
                specs=[
                    [{"secondary_y": True}],
                    [{"secondary_y": True}],
                    [{"secondary_y": False}],
                    [{"secondary_y": True}]
                ]
            )
            
            # Extract lab data
            lab_data = patient_data.get('lab_results', [])
            if lab_data:
                lab_df = pd.DataFrame(lab_data)
                lab_df['date'] = pd.to_datetime(lab_df['date'])
                
                # Plot 1: Key Laboratory Values
                for param in ['creatinine', 'bun', 'albumin', 'hemoglobin']:
                    param_data = lab_df[lab_df['parameter'].str.lower() == param]
                    if not param_data.empty:
                        fig.add_trace(
                            go.Scatter(
                                x=param_data['date'],
                                y=param_data['value'],
                                mode='lines+markers',
                                name=param.title(),
                                line=dict(color=self.color_palette.get(param, '#7f8c8d'), width=2),
                                marker=dict(size=6),
                                hovertemplate=f'<b>{param.title()}</b><br>' +
                                            'Date: %{x}<br>' +
                                            'Value: %{y}<br>' +
                                            '<extra></extra>'
                            ),
                            row=1, col=1
                        )
                
                # Plot 2: Kidney Function (GFR and Creatinine)
                gfr_data = lab_df[lab_df['parameter'].str.lower() == 'gfr']
                creat_data = lab_df[lab_df['parameter'].str.lower() == 'creatinine']
                
                if not gfr_data.empty:
                    fig.add_trace(
                        go.Scatter(
                            x=gfr_data['date'],
                            y=gfr_data['value'],
                            mode='lines+markers',
                            name='GFR',
                            line=dict(color=self.color_palette['gfr'], width=3),
                            marker=dict(size=8),
                            yaxis='y3'
                        ),
                        row=2, col=1
                    )
                
                if not creat_data.empty:
                    fig.add_trace(
                        go.Scatter(
                            x=creat_data['date'],
                            y=creat_data['value'],
                            mode='lines+markers',
                            name='Creatinine',
                            line=dict(color=self.color_palette['creatinine'], width=3),
                            marker=dict(size=8),
                            yaxis='y4'
                        ),
                        row=2, col=1
                    )
            
            # Plot 3: Clinical Events
            events_data = patient_data.get('clinical_events', [])
            if events_data:
                events_df = pd.DataFrame(events_data)
                events_df['date'] = pd.to_datetime(events_df['date'])
                
                # Create event timeline
                event_types = events_df['event_type'].unique()
                for i, event_type in enumerate(event_types):
                    event_subset = events_df[events_df['event_type'] == event_type]
                    fig.add_trace(
                        go.Scatter(
                            x=event_subset['date'],
                            y=[i] * len(event_subset),
                            mode='markers',
                            name=event_type.title(),
                            marker=dict(
                                size=12,
                                color=self.color_palette.get(event_type.lower(), '#95a5a6'),
                                symbol='diamond'
                            ),
                            text=event_subset['description'],
                            hovertemplate='<b>%{fullData.name}</b><br>' +
                                        'Date: %{x}<br>' +
                                        'Description: %{text}<br>' +
                                        '<extra></extra>'
                        ),
                        row=3, col=1
                    )
            
            # Plot 4: Risk Scores and Predictions
            risk_data = patient_data.get('risk_assessments', [])
            if risk_data:
                risk_df = pd.DataFrame(risk_data)
                risk_df['date'] = pd.to_datetime(risk_df['date'])
                
                # Plot different risk scores
                for risk_type in ['dialysis_risk', 'mortality_risk', 'progression_risk']:
                    if risk_type in risk_df.columns:
                        fig.add_trace(
                            go.Scatter(
                                x=risk_df['date'],
                                y=risk_df[risk_type] * 100,  # Convert to percentage
                                mode='lines+markers',
                                name=risk_type.replace('_', ' ').title(),
                                line=dict(width=2),
                                marker=dict(size=6)
                            ),
                            row=4, col=1
                        )
            
            # Update layout
            fig.update_layout(
                height=1000,
                title={
                    'text': f"Comprehensive Patient Timeline - {patient_data.get('patient_id', 'Unknown')}",
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 20, 'color': '#2c3e50'}
                },
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                template='plotly_white'
            )
            
            # Update y-axes labels
            fig.update_yaxes(title_text="Lab Values", row=1, col=1)
            fig.update_yaxes(title_text="GFR (mL/min/1.73m²)", row=2, col=1)
            fig.update_yaxes(title_text="Creatinine (mg/dL)", secondary_y=True, row=2, col=1)
            fig.update_yaxes(title_text="Event Type", row=3, col=1)
            fig.update_yaxes(title_text="Risk Score (%)", row=4, col=1)
            
            # Update x-axes
            fig.update_xaxes(title_text="Date", row=4, col=1)
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating timeline: {str(e)}")
            return go.Figure()
    
    def create_lab_trends_chart(self, lab_data: List[Dict[str, Any]], 
                               parameters: List[str] = None) -> go.Figure:
        """Create detailed lab trends visualization"""
        try:
            if not lab_data:
                return go.Figure().add_annotation(
                    text="No lab data available",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5, showarrow=False
                )
            
            df = pd.DataFrame(lab_data)
            df['date'] = pd.to_datetime(df['date'])
            
            if parameters is None:
                parameters = df['parameter'].unique()[:6]  # Limit to 6 parameters
            
            fig = go.Figure()
            
            for param in parameters:
                param_data = df[df['parameter'].str.lower() == param.lower()]
                if not param_data.empty:
                    # Add trend line
                    fig.add_trace(
                        go.Scatter(
                            x=param_data['date'],
                            y=param_data['value'],
                            mode='lines+markers',
                            name=param.title(),
                            line=dict(
                                color=self.color_palette.get(param.lower(), '#7f8c8d'),
                                width=2
                            ),
                            marker=dict(size=8),
                            hovertemplate=f'<b>{param.title()}</b><br>' +
                                        'Date: %{x}<br>' +
                                        'Value: %{y}<br>' +
                                        '<extra></extra>'
                        )
                    )
                    
                    # Add reference range if available
                    if 'reference_range' in param_data.columns:
                        ref_range = param_data['reference_range'].iloc[0]
                        if ref_range and '-' in str(ref_range):
                            try:
                                low, high = map(float, str(ref_range).split('-'))
                                fig.add_hline(
                                    y=low, line_dash="dash", line_color="gray",
                                    annotation_text=f"{param} Low Normal"
                                )
                                fig.add_hline(
                                    y=high, line_dash="dash", line_color="gray",
                                    annotation_text=f"{param} High Normal"
                                )
                            except ValueError:
                                pass
            
            fig.update_layout(
                title="Laboratory Values Trends",
                xaxis_title="Date",
                yaxis_title="Value",
                hovermode='x unified',
                template='plotly_white',
                height=500
            )
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating lab trends: {str(e)}")
            return go.Figure()
    
    def create_gfr_progression_chart(self, gfr_data: List[Dict[str, Any]]) -> go.Figure:
        """Create GFR progression visualization with CKD stages"""
        try:
            if not gfr_data:
                return go.Figure().add_annotation(
                    text="No GFR data available",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5, showarrow=False
                )
            
            df = pd.DataFrame(gfr_data)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            
            fig = go.Figure()
            
            # Add GFR trend line
            fig.add_trace(
                go.Scatter(
                    x=df['date'],
                    y=df['gfr'],
                    mode='lines+markers',
                    name='GFR',
                    line=dict(color='#3498db', width=3),
                    marker=dict(size=8, color='#3498db'),
                    hovertemplate='<b>GFR</b><br>' +
                                'Date: %{x}<br>' +
                                'GFR: %{y} mL/min/1.73m²<br>' +
                                '<extra></extra>'
                )
            )
            
            # Add CKD stage reference lines
            ckd_stages = [
                {'stage': 'Normal/High', 'range': (90, 150), 'color': '#27ae60'},
                {'stage': 'CKD Stage 1', 'range': (90, 150), 'color': '#f1c40f'},
                {'stage': 'CKD Stage 2', 'range': (60, 89), 'color': '#f39c12'},
                {'stage': 'CKD Stage 3a', 'range': (45, 59), 'color': '#e67e22'},
                {'stage': 'CKD Stage 3b', 'range': (30, 44), 'color': '#d35400'},
                {'stage': 'CKD Stage 4', 'range': (15, 29), 'color': '#c0392b'},
                {'stage': 'CKD Stage 5', 'range': (0, 14), 'color': '#8b0000'}
            ]
            
            for stage in ckd_stages:
                fig.add_hrect(
                    y0=stage['range'][0], y1=stage['range'][1],
                    fillcolor=stage['color'], opacity=0.1,
                    layer="below", line_width=0
                )
                
                # Add stage labels
                fig.add_annotation(
                    x=df['date'].iloc[-1],
                    y=(stage['range'][0] + stage['range'][1]) / 2,
                    text=stage['stage'],
                    showarrow=False,
                    xanchor="left",
                    font=dict(size=10, color=stage['color'])
                )
            
            # Calculate and add trend line
            if len(df) > 1:
                # Simple linear regression for trend
                x_numeric = (df['date'] - df['date'].min()).dt.days
                z = np.polyfit(x_numeric, df['gfr'], 1)
                trend_line = np.poly1d(z)
                
                fig.add_trace(
                    go.Scatter(
                        x=df['date'],
                        y=trend_line(x_numeric),
                        mode='lines',
                        name='Trend',
                        line=dict(color='red', width=2, dash='dash'),
                        hovertemplate='<b>Trend Line</b><br>' +
                                    'Date: %{x}<br>' +
                                    'Predicted GFR: %{y:.1f}<br>' +
                                    '<extra></extra>'
                    )
                )
                
                # Calculate slope (GFR decline rate)
                slope = z[0] * 365  # Convert to per year
                fig.add_annotation(
                    text=f"GFR Decline Rate: {slope:.1f} mL/min/1.73m²/year",
                    xref="paper", yref="paper",
                    x=0.02, y=0.98,
                    showarrow=False,
                    bgcolor="rgba(255,255,255,0.8)",
                    bordercolor="gray",
                    borderwidth=1
                )
            
            fig.update_layout(
                title="GFR Progression and CKD Staging",
                xaxis_title="Date",
                yaxis_title="GFR (mL/min/1.73m²)",
                template='plotly_white',
                height=500,
                yaxis=dict(range=[0, 120])
            )
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating GFR progression chart: {str(e)}")
            return go.Figure()
    
    def create_medication_timeline(self, medication_data: List[Dict[str, Any]]) -> go.Figure:
        """Create medication timeline visualization"""
        try:
            if not medication_data:
                return go.Figure().add_annotation(
                    text="No medication data available",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5, showarrow=False
                )
            
            df = pd.DataFrame(medication_data)
            df['start_date'] = pd.to_datetime(df['start_date'])
            df['end_date'] = pd.to_datetime(df.get('end_date', datetime.now()))
            
            fig = go.Figure()
            
            # Create Gantt-like chart for medications
            medications = df['medication'].unique()
            colors = px.colors.qualitative.Set3
            
            for i, med in enumerate(medications):
                med_data = df[df['medication'] == med]
                
                for _, row in med_data.iterrows():
                    fig.add_trace(
                        go.Scatter(
                            x=[row['start_date'], row['end_date']],
                            y=[i, i],
                            mode='lines+markers',
                            name=med,
                            line=dict(
                                color=colors[i % len(colors)],
                                width=8
                            ),
                            marker=dict(size=10),
                            hovertemplate=f'<b>{med}</b><br>' +
                                        'Start: %{x[0]}<br>' +
                                        'End: %{x[1]}<br>' +
                                        f'Dose: {row.get("dose", "N/A")}<br>' +
                                        '<extra></extra>',
                            showlegend=False
                        )
                    )
            
            fig.update_layout(
                title="Medication Timeline",
                xaxis_title="Date",
                yaxis=dict(
                    tickmode='array',
                    tickvals=list(range(len(medications))),
                    ticktext=medications,
                    title="Medications"
                ),
                template='plotly_white',
                height=max(300, len(medications) * 50)
            )
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating medication timeline: {str(e)}")
            return go.Figure()
    
    def create_interactive_dashboard(self, patient_data: Dict[str, Any]) -> None:
        """Create an interactive timeline dashboard"""
        st.markdown("### 📈 Patient Timeline Dashboard")
        
        # Timeline options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            timeline_type = st.selectbox(
                "Timeline View",
                ["Comprehensive", "Lab Trends", "GFR Progression", "Medications"]
            )
        
        with col2:
            date_range = st.selectbox(
                "Date Range",
                ["All Time", "Last Year", "Last 6 Months", "Last 3 Months"]
            )
        
        with col3:
            if timeline_type == "Lab Trends":
                available_params = ['creatinine', 'gfr', 'bun', 'albumin', 'hemoglobin', 'phosphorus']
                selected_params = st.multiselect(
                    "Select Parameters",
                    available_params,
                    default=['creatinine', 'gfr']
                )
        
        # Filter data based on date range
        filtered_data = self._filter_data_by_date_range(patient_data, date_range)
        
        # Display appropriate timeline
        if timeline_type == "Comprehensive":
            fig = self.create_comprehensive_timeline(filtered_data)
            st.plotly_chart(fig, use_container_width=True)
            
        elif timeline_type == "Lab Trends":
            lab_data = filtered_data.get('lab_results', [])
            fig = self.create_lab_trends_chart(lab_data, selected_params)
            st.plotly_chart(fig, use_container_width=True)
            
        elif timeline_type == "GFR Progression":
            gfr_data = self._extract_gfr_data(filtered_data.get('lab_results', []))
            fig = self.create_gfr_progression_chart(gfr_data)
            st.plotly_chart(fig, use_container_width=True)
            
        elif timeline_type == "Medications":
            med_data = filtered_data.get('medications', [])
            fig = self.create_medication_timeline(med_data)
            st.plotly_chart(fig, use_container_width=True)
        
        # Timeline insights
        self._display_timeline_insights(filtered_data)
    
    def _filter_data_by_date_range(self, patient_data: Dict[str, Any], date_range: str) -> Dict[str, Any]:
        """Filter patient data by selected date range"""
        if date_range == "All Time":
            return patient_data
        
        # Calculate cutoff date
        now = datetime.now()
        if date_range == "Last Year":
            cutoff = now - timedelta(days=365)
        elif date_range == "Last 6 Months":
            cutoff = now - timedelta(days=180)
        elif date_range == "Last 3 Months":
            cutoff = now - timedelta(days=90)
        else:
            return patient_data
        
        # Filter lab results
        filtered_data = patient_data.copy()
        if 'lab_results' in filtered_data:
            filtered_data['lab_results'] = [
                lab for lab in filtered_data['lab_results']
                if pd.to_datetime(lab['date']) >= cutoff
            ]
        
        # Filter clinical events
        if 'clinical_events' in filtered_data:
            filtered_data['clinical_events'] = [
                event for event in filtered_data['clinical_events']
                if pd.to_datetime(event['date']) >= cutoff
            ]
        
        return filtered_data
    
    def _extract_gfr_data(self, lab_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract GFR data from lab results"""
        gfr_data = []
        for lab in lab_data:
            if lab.get('parameter', '').lower() == 'gfr':
                gfr_data.append({
                    'date': lab['date'],
                    'gfr': float(lab['value'])
                })
        return gfr_data
    
    def _display_timeline_insights(self, patient_data: Dict[str, Any]) -> None:
        """Display insights from timeline data"""
        st.markdown("#### 🔍 Timeline Insights")
        
        insights_col1, insights_col2 = st.columns(2)
        
        with insights_col1:
            # Lab trends insights
            lab_data = patient_data.get('lab_results', [])
            if lab_data:
                st.markdown("**Laboratory Trends:**")
                
                # Calculate trends for key parameters
                for param in ['creatinine', 'gfr']:
                    param_data = [lab for lab in lab_data if lab.get('parameter', '').lower() == param]
                    if len(param_data) >= 2:
                        values = [float(lab['value']) for lab in param_data]
                        trend = "↗️ Increasing" if values[-1] > values[0] else "↘️ Decreasing"
                        change = abs(values[-1] - values[0])
                        st.write(f"• {param.title()}: {trend} ({change:.1f} change)")
        
        with insights_col2:
            # Clinical events summary
            events_data = patient_data.get('clinical_events', [])
            if events_data:
                st.markdown("**Recent Clinical Events:**")
                event_counts = {}
                for event in events_data:
                    event_type = event.get('event_type', 'Unknown')
                    event_counts[event_type] = event_counts.get(event_type, 0) + 1
                
                for event_type, count in event_counts.items():
                    st.write(f"• {event_type.title()}: {count} events")