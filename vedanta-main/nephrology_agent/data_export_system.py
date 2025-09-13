import pandas as pd
import io
import base64
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import json
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import numpy as np

class DataExportSystem:
    """Comprehensive data export and reporting system for nephrology data"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.custom_styles = self._create_custom_styles()
        
    def _create_custom_styles(self):
        """Create custom styles for PDF reports"""
        styles = {}
        
        # Title style
        styles['CustomTitle'] = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Title'],
            fontSize=18,
            spaceAfter=30,
            textColor=colors.HexColor('#2c3e50'),
            alignment=1  # Center alignment
        )
        
        # Header style
        styles['CustomHeader'] = ParagraphStyle(
            'CustomHeader',
            parent=self.styles['Heading1'],
            fontSize=14,
            spaceAfter=12,
            textColor=colors.HexColor('#34495e'),
            borderWidth=1,
            borderColor=colors.HexColor('#bdc3c7')
        )
        
        # Body style
        styles['CustomBody'] = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            textColor=colors.HexColor('#2c3e50')
        )
        
        return styles
    
    def export_patient_data_csv(self, patient_data: Dict[str, Any], 
                               lab_results: List[Dict[str, Any]] = None,
                               assessments: List[Dict[str, Any]] = None) -> str:
        """Export patient data to CSV format"""
        try:
            # Create patient summary
            patient_summary = {
                'Patient_ID': patient_data.get('id', 'N/A'),
                'Age': patient_data.get('age', 'N/A'),
                'Gender': patient_data.get('gender', 'N/A'),
                'Diabetes': patient_data.get('diabetes', False),
                'Hypertension': patient_data.get('hypertension', False),
                'CVD': patient_data.get('cardiovascular_disease', False),
                'Export_Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Convert to DataFrame
            df_patient = pd.DataFrame([patient_summary])
            
            # Lab results DataFrame
            df_labs = pd.DataFrame(lab_results) if lab_results else pd.DataFrame()
            
            # Assessments DataFrame
            df_assessments = pd.DataFrame(assessments) if assessments else pd.DataFrame()
            
            # Create CSV content
            output = io.StringIO()
            
            # Write patient data
            output.write("PATIENT INFORMATION\n")
            df_patient.to_csv(output, index=False)
            output.write("\n")
            
            # Write lab results
            if not df_labs.empty:
                output.write("LAB RESULTS\n")
                df_labs.to_csv(output, index=False)
                output.write("\n")
            
            # Write assessments
            if not df_assessments.empty:
                output.write("CLINICAL ASSESSMENTS\n")
                df_assessments.to_csv(output, index=False)
            
            return output.getvalue()
            
        except Exception as e:
            return f"Error exporting CSV: {str(e)}"
    
    def export_patient_data_excel(self, patient_data: Dict[str, Any],
                                 lab_results: List[Dict[str, Any]] = None,
                                 assessments: List[Dict[str, Any]] = None,
                                 predictions: Dict[str, Any] = None) -> bytes:
        """Export comprehensive patient data to Excel format"""
        try:
            output = BytesIO()
            
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                # Patient Summary Sheet
                patient_summary = {
                    'Field': ['Patient ID', 'Age', 'Gender', 'Diabetes', 'Hypertension', 
                             'Cardiovascular Disease', 'Export Date'],
                    'Value': [
                        patient_data.get('id', 'N/A'),
                        patient_data.get('age', 'N/A'),
                        patient_data.get('gender', 'N/A'),
                        'Yes' if patient_data.get('diabetes', False) else 'No',
                        'Yes' if patient_data.get('hypertension', False) else 'No',
                        'Yes' if patient_data.get('cardiovascular_disease', False) else 'No',
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    ]
                }
                df_patient = pd.DataFrame(patient_summary)
                df_patient.to_excel(writer, sheet_name='Patient Summary', index=False)
                
                # Lab Results Sheet
                if lab_results:
                    df_labs = pd.DataFrame(lab_results)
                    df_labs.to_excel(writer, sheet_name='Lab Results', index=False)
                
                # Clinical Assessments Sheet
                if assessments:
                    df_assessments = pd.DataFrame(assessments)
                    df_assessments.to_excel(writer, sheet_name='Clinical Assessments', index=False)
                
                # ML Predictions Sheet
                if predictions:
                    pred_data = []
                    for pred_type, pred_data_item in predictions.items():
                        if isinstance(pred_data_item, dict):
                            for key, value in pred_data_item.items():
                                pred_data.append({
                                    'Prediction_Type': pred_type,
                                    'Metric': key,
                                    'Value': value
                                })
                    
                    if pred_data:
                        df_predictions = pd.DataFrame(pred_data)
                        df_predictions.to_excel(writer, sheet_name='ML Predictions', index=False)
            
            output.seek(0)
            return output.getvalue()
            
        except Exception as e:
            return f"Error exporting Excel: {str(e)}".encode()
    
    def generate_clinical_report_pdf(self, patient_data: Dict[str, Any],
                                   lab_results: List[Dict[str, Any]] = None,
                                   assessments: List[Dict[str, Any]] = None,
                                   predictions: Dict[str, Any] = None,
                                   alerts: Dict[str, Any] = None) -> bytes:
        """Generate comprehensive clinical report in PDF format"""
        try:
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4)
            story = []
            
            # Title
            title = Paragraph("Nephrology Clinical Report", self.custom_styles['CustomTitle'])
            story.append(title)
            story.append(Spacer(1, 20))
            
            # Report metadata
            report_info = f"""<b>Report Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>
            <b>Patient ID:</b> {patient_data.get('id', 'N/A')}<br/>
            <b>Report Type:</b> Comprehensive Clinical Assessment"""
            story.append(Paragraph(report_info, self.custom_styles['CustomBody']))
            story.append(Spacer(1, 20))
            
            # Patient Information Section
            story.append(Paragraph("Patient Information", self.custom_styles['CustomHeader']))
            
            patient_info_data = [
                ['Field', 'Value'],
                ['Age', str(patient_data.get('age', 'N/A'))],
                ['Gender', patient_data.get('gender', 'N/A')],
                ['Diabetes', 'Yes' if patient_data.get('diabetes', False) else 'No'],
                ['Hypertension', 'Yes' if patient_data.get('hypertension', False) else 'No'],
                ['Cardiovascular Disease', 'Yes' if patient_data.get('cardiovascular_disease', False) else 'No']
            ]
            
            patient_table = Table(patient_info_data)
            patient_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ecf0f1')),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(patient_table)
            story.append(Spacer(1, 20))
            
            # Lab Results Section
            if lab_results:
                story.append(Paragraph("Laboratory Results", self.custom_styles['CustomHeader']))
                
                lab_data = [['Parameter', 'Value', 'Reference Range', 'Status']]
                for lab in lab_results:
                    status = self._get_lab_status(lab.get('parameter'), lab.get('value'))
                    lab_data.append([
                        lab.get('parameter', 'N/A'),
                        str(lab.get('value', 'N/A')),
                        lab.get('reference_range', 'N/A'),
                        status
                    ])
                
                lab_table = Table(lab_data)
                lab_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fadbd8')),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                story.append(lab_table)
                story.append(Spacer(1, 20))
            
            # ML Predictions Section
            if predictions:
                story.append(Paragraph("AI Predictions & Risk Assessment", self.custom_styles['CustomHeader']))
                
                # Create predictions summary
                pred_summary = []
                if 'dialysis_initiation' in predictions:
                    dialysis_risk = predictions['dialysis_initiation'].get('risk_score', 0)
                    pred_summary.append(f"Dialysis Initiation Risk (1 year): {dialysis_risk:.1%}")
                
                if 'mortality_risk' in predictions:
                    mortality_risk = predictions['mortality_risk'].get('risk_score', 0)
                    pred_summary.append(f"Mortality Risk (5 year): {mortality_risk:.1%}")
                
                if 'disease_progression' in predictions:
                    progression_rate = predictions['disease_progression'].get('progression_rate', 0)
                    pred_summary.append(f"GFR Decline Rate: {progression_rate:.1f} mL/min/year")
                
                for summary in pred_summary:
                    story.append(Paragraph(f"• {summary}", self.custom_styles['CustomBody']))
                
                story.append(Spacer(1, 20))
            
            # Alerts Section
            if alerts and alerts.get('critical_values', {}).get('alerts'):
                story.append(Paragraph("Critical Alerts", self.custom_styles['CustomHeader']))
                
                for alert in alerts['critical_values']['alerts']:
                    alert_text = f"<b>{alert.get('severity', 'ALERT').upper()}:</b> {alert.get('message', 'N/A')}"
                    story.append(Paragraph(alert_text, self.custom_styles['CustomBody']))
                
                story.append(Spacer(1, 20))
            
            # Clinical Assessments Section
            if assessments:
                story.append(Paragraph("Clinical Assessments", self.custom_styles['CustomHeader']))
                
                for assessment in assessments[-3:]:  # Last 3 assessments
                    assessment_text = f"""<b>Date:</b> {assessment.get('date', 'N/A')}<br/>
                    <b>Assessment:</b> {assessment.get('assessment', 'N/A')}<br/>
                    <b>Recommendations:</b> {assessment.get('recommendations', 'N/A')}"""
                    story.append(Paragraph(assessment_text, self.custom_styles['CustomBody']))
                    story.append(Spacer(1, 10))
            
            # Footer
            story.append(Spacer(1, 30))
            footer_text = """<i>This report is generated by AI and should be reviewed by a qualified healthcare professional. 
            This information is for clinical decision support only and should not replace professional medical judgment.</i>"""
            story.append(Paragraph(footer_text, self.custom_styles['CustomBody']))
            
            # Build PDF
            doc.build(story)
            buffer.seek(0)
            return buffer.getvalue()
            
        except Exception as e:
            return f"Error generating PDF: {str(e)}".encode()
    
    def _get_lab_status(self, parameter: str, value: Any) -> str:
        """Determine lab value status based on reference ranges"""
        try:
            if parameter and value is not None:
                value = float(value)
                
                # Define reference ranges (simplified)
                ranges = {
                    'creatinine': (0.6, 1.2),
                    'gfr': (90, 120),
                    'bun': (7, 20),
                    'potassium': (3.5, 5.0),
                    'hemoglobin': (12.0, 16.0),
                    'albumin': (3.5, 5.0)
                }
                
                param_lower = parameter.lower()
                for key, (low, high) in ranges.items():
                    if key in param_lower:
                        if value < low:
                            return "LOW"
                        elif value > high:
                            return "HIGH"
                        else:
                            return "NORMAL"
            
            return "UNKNOWN"
            
        except (ValueError, TypeError):
            return "INVALID"
    
    def generate_trend_analysis_chart(self, lab_data: List[Dict[str, Any]], 
                                    parameter: str) -> bytes:
        """Generate trend analysis chart for lab parameters"""
        try:
            # Extract data for the specific parameter
            dates = []
            values = []
            
            for lab in lab_data:
                if lab.get('parameter', '').lower() == parameter.lower():
                    dates.append(pd.to_datetime(lab.get('date', datetime.now())))
                    values.append(float(lab.get('value', 0)))
            
            if not dates or not values:
                return b"No data available for trend analysis"
            
            # Create the plot
            plt.figure(figsize=(10, 6))
            plt.plot(dates, values, marker='o', linewidth=2, markersize=6)
            plt.title(f'{parameter.title()} Trend Analysis', fontsize=16, fontweight='bold')
            plt.xlabel('Date', fontsize=12)
            plt.ylabel(f'{parameter.title()} Value', fontsize=12)
            plt.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # Save to bytes
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
            buffer.seek(0)
            plt.close()
            
            return buffer.getvalue()
            
        except Exception as e:
            return f"Error generating chart: {str(e)}".encode()
    
    def export_analytics_summary(self, analytics_data: Dict[str, Any]) -> Dict[str, Any]:
        """Export analytics summary in multiple formats"""
        try:
            summary = {
                'export_timestamp': datetime.now().isoformat(),
                'total_patients': analytics_data.get('total_patients', 0),
                'total_assessments': analytics_data.get('total_assessments', 0),
                'average_risk_score': analytics_data.get('average_risk_score', 0),
                'high_risk_patients': analytics_data.get('high_risk_patients', 0),
                'common_conditions': analytics_data.get('common_conditions', []),
                'monthly_trends': analytics_data.get('monthly_trends', {})
            }
            
            # Generate CSV format
            csv_data = pd.DataFrame([summary]).to_csv(index=False)
            
            # Generate JSON format
            json_data = json.dumps(summary, indent=2)
            
            return {
                'summary': summary,
                'csv_format': csv_data,
                'json_format': json_data
            }
            
        except Exception as e:
            return {'error': f"Error exporting analytics: {str(e)}"}
    
    def create_batch_export(self, patients_data: List[Dict[str, Any]], 
                           export_format: str = 'excel') -> bytes:
        """Create batch export for multiple patients"""
        try:
            if export_format.lower() == 'excel':
                output = BytesIO()
                
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    # Summary sheet
                    summary_data = []
                    for patient in patients_data:
                        summary_data.append({
                            'Patient_ID': patient.get('id', 'N/A'),
                            'Age': patient.get('age', 'N/A'),
                            'Gender': patient.get('gender', 'N/A'),
                            'Risk_Level': patient.get('risk_level', 'N/A'),
                            'Last_Assessment': patient.get('last_assessment_date', 'N/A')
                        })
                    
                    df_summary = pd.DataFrame(summary_data)
                    df_summary.to_excel(writer, sheet_name='Patient Summary', index=False)
                    
                    # Individual patient sheets (limit to first 10 for performance)
                    for i, patient in enumerate(patients_data[:10]):
                        sheet_name = f"Patient_{patient.get('id', i+1)}"
                        patient_df = pd.DataFrame([patient])
                        patient_df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                output.seek(0)
                return output.getvalue()
            
            elif export_format.lower() == 'csv':
                # Create comprehensive CSV
                df = pd.DataFrame(patients_data)
                return df.to_csv(index=False).encode()
            
            else:
                return b"Unsupported export format"
                
        except Exception as e:
            return f"Error in batch export: {str(e)}".encode()