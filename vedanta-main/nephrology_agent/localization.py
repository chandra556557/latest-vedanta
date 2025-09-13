import streamlit as st
from typing import Dict, Any
import json
import os

class LocalizationManager:
    def __init__(self):
        self.current_language = 'en'
        self.translations = {}
        self.load_translations()
    
    def load_translations(self):
        """Load translation files for supported languages"""
        self.translations = {
            'en': {
                # Navigation and Headers
                'app_title': 'Advanced Nephrology AI Agent',
                'app_subtitle': 'AI-Powered Kidney Health Assessment & Clinical Decision Support',
                'welcome_message': 'Welcome to the Advanced Nephrology AI Agent',
                
                # Tab Labels
                'tab_consultation': '💬 AI Consultation',
                'tab_clinical_intelligence': '🧠 AI Clinical Intelligence',
                'tab_risk_assessment': '🧮 Risk Assessment',
                'tab_analytics': '📊 Analytics',
                'tab_timeline': '📈 Patient Timeline',
                'tab_monitoring': '🚨 Real-Time Monitoring',
                'tab_patient_portal': '👤 Patient Portal',
                
                # Common UI Elements
                'login': 'Login',
                'logout': 'Logout',
                'submit': 'Submit',
                'cancel': 'Cancel',
                'save': 'Save',
                'delete': 'Delete',
                'edit': 'Edit',
                'view': 'View',
                'download': 'Download',
                'upload': 'Upload',
                'search': 'Search',
                'filter': 'Filter',
                'sort': 'Sort',
                'refresh': 'Refresh',
                'loading': 'Loading...',
                'error': 'Error',
                'success': 'Success',
                'warning': 'Warning',
                'info': 'Information',
                
                # Patient Portal
                'patient_portal_title': 'Patient Portal',
                'patient_portal_subtitle': 'Secure patient access to medical records, appointments, and communication',
                'patient_login': 'Patient Login',
                'email_address': 'Email Address',
                'password': 'Password',
                'demo_credentials': 'Demo Credentials',
                'login_successful': 'Login successful! Redirecting to dashboard...',
                'invalid_credentials': 'Invalid email or password. Please try again.',
                'enter_credentials': 'Please enter both email and password.',
                'new_patient_info': 'New Patient? Contact your healthcare provider to set up portal access.',
                'welcome_patient': 'Welcome, {name}',
                'medical_record_number': 'MRN: {mrn}',
                
                # Dashboard Metrics
                'upcoming_appointments': 'Upcoming Appointments',
                'recent_lab_results': 'Recent Lab Results',
                'unread_messages': 'Unread Messages',
                'total_records': 'Total Records',
                
                # Portal Sections
                'dashboard': 'Dashboard',
                'appointments': 'Appointments',
                'lab_results': 'Lab Results',
                'messages': 'Messages',
                'profile': 'Profile',
                'health_dashboard': 'Health Dashboard',
                'my_appointments': 'My Appointments',
                'my_profile': 'My Profile',
                
                # Actions
                'schedule_appointment': 'Schedule Appointment',
                'request_prescription_refill': 'Request Prescription Refill',
                'contact_provider': 'Contact Provider',
                'update_contact_info': 'Update Contact Info',
                'change_password': 'Change Password',
                'download_records': 'Download Records',
                'mark_as_read': 'Mark as Read',
                'send_message': 'Send Message',
                
                # Medical Information
                'personal_information': 'Personal Information',
                'medical_information': 'Medical Information',
                'name': 'Name',
                'date_of_birth': 'Date of Birth',
                'phone': 'Phone',
                'emergency_contact': 'Emergency Contact',
                'doctor': 'Doctor',
                'date': 'Date',
                'time': 'Time',
                'status': 'Status',
                'notes': 'Notes',
                'test': 'Test',
                'result': 'Result',
                'reference': 'Reference',
                'subject': 'Subject',
                'message': 'Message',
                
                # Clinical Terms
                'creatinine': 'Creatinine',
                'bun': 'BUN',
                'egfr': 'eGFR',
                'protein_urine': 'Protein (Urine)',
                'blood_pressure': 'Blood Pressure',
                'kidney_function': 'Kidney Function',
                
                # Status Messages
                'no_appointments_found': 'No appointments found.',
                'no_lab_results_found': 'No lab results found.',
                'no_messages_found': 'No messages found.',
                'message_sent_successfully': 'Message sent successfully! You will receive a response within 24-48 hours.',
                'fill_subject_message': 'Please fill in both subject and message.',
                'contact_patient_services': 'Please contact Patient Services at (555) 123-4567 to update your contact information.',
                'password_change_info': 'Password changes can be requested through Patient Services for security purposes.',
                'records_request_info': 'Medical records can be requested through Patient Services. Processing may take 3-5 business days.',
                
                # AI Consultation
                'ai_consultation_title': 'AI Consultation',
                'enter_symptoms': 'Enter your symptoms or medical concerns',
                'get_ai_response': 'Get AI Response',
                'medical_disclaimer': 'Medical Disclaimer: This AI assistant provides educational information only and should not replace professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare providers for medical decisions.',
                
                # Risk Assessment
                'risk_assessment_title': 'Risk Assessment',
                'patient_age': 'Patient Age',
                'serum_creatinine': 'Serum Creatinine (mg/dL)',
                'blood_pressure_systolic': 'Systolic Blood Pressure (mmHg)',
                'diabetes': 'Diabetes',
                'hypertension': 'Hypertension',
                'calculate_risk': 'Calculate Risk',
                'risk_level': 'Risk Level',
                'low_risk': 'Low Risk',
                'moderate_risk': 'Moderate Risk',
                'high_risk': 'High Risk',
                
                # Monitoring
                'real_time_monitoring': 'Real-Time Monitoring',
                'active_alerts': 'Active Alerts',
                'patient_dashboard_monitoring': 'Patient Dashboard',
                'alert_management': 'Alert Management',
                'simulate_data': 'Simulate Data',
                'auto_refresh': 'Auto Refresh',
                'enable_auto_refresh': 'Enable Auto Refresh',
                'refresh_interval': 'Refresh Interval (seconds)',
            },
            
            'es': {
                # Navigation and Headers
                'app_title': 'Agente de IA de Nefrología Avanzada',
                'app_subtitle': 'Evaluación de Salud Renal y Soporte de Decisiones Clínicas con IA',
                'welcome_message': 'Bienvenido al Agente de IA de Nefrología Avanzada',
                
                # Tab Labels
                'tab_consultation': '💬 Consulta de IA',
                'tab_clinical_intelligence': '🧠 Inteligencia Clínica de IA',
                'tab_risk_assessment': '🧮 Evaluación de Riesgo',
                'tab_analytics': '📊 Analíticas',
                'tab_timeline': '📈 Línea de Tiempo del Paciente',
                'tab_monitoring': '🚨 Monitoreo en Tiempo Real',
                'tab_patient_portal': '👤 Portal del Paciente',
                
                # Common UI Elements
                'login': 'Iniciar Sesión',
                'logout': 'Cerrar Sesión',
                'submit': 'Enviar',
                'cancel': 'Cancelar',
                'save': 'Guardar',
                'delete': 'Eliminar',
                'edit': 'Editar',
                'view': 'Ver',
                'download': 'Descargar',
                'upload': 'Subir',
                'search': 'Buscar',
                'filter': 'Filtrar',
                'sort': 'Ordenar',
                'refresh': 'Actualizar',
                'loading': 'Cargando...',
                'error': 'Error',
                'success': 'Éxito',
                'warning': 'Advertencia',
                'info': 'Información',
                
                # Patient Portal
                'patient_portal_title': 'Portal del Paciente',
                'patient_portal_subtitle': 'Acceso seguro del paciente a registros médicos, citas y comunicación',
                'patient_login': 'Inicio de Sesión del Paciente',
                'email_address': 'Dirección de Correo Electrónico',
                'password': 'Contraseña',
                'demo_credentials': 'Credenciales de Demostración',
                'login_successful': '¡Inicio de sesión exitoso! Redirigiendo al panel...',
                'invalid_credentials': 'Correo electrónico o contraseña inválidos. Inténtalo de nuevo.',
                'enter_credentials': 'Por favor ingresa tanto el correo electrónico como la contraseña.',
                'new_patient_info': '¿Nuevo Paciente? Contacta a tu proveedor de atención médica para configurar el acceso al portal.',
                'welcome_patient': 'Bienvenido, {name}',
                'medical_record_number': 'NMR: {mrn}',
                
                # Dashboard Metrics
                'upcoming_appointments': 'Citas Próximas',
                'recent_lab_results': 'Resultados de Laboratorio Recientes',
                'unread_messages': 'Mensajes No Leídos',
                'total_records': 'Registros Totales',
                
                # Portal Sections
                'dashboard': 'Panel',
                'appointments': 'Citas',
                'lab_results': 'Resultados de Laboratorio',
                'messages': 'Mensajes',
                'profile': 'Perfil',
                'health_dashboard': 'Panel de Salud',
                'my_appointments': 'Mis Citas',
                'my_profile': 'Mi Perfil',
                
                # Actions
                'schedule_appointment': 'Programar Cita',
                'request_prescription_refill': 'Solicitar Renovación de Receta',
                'contact_provider': 'Contactar Proveedor',
                'update_contact_info': 'Actualizar Información de Contacto',
                'change_password': 'Cambiar Contraseña',
                'download_records': 'Descargar Registros',
                'mark_as_read': 'Marcar como Leído',
                'send_message': 'Enviar Mensaje',
                
                # Medical Information
                'personal_information': 'Información Personal',
                'medical_information': 'Información Médica',
                'name': 'Nombre',
                'date_of_birth': 'Fecha de Nacimiento',
                'phone': 'Teléfono',
                'emergency_contact': 'Contacto de Emergencia',
                'doctor': 'Doctor',
                'date': 'Fecha',
                'time': 'Hora',
                'status': 'Estado',
                'notes': 'Notas',
                'test': 'Prueba',
                'result': 'Resultado',
                'reference': 'Referencia',
                'subject': 'Asunto',
                'message': 'Mensaje',
                
                # Clinical Terms
                'creatinine': 'Creatinina',
                'bun': 'BUN',
                'egfr': 'TFGe',
                'protein_urine': 'Proteína (Orina)',
                'blood_pressure': 'Presión Arterial',
                'kidney_function': 'Función Renal',
                
                # Status Messages
                'no_appointments_found': 'No se encontraron citas.',
                'no_lab_results_found': 'No se encontraron resultados de laboratorio.',
                'no_messages_found': 'No se encontraron mensajes.',
                'message_sent_successfully': '¡Mensaje enviado exitosamente! Recibirás una respuesta en 24-48 horas.',
                'fill_subject_message': 'Por favor completa tanto el asunto como el mensaje.',
                'contact_patient_services': 'Por favor contacta a Servicios al Paciente al (555) 123-4567 para actualizar tu información de contacto.',
                'password_change_info': 'Los cambios de contraseña pueden solicitarse a través de Servicios al Paciente por razones de seguridad.',
                'records_request_info': 'Los registros médicos pueden solicitarse a través de Servicios al Paciente. El procesamiento puede tomar 3-5 días hábiles.',
                
                # AI Consultation
                'ai_consultation_title': 'Consulta de IA',
                'enter_symptoms': 'Ingresa tus síntomas o preocupaciones médicas',
                'get_ai_response': 'Obtener Respuesta de IA',
                'medical_disclaimer': 'Descargo de Responsabilidad Médica: Este asistente de IA proporciona información educativa únicamente y no debe reemplazar el consejo, diagnóstico o tratamiento médico profesional. Siempre consulta con proveedores de atención médica calificados para decisiones médicas.',
                
                # Risk Assessment
                'risk_assessment_title': 'Evaluación de Riesgo',
                'patient_age': 'Edad del Paciente',
                'serum_creatinine': 'Creatinina Sérica (mg/dL)',
                'blood_pressure_systolic': 'Presión Arterial Sistólica (mmHg)',
                'diabetes': 'Diabetes',
                'hypertension': 'Hipertensión',
                'calculate_risk': 'Calcular Riesgo',
                'risk_level': 'Nivel de Riesgo',
                'low_risk': 'Riesgo Bajo',
                'moderate_risk': 'Riesgo Moderado',
                'high_risk': 'Riesgo Alto',
                
                # Monitoring
                'real_time_monitoring': 'Monitoreo en Tiempo Real',
                'active_alerts': 'Alertas Activas',
                'patient_dashboard_monitoring': 'Panel del Paciente',
                'alert_management': 'Gestión de Alertas',
                'simulate_data': 'Simular Datos',
                'auto_refresh': 'Actualización Automática',
                'enable_auto_refresh': 'Habilitar Actualización Automática',
                'refresh_interval': 'Intervalo de Actualización (segundos)',
            },
            
            'fr': {
                # Navigation and Headers
                'app_title': 'Agent IA de Néphrologie Avancée',
                'app_subtitle': 'Évaluation de la Santé Rénale et Support de Décision Clinique par IA',
                'welcome_message': 'Bienvenue dans l\'Agent IA de Néphrologie Avancée',
                
                # Tab Labels
                'tab_consultation': '💬 Consultation IA',
                'tab_clinical_intelligence': '🧠 Intelligence Clinique IA',
                'tab_risk_assessment': '🧮 Évaluation des Risques',
                'tab_analytics': '📊 Analyses',
                'tab_timeline': '📈 Chronologie du Patient',
                'tab_monitoring': '🚨 Surveillance en Temps Réel',
                'tab_patient_portal': '👤 Portail Patient',
                
                # Common UI Elements
                'login': 'Connexion',
                'logout': 'Déconnexion',
                'submit': 'Soumettre',
                'cancel': 'Annuler',
                'save': 'Sauvegarder',
                'delete': 'Supprimer',
                'edit': 'Modifier',
                'view': 'Voir',
                'download': 'Télécharger',
                'upload': 'Téléverser',
                'search': 'Rechercher',
                'filter': 'Filtrer',
                'sort': 'Trier',
                'refresh': 'Actualiser',
                'loading': 'Chargement...',
                'error': 'Erreur',
                'success': 'Succès',
                'warning': 'Avertissement',
                'info': 'Information',
                
                # Patient Portal
                'patient_portal_title': 'Portail Patient',
                'patient_portal_subtitle': 'Accès sécurisé du patient aux dossiers médicaux, rendez-vous et communication',
                'patient_login': 'Connexion Patient',
                'email_address': 'Adresse E-mail',
                'password': 'Mot de Passe',
                'demo_credentials': 'Identifiants de Démonstration',
                'login_successful': 'Connexion réussie! Redirection vers le tableau de bord...',
                'invalid_credentials': 'E-mail ou mot de passe invalide. Veuillez réessayer.',
                'enter_credentials': 'Veuillez saisir à la fois l\'e-mail et le mot de passe.',
                'new_patient_info': 'Nouveau Patient? Contactez votre fournisseur de soins de santé pour configurer l\'accès au portail.',
                'welcome_patient': 'Bienvenue, {name}',
                'medical_record_number': 'NMD: {mrn}',
                
                # Dashboard Metrics
                'upcoming_appointments': 'Rendez-vous à Venir',
                'recent_lab_results': 'Résultats de Laboratoire Récents',
                'unread_messages': 'Messages Non Lus',
                'total_records': 'Dossiers Totaux',
                
                # Portal Sections
                'dashboard': 'Tableau de Bord',
                'appointments': 'Rendez-vous',
                'lab_results': 'Résultats de Laboratoire',
                'messages': 'Messages',
                'profile': 'Profil',
                'health_dashboard': 'Tableau de Bord Santé',
                'my_appointments': 'Mes Rendez-vous',
                'my_profile': 'Mon Profil',
                
                # Actions
                'schedule_appointment': 'Planifier un Rendez-vous',
                'request_prescription_refill': 'Demander un Renouvellement d\'Ordonnance',
                'contact_provider': 'Contacter le Fournisseur',
                'update_contact_info': 'Mettre à Jour les Informations de Contact',
                'change_password': 'Changer le Mot de Passe',
                'download_records': 'Télécharger les Dossiers',
                'mark_as_read': 'Marquer comme Lu',
                'send_message': 'Envoyer un Message',
                
                # Medical Information
                'personal_information': 'Informations Personnelles',
                'medical_information': 'Informations Médicales',
                'name': 'Nom',
                'date_of_birth': 'Date de Naissance',
                'phone': 'Téléphone',
                'emergency_contact': 'Contact d\'Urgence',
                'doctor': 'Docteur',
                'date': 'Date',
                'time': 'Heure',
                'status': 'Statut',
                'notes': 'Notes',
                'test': 'Test',
                'result': 'Résultat',
                'reference': 'Référence',
                'subject': 'Sujet',
                'message': 'Message',
                
                # Clinical Terms
                'creatinine': 'Créatinine',
                'bun': 'BUN',
                'egfr': 'DFGe',
                'protein_urine': 'Protéine (Urine)',
                'blood_pressure': 'Pression Artérielle',
                'kidney_function': 'Fonction Rénale',
                
                # Status Messages
                'no_appointments_found': 'Aucun rendez-vous trouvé.',
                'no_lab_results_found': 'Aucun résultat de laboratoire trouvé.',
                'no_messages_found': 'Aucun message trouvé.',
                'message_sent_successfully': 'Message envoyé avec succès! Vous recevrez une réponse dans 24-48 heures.',
                'fill_subject_message': 'Veuillez remplir à la fois le sujet et le message.',
                'contact_patient_services': 'Veuillez contacter les Services aux Patients au (555) 123-4567 pour mettre à jour vos informations de contact.',
                'password_change_info': 'Les changements de mot de passe peuvent être demandés via les Services aux Patients pour des raisons de sécurité.',
                'records_request_info': 'Les dossiers médicaux peuvent être demandés via les Services aux Patients. Le traitement peut prendre 3-5 jours ouvrables.',
                
                # AI Consultation
                'ai_consultation_title': 'Consultation IA',
                'enter_symptoms': 'Entrez vos symptômes ou préoccupations médicales',
                'get_ai_response': 'Obtenir une Réponse IA',
                'medical_disclaimer': 'Avertissement Médical: Cet assistant IA fournit des informations éducatives uniquement et ne doit pas remplacer les conseils, diagnostics ou traitements médicaux professionnels. Consultez toujours des fournisseurs de soins de santé qualifiés pour les décisions médicales.',
                
                # Risk Assessment
                'risk_assessment_title': 'Évaluation des Risques',
                'patient_age': 'Âge du Patient',
                'serum_creatinine': 'Créatinine Sérique (mg/dL)',
                'blood_pressure_systolic': 'Pression Artérielle Systolique (mmHg)',
                'diabetes': 'Diabète',
                'hypertension': 'Hypertension',
                'calculate_risk': 'Calculer le Risque',
                'risk_level': 'Niveau de Risque',
                'low_risk': 'Risque Faible',
                'moderate_risk': 'Risque Modéré',
                'high_risk': 'Risque Élevé',
                
                # Monitoring
                'real_time_monitoring': 'Surveillance en Temps Réel',
                'active_alerts': 'Alertes Actives',
                'patient_dashboard_monitoring': 'Tableau de Bord Patient',
                'alert_management': 'Gestion des Alertes',
                'simulate_data': 'Simuler des Données',
                'auto_refresh': 'Actualisation Automatique',
                'enable_auto_refresh': 'Activer l\'Actualisation Automatique',
                'refresh_interval': 'Intervalle d\'Actualisation (secondes)',
            }
        }
    
    def set_language(self, language_code: str):
        """Set the current language"""
        if language_code in self.translations:
            self.current_language = language_code
            # Store in session state
            st.session_state.language = language_code
        else:
            st.error(f"Language '{language_code}' not supported")
    
    def get_text(self, key: str, **kwargs) -> str:
        """Get translated text for the given key"""
        # Check session state for language preference
        if 'language' in st.session_state:
            self.current_language = st.session_state.language
        
        try:
            text = self.translations[self.current_language].get(key, key)
            # Format with any provided kwargs
            if kwargs:
                text = text.format(**kwargs)
            return text
        except KeyError:
            # Fallback to English if key not found
            try:
                text = self.translations['en'].get(key, key)
                if kwargs:
                    text = text.format(**kwargs)
                return text
            except:
                return key
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get list of supported languages"""
        return {
            'en': '🇺🇸 English',
            'es': '🇪🇸 Español',
            'fr': '🇫🇷 Français'
        }
    
    def create_language_selector(self):
        """Create a language selector widget"""
        languages = self.get_supported_languages()
        
        # Get current language from session state or default
        current_lang = st.session_state.get('language', 'en')
        
        # Find the index of current language
        lang_codes = list(languages.keys())
        try:
            current_index = lang_codes.index(current_lang)
        except ValueError:
            current_index = 0
        
        selected_lang = st.selectbox(
            "🌐 Language / Idioma / Langue",
            options=lang_codes,
            format_func=lambda x: languages[x],
            index=current_index,
            key="language_selector"
        )
        
        if selected_lang != current_lang:
            self.set_language(selected_lang)
            st.rerun()
        
        return selected_lang

# Global instance
_localization_manager = None

def get_localization_manager() -> LocalizationManager:
    """Get the global localization manager instance"""
    global _localization_manager
    if _localization_manager is None:
        _localization_manager = LocalizationManager()
    return _localization_manager

def t(key: str, **kwargs) -> str:
    """Shorthand function for getting translated text"""
    return get_localization_manager().get_text(key, **kwargs)

def create_language_selector():
    """Shorthand function for creating language selector"""
    return get_localization_manager().create_language_selector()