import streamlit as st
import pandas as pd
from typing import Dict, List, Optional, Tuple
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json

class MobileResponsiveManager:
    """Manager for mobile-responsive design optimization"""
    
    def __init__(self):
        self.device_breakpoints = {
            'mobile': 768,
            'tablet': 1024,
            'desktop': 1200,
            'large_desktop': 1440
        }
        
        self.responsive_config = {
            'mobile': {
                'sidebar_width': 280,
                'chart_height': 300,
                'font_size': 14,
                'padding': '0.5rem',
                'columns': 1,
                'button_size': 'small',
                'input_size': 'small'
            },
            'tablet': {
                'sidebar_width': 320,
                'chart_height': 400,
                'font_size': 16,
                'padding': '1rem',
                'columns': 2,
                'button_size': 'medium',
                'input_size': 'medium'
            },
            'desktop': {
                'sidebar_width': 350,
                'chart_height': 500,
                'font_size': 18,
                'padding': '1.5rem',
                'columns': 3,
                'button_size': 'large',
                'input_size': 'large'
            }
        }
    
    def inject_responsive_css(self):
        """Inject responsive CSS styles"""
        css = """
        <style>
        /* Mobile-first responsive design */
        .main .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
            max-width: 100%;
        }
        
        /* Mobile styles (default) */
        @media (max-width: 768px) {
            .main .block-container {
                padding-left: 0.5rem;
                padding-right: 0.5rem;
            }
            
            .stSelectbox > div > div {
                font-size: 14px;
            }
            
            .stButton > button {
                width: 100%;
                font-size: 14px;
                padding: 0.5rem;
                margin-bottom: 0.5rem;
            }
            
            .stTextInput > div > div > input {
                font-size: 14px;
            }
            
            .stTextArea > div > div > textarea {
                font-size: 14px;
            }
            
            .stMetric {
                background-color: #f0f2f6;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 1rem;
                margin-bottom: 1rem;
            }
            
            .stTabs [data-baseweb="tab-list"] {
                gap: 0.25rem;
            }
            
            .stTabs [data-baseweb="tab"] {
                font-size: 12px;
                padding: 0.5rem 0.75rem;
            }
            
            .stSidebar > div {
                width: 280px;
            }
            
            /* Hide complex charts on mobile, show simplified versions */
            .mobile-hide {
                display: none;
            }
            
            .mobile-show {
                display: block;
            }
        }
        
        /* Tablet styles */
        @media (min-width: 769px) and (max-width: 1024px) {
            .main .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }
            
            .stButton > button {
                font-size: 16px;
                padding: 0.75rem 1rem;
            }
            
            .stSidebar > div {
                width: 320px;
            }
            
            .mobile-hide {
                display: block;
            }
            
            .mobile-show {
                display: none;
            }
        }
        
        /* Desktop styles */
        @media (min-width: 1025px) {
            .main .block-container {
                padding-left: 1.5rem;
                padding-right: 1.5rem;
            }
            
            .stSidebar > div {
                width: 350px;
            }
            
            .mobile-hide {
                display: block;
            }
            
            .mobile-show {
                display: none;
            }
        }
        
        /* Touch-friendly improvements */
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            transition: all 0.2s ease;
        }
        
        /* Improved form layouts */
        .stForm {
            background-color: #ffffff;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
        }
        
        /* Better spacing for mobile */
        .element-container {
            margin-bottom: 1rem;
        }
        
        /* Responsive tables */
        .stDataFrame {
            overflow-x: auto;
        }
        
        /* Loading states */
        .stSpinner {
            text-align: center;
            padding: 2rem;
        }
        
        /* Alert styles */
        .stAlert {
            border-radius: 8px;
            margin-bottom: 1rem;
        }
        
        /* Progress bars */
        .stProgress > div > div {
            border-radius: 10px;
        }
        
        /* Custom card component */
        .custom-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
            border: 1px solid #e0e0e0;
        }
        
        .custom-card h3 {
            margin-top: 0;
            color: #1f2937;
            font-weight: 600;
        }
        
        /* Responsive grid */
        .responsive-grid {
            display: grid;
            gap: 1rem;
            grid-template-columns: 1fr;
        }
        
        @media (min-width: 769px) {
            .responsive-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
        
        @media (min-width: 1025px) {
            .responsive-grid {
                grid-template-columns: repeat(3, 1fr);
            }
        }
        
        /* Dark mode support */
        @media (prefers-color-scheme: dark) {
            .custom-card {
                background: #1f2937;
                border-color: #374151;
                color: #f9fafb;
            }
            
            .custom-card h3 {
                color: #f9fafb;
            }
        }
        </style>
        """
        
        st.markdown(css, unsafe_allow_html=True)
    
    def get_device_type(self) -> str:
        """Detect device type based on screen width"""
        # This is a simplified detection - in a real app, you'd use JavaScript
        # For now, we'll use session state to simulate device detection
        if 'device_type' not in st.session_state:
            st.session_state.device_type = 'desktop'  # Default
        
        return st.session_state.device_type
    
    def set_device_type(self, device_type: str):
        """Set device type for testing"""
        st.session_state.device_type = device_type
    
    def get_responsive_config(self, device_type: str = None) -> Dict:
        """Get responsive configuration for current device"""
        if device_type is None:
            device_type = self.get_device_type()
        
        return self.responsive_config.get(device_type, self.responsive_config['desktop'])
    
    def create_responsive_columns(self, ratios: List[float] = None) -> List:
        """Create responsive columns based on device type"""
        device_type = self.get_device_type()
        config = self.get_responsive_config(device_type)
        
        if device_type == 'mobile':
            # Single column on mobile
            return [st.container()]
        elif device_type == 'tablet':
            # Two columns on tablet
            if ratios and len(ratios) >= 2:
                return st.columns(ratios[:2])
            return st.columns(2)
        else:
            # Full columns on desktop
            if ratios:
                return st.columns(ratios)
            return st.columns(config['columns'])
    
    def create_responsive_chart(self, fig, title: str = "", mobile_height: int = 300) -> go.Figure:
        """Create responsive chart with device-specific settings"""
        device_type = self.get_device_type()
        config = self.get_responsive_config(device_type)
        
        # Update layout for responsiveness
        fig.update_layout(
            title={
                'text': title,
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': config['font_size']}
            },
            height=config['chart_height'],
            margin=dict(l=20, r=20, t=40, b=20),
            font=dict(size=config['font_size'] - 2),
            showlegend=device_type != 'mobile',  # Hide legend on mobile
            autosize=True
        )
        
        # Simplify chart for mobile
        if device_type == 'mobile':
            fig.update_layout(
                xaxis_title="",
                yaxis_title="",
                showlegend=False
            )
            
            # Reduce number of data points for mobile
            if hasattr(fig, 'data') and len(fig.data) > 0:
                for trace in fig.data:
                    if hasattr(trace, 'x') and len(trace.x) > 20:
                        # Sample data for mobile
                        step = len(trace.x) // 15
                        trace.x = trace.x[::step]
                        if hasattr(trace, 'y'):
                            trace.y = trace.y[::step]
        
        return fig
    
    def create_mobile_friendly_table(self, df: pd.DataFrame, max_rows: int = 10) -> pd.DataFrame:
        """Create mobile-friendly table"""
        device_type = self.get_device_type()
        
        if device_type == 'mobile':
            # Limit columns and rows for mobile
            if len(df.columns) > 3:
                # Show only first 3 columns
                df = df.iloc[:, :3]
            
            # Limit rows
            if len(df) > max_rows:
                df = df.head(max_rows)
            
            # Shorten column names
            df.columns = [col[:10] + '...' if len(col) > 10 else col for col in df.columns]
        
        return df
    
    def create_responsive_metrics(self, metrics: List[Dict], cols_per_row: int = 4):
        """Create responsive metrics display"""
        device_type = self.get_device_type()
        
        if device_type == 'mobile':
            # Stack metrics vertically on mobile
            for metric in metrics:
                with st.container():
                    st.metric(
                        label=metric['label'],
                        value=metric['value'],
                        delta=metric.get('delta')
                    )
        else:
            # Use columns for larger screens
            cols = st.columns(min(len(metrics), cols_per_row))
            for i, metric in enumerate(metrics):
                with cols[i % len(cols)]:
                    st.metric(
                        label=metric['label'],
                        value=metric['value'],
                        delta=metric.get('delta')
                    )
    
    def create_responsive_form(self, form_key: str, fields: List[Dict]):
        """Create responsive form with device-specific layouts"""
        device_type = self.get_device_type()
        
        with st.form(form_key):
            if device_type == 'mobile':
                # Stack all fields vertically on mobile
                for field in fields:
                    self._render_form_field(field)
            else:
                # Use columns for larger screens
                cols = st.columns(2)
                for i, field in enumerate(fields):
                    with cols[i % 2]:
                        self._render_form_field(field)
            
            # Submit button
            submitted = st.form_submit_button(
                "Submit",
                use_container_width=device_type == 'mobile'
            )
            
            return submitted
    
    def _render_form_field(self, field: Dict):
        """Render individual form field"""
        field_type = field.get('type', 'text')
        label = field.get('label', '')
        key = field.get('key', '')
        
        if field_type == 'text':
            st.text_input(label, key=key)
        elif field_type == 'textarea':
            st.text_area(label, key=key)
        elif field_type == 'number':
            st.number_input(label, key=key)
        elif field_type == 'select':
            options = field.get('options', [])
            st.selectbox(label, options, key=key)
        elif field_type == 'multiselect':
            options = field.get('options', [])
            st.multiselect(label, options, key=key)
        elif field_type == 'date':
            st.date_input(label, key=key)
        elif field_type == 'time':
            st.time_input(label, key=key)
        elif field_type == 'checkbox':
            st.checkbox(label, key=key)
    
    def create_responsive_sidebar(self, content_func):
        """Create responsive sidebar"""
        device_type = self.get_device_type()
        
        if device_type == 'mobile':
            # Use expander for mobile navigation
            with st.expander("📱 Navigation Menu", expanded=False):
                content_func()
        else:
            # Use regular sidebar for larger screens
            with st.sidebar:
                content_func()
    
    def add_device_selector(self):
        """Add device type selector for testing"""
        if st.checkbox("🔧 Developer Mode", key="dev_mode"):
            device_type = st.selectbox(
                "Device Type (for testing)",
                options=['mobile', 'tablet', 'desktop'],
                index=['mobile', 'tablet', 'desktop'].index(self.get_device_type()),
                key="device_selector"
            )
            
            if device_type != self.get_device_type():
                self.set_device_type(device_type)
                st.experimental_rerun()
    
    def create_responsive_card(self, title: str, content: str, actions: List[Dict] = None):
        """Create responsive card component"""
        device_type = self.get_device_type()
        
        card_html = f"""
        <div class="custom-card">
            <h3>{title}</h3>
            <p>{content}</p>
        </div>
        """
        
        st.markdown(card_html, unsafe_allow_html=True)
        
        if actions:
            if device_type == 'mobile':
                # Stack buttons vertically on mobile
                for action in actions:
                    st.button(
                        action['label'],
                        key=action.get('key'),
                        use_container_width=True
                    )
            else:
                # Use columns for buttons on larger screens
                cols = st.columns(len(actions))
                for i, action in enumerate(actions):
                    with cols[i]:
                        st.button(
                            action['label'],
                            key=action.get('key')
                        )
    
    def optimize_dataframe_display(self, df: pd.DataFrame, max_width: int = None) -> pd.DataFrame:
        """Optimize dataframe display for different devices"""
        device_type = self.get_device_type()
        
        if device_type == 'mobile':
            # Limit columns for mobile
            if len(df.columns) > 4:
                df = df.iloc[:, :4]
            
            # Truncate long text in cells
            for col in df.select_dtypes(include=['object']).columns:
                df[col] = df[col].astype(str).apply(
                    lambda x: x[:20] + '...' if len(x) > 20 else x
                )
        
        return df
    
    def get_responsive_plot_config(self) -> Dict:
        """Get plot configuration for current device"""
        device_type = self.get_device_type()
        config = self.get_responsive_config(device_type)
        
        return {
            'displayModeBar': device_type != 'mobile',
            'responsive': True,
            'toImageButtonOptions': {
                'format': 'png',
                'filename': 'chart',
                'height': config['chart_height'],
                'width': None,
                'scale': 1
            }
        }

# Global instance
_responsive_manager = None

def get_responsive_manager() -> MobileResponsiveManager:
    """Get the global responsive manager instance"""
    global _responsive_manager
    if _responsive_manager is None:
        _responsive_manager = MobileResponsiveManager()
    return _responsive_manager

def init_responsive_design():
    """Initialize responsive design for the app"""
    manager = get_responsive_manager()
    manager.inject_responsive_css()
    return manager