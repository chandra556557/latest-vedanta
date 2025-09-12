import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navigation from './components/Navigation';
import Footer from './components/Footer';
import HomePage from './pages/HomePage';
import AboutPage from './pages/AboutPage';
import ServicesPage from './pages/ServicesPage';
import DoctorsPage from './pages/DoctorsPage';
import AIServicesPage from './pages/AIServicesPage';
import ContactPage from './pages/ContactPage';
import AppointmentPage from './pages/AppointmentPage';
import DoctorProfilePage from './pages/DoctorProfilePage';
import Testimonials from './components/Testimonials';
import News from './components/News';
import PackagesPage from './pages/PackagesPage';
import AIHealthDashboard from './components/AIHealthDashboard';
import AISymptomChecker from './components/AISymptomChecker';
import PatientLoginPage from './pages/PatientLoginPage';
import BlogPage from './pages/BlogPage';
import SmartAIAssistant from './components/SmartAIAssistant';
import FitnessAssistantPage from './pages/FitnessAssistantPage';
import FitnessAssistantWidget from './components/FitnessAssistantWidget';
import WhatsAppFloatButton from './components/WhatsAppFloatButton';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-white" itemScope itemType="https://schema.org/WebSite">
        <meta itemProp="url" content="https://vedantahospitals.in" />
        <meta itemProp="name" content="Vedanta Hospital - Best Multi-Specialty Hospital in Guntur" />
        <Navigation />
        <main role="main">
          <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/services" element={<ServicesPage />} />
          <Route path="/services/:specialty" element={<ServicesPage />} />
          <Route path="/doctors" element={<DoctorsPage />} />
          <Route path="/packages" element={<PackagesPage />} />
          <Route path="/ai-services" element={<AIServicesPage />} />
          <Route path="/ai-services/chatbot" element={<AIServicesPage />} />
          <Route path="/ai-services/symptom-checker" element={<AISymptomChecker />} />
          <Route path="/ai-services/dashboard" element={<AIHealthDashboard />} />
          <Route path="/ai-services/fitness-assistant" element={<FitnessAssistantPage />} />
          <Route path="/testimonials" element={<Testimonials />} />
          <Route path="/blog" element={<BlogPage />} />
          <Route path="/news" element={<News />} />
          <Route path="/contact" element={<ContactPage />} />
          <Route path="/appointment" element={<AppointmentPage />} />
          <Route path="/doctor/:doctorName" element={<DoctorProfilePage />} />
          <Route path="/patient/login" element={<PatientLoginPage />} />
          <Route path="/forgot-password" element={<PatientLoginPage />} />
          <Route path="/patient/register" element={<PatientLoginPage />} />
          {/* Advanced features routes have been removed as per requirements */}
        </Routes>
        </main>
        <Footer />
        <SmartAIAssistant />
        {/* Floating Vedanta Fitness Assistant */}
        <FitnessAssistantWidget />
        <WhatsAppFloatButton />
      </div>
    </Router>
  );
}

export default App;