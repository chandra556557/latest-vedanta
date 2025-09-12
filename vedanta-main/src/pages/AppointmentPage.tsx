import React, { useEffect, useMemo, useState } from 'react';
import { useLocation, Link, useNavigate } from 'react-router-dom';
import { Calendar, User, Phone, Stethoscope, ArrowLeft, CheckCircle, XCircle } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { doctors } from '../data/doctorsList';

function useQuery() {
  const { search } = useLocation();
  return useMemo(() => new URLSearchParams(search), [search]);
}

interface FormErrors {
  name?: string;
  phone?: string;
  date?: string;
}

const AppointmentPage: React.FC = () => {
  const query = useQuery();
  const navigate = useNavigate();
  const prefillDoctor = query.get('doctor') || '';
  const prefillSpecialty = query.get('specialty') || '';
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState<{ success: boolean; message: string } | null>(null);
  const [errors, setErrors] = useState<FormErrors>({});

  const [form, setForm] = useState({
    doctor: prefillDoctor,
    specialty: prefillSpecialty,
    name: '',
    phone: '',
    date: '',
    notes: ''
  });

  // Derive specialties list from doctors data
  const specialtiesFromData = useMemo(() => Array.from(new Set(doctors.map(d => d.specialty))), []);

  // If a doctor was prefilled but specialty was not, auto-fill specialty from the doctor profile
  useEffect(() => {
    if (prefillDoctor && !prefillSpecialty) {
      const doc = doctors.find(d => d.name === prefillDoctor);
      if (doc) {
        setForm(prev => ({ ...prev, specialty: doc.specialty }));
      }
    }
  }, [prefillDoctor, prefillSpecialty]);

  // Set minimum date to today
  const today = new Date().toISOString().split('T')[0];
  const maxDate = new Date();
  maxDate.setMonth(maxDate.getMonth() + 3);
  const maxDateStr = maxDate.toISOString().split('T')[0];

  const validateForm = (): boolean => {
    const newErrors: FormErrors = {};
    
    if (!form.name.trim()) {
      newErrors.name = 'Name is required';
    }
    
    if (!form.phone.trim()) {
      newErrors.phone = 'Phone number is required';
    } else if (!/^[0-9]{10}$/.test(form.phone)) {
      newErrors.phone = 'Please enter a valid 10-digit phone number';
    }
    
    if (!form.date) {
      newErrors.date = 'Please select a date';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const onChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    if (name === 'doctor') {
      // When selecting a doctor, also set the specialty to match
      const doc = doctors.find(d => d.name === value);
      setForm((f) => ({ ...f, doctor: value, specialty: doc ? doc.specialty : f.specialty }));
    } else {
      setForm((f) => ({ ...f, [name]: value }));
    }
    
    // Clear error when user starts typing
    if (errors[name as keyof FormErrors]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[name as keyof FormErrors];
        return newErrors;
      });
    }
  };

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    setIsSubmitting(true);
    setSubmitStatus(null);
    
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // In a real app, you would make an API call here:
      // const response = await fetch('/api/appointments', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify(form)
      // });
      // const data = await response.json();
      
      setSubmitStatus({
        success: true,
        message: 'Your appointment request has been submitted successfully! We will contact you shortly to confirm.'
      });
      
      // Reset form
      setForm({
        doctor: '',
        specialty: '',
        name: '',
        phone: '',
        date: '',
        notes: ''
      });
      
      // Redirect to home after 3 seconds
      setTimeout(() => {
        navigate('/');
      }, 3000);
      
    } catch (error) {
      console.error('Error submitting appointment:', error);
      setSubmitStatus({
        success: false,
        message: 'There was an error submitting your appointment. Please try again later.'
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-white">
      <section className="bg-gradient-to-br from-sky-50 to-emerald-50 py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-3xl mx-auto">
            <div className="flex items-center gap-3 mb-6">
              <Link to="/doctors" className="inline-flex items-center text-sky-700 hover:underline">
                <ArrowLeft className="h-4 w-4 mr-1" /> Back to Doctors
              </Link>
            </div>
            <h1 className="text-4xl lg:text-5xl font-bold text-gray-900 mb-3">Book Appointment</h1>
            <p className="text-gray-600">
              Select your preferred date and share your details. If you came from a doctor profile, their info is pre-filled below.
            </p>
          </div>
        </div>
      </section>

      <AnimatePresence>
        {submitStatus && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className={`fixed top-6 left-1/2 transform -translate-x-1/2 z-50 max-w-md w-full px-6`}
          >
            <div className={`p-4 rounded-lg shadow-lg ${submitStatus.success ? 'bg-emerald-50 border border-emerald-200' : 'bg-red-50 border border-red-200'}`}>
              <div className="flex items-start">
                <div className={`flex-shrink-0 ${submitStatus.success ? 'text-emerald-500' : 'text-red-500'}`}>
                  {submitStatus.success ? (
                    <CheckCircle className="h-6 w-6" />
                  ) : (
                    <XCircle className="h-6 w-6" />
                  )}
                </div>
                <div className="ml-3">
                  <p className={`text-sm font-medium ${submitStatus.success ? 'text-emerald-800' : 'text-red-800'}`}>
                    {submitStatus.message}
                  </p>
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <section className="py-12">
        <div className="container mx-auto px-4">
          <form onSubmit={onSubmit} className="max-w-3xl mx-auto bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Doctor</label>
                <div className="relative">
                  <Stethoscope className="h-5 w-5 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
                  <select
                    name="doctor"
                    value={form.doctor}
                    onChange={onChange}
                    className="w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500 outline-none appearance-none bg-white"
                  >
                    <option value="">Select a doctor (optional)</option>
                    {doctors.map(d => (
                      <option key={d.name} value={d.name}>{`${d.name} (${d.specialty})`}</option>
                    ))}
                  </select>
                  <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
                    <svg className="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                      <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
                    </svg>
                  </div>
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Specialty</label>
                <div className="relative">
                  <select
                    name="specialty"
                    value={form.specialty}
                    onChange={onChange}
                    className="w-full pl-3 pr-10 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500 outline-none appearance-none bg-white"
                  >
                    <option value="">Select a specialty</option>
                    {specialtiesFromData.map(s => (
                      <option key={s} value={s}>{s}</option>
                    ))}
                  </select>
                  <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
                    <svg className="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                      <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
                    </svg>
                  </div>
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Your Name</label>
                <div className="relative">
                  <User className="h-5 w-5 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
                  <input
                    name="name"
                    value={form.name}
                    onChange={onChange}
                    placeholder="Full name"
                    className={`w-full pl-10 pr-3 py-3 border ${errors.name ? 'border-red-500' : 'border-gray-300'} rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500 outline-none`}
                  />
                </div>
                {errors.name && <p className="mt-1 text-sm text-red-600">{errors.name}</p>}
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Phone</label>
                <div className="relative">
                  <Phone className="h-5 w-5 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
                  <input
                    name="phone"
                    type="tel"
                    value={form.phone}
                    onChange={onChange}
                    placeholder="Mobile number (10 digits)"
                    className={`w-full pl-10 pr-3 py-3 border ${errors.phone ? 'border-red-500' : 'border-gray-300'} rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500 outline-none`}
                    maxLength={10}
                  />
                </div>
                {errors.phone && <p className="mt-1 text-sm text-red-600">{errors.phone}</p>}
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Preferred Date</label>
                <div className="relative">
                  <Calendar className="h-5 w-5 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
                  <input
                    type="date"
                    name="date"
                    value={form.date}
                    onChange={onChange}
                    min={today}
                    max={maxDateStr}
                    className={`w-full pl-10 pr-3 py-3 border ${errors.date ? 'border-red-500' : 'border-gray-300'} rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500 outline-none`}
                  />
                </div>
                {errors.date && <p className="mt-1 text-sm text-red-600">{errors.date}</p>}
                <p className="mt-1 text-xs text-gray-500">Available up to 3 months in advance</p>
              </div>
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-1">Notes (optional)</label>
                <textarea
                  name="notes"
                  value={form.notes}
                  onChange={onChange}
                  placeholder="Briefly describe your concern"
                  className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500 outline-none min-h-[100px]"
                />
              </div>
            </div>

            <div className="mt-6 flex flex-col sm:flex-row gap-3">
              <button
                type="submit"
                disabled={isSubmitting}
                className={`flex items-center justify-center gap-2 bg-emerald-600 text-white px-6 py-3 rounded-lg hover:bg-emerald-700 transition-colors font-semibold ${isSubmitting ? 'opacity-70 cursor-not-allowed' : ''}`}
              >
                {isSubmitting ? (
                  <>
                    <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Processing...
                  </>
                ) : (
                  'Submit Request'
                )}
              </button>
              <Link 
                to="/doctors" 
                className="text-center border border-gray-300 text-gray-700 px-6 py-3 rounded-lg hover:bg-gray-50 transition-colors font-medium"
              >
                Cancel
              </Link>
            </div>
          </form>
        </div>
      </section>
    </div>
  );
};

export default AppointmentPage;
