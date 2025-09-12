import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Calendar, User, Phone, X, Clock, Stethoscope } from 'lucide-react';

interface AppointmentFormProps {
  onClose: () => void;
  onSubmit: (data: any) => void;
  isSubmitting: boolean;
  initialData?: {
    doctor?: string;
    specialty?: string;
  };
}

const AppointmentForm: React.FC<AppointmentFormProps> = ({
  onClose,
  onSubmit,
  isSubmitting,
  initialData = {},
}) => {
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    date: '',
    doctor: initialData.doctor || '',
    specialty: initialData.specialty || '',
    notes: '',
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const validateForm = () => {
    const newErrors: Record<string, string> = {};
    
    if (!formData.name.trim()) newErrors.name = 'Name is required';
    if (!formData.phone.trim()) {
      newErrors.phone = 'Phone number is required';
    } else if (!/^[0-9]{10}$/.test(formData.phone)) {
      newErrors.phone = 'Please enter a valid 10-digit phone number';
    }
    if (!formData.date) newErrors.date = 'Please select a date';
    if (!formData.doctor) newErrors.doctor = 'Please select a doctor';
    if (!formData.specialty) newErrors.specialty = 'Please select a specialty';
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validateForm()) {
      onSubmit(formData);
    }
  };

  // Set minimum date to today
  const today = new Date().toISOString().split('T')[0];
  const maxDate = new Date();
  maxDate.setMonth(maxDate.getMonth() + 3);
  const maxDateStr = maxDate.toISOString().split('T')[0];

  const specialties = [
    'General Medicine',
    'Cardiology',
    'Dermatology',
    'Neurology',
    'Orthopedics',
    'Pediatrics',
    'Ophthalmology',
    'ENT',
  ];

  const doctors = {
    'General Medicine': ['Dr. Smith', 'Dr. Johnson', 'Dr. Williams'],
    'Cardiology': ['Dr. Brown', 'Dr. Davis'],
    'Dermatology': ['Dr. Miller', 'Dr. Wilson'],
    'Neurology': ['Dr. Moore', 'Dr. Taylor'],
    'Orthopedics': ['Dr. Anderson', 'Dr. Thomas'],
    'Pediatrics': ['Dr. Jackson', 'Dr. White'],
    'Ophthalmology': ['Dr. Harris', 'Dr. Martin'],
    'ENT': ['Dr. Thompson', 'Dr. Garcia'],
  };

  const availableDoctors = formData.specialty ? doctors[formData.specialty as keyof typeof doctors] || [] : [];

  return (
    <motion.div 
      className="bg-white rounded-lg shadow-lg p-6 w-full max-w-md mx-auto"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
    >
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-xl font-semibold text-gray-800 flex items-center">
          <Calendar className="mr-2 h-5 w-5 text-blue-600" />
          Book an Appointment
        </h3>
        <button 
          onClick={onClose}
          className="text-gray-500 hover:text-gray-700"
          aria-label="Close form"
        >
          <X className="h-5 w-5" />
        </button>
      </div>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
            Full Name <span className="text-red-500">*</span>
          </label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <User className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              className={`block w-full pl-10 pr-3 py-2 border ${errors.name ? 'border-red-300' : 'border-gray-300'} rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500`}
              placeholder="John Doe"
            />
          </div>
          {errors.name && <p className="mt-1 text-sm text-red-600">{errors.name}</p>}
        </div>

        <div>
          <label htmlFor="phone" className="block text-sm font-medium text-gray-700 mb-1">
            Phone Number <span className="text-red-500">*</span>
          </label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Phone className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="tel"
              id="phone"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              className={`block w-full pl-10 pr-3 py-2 border ${errors.phone ? 'border-red-300' : 'border-gray-300'} rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500`}
              placeholder="123-456-7890"
            />
          </div>
          {errors.phone && <p className="mt-1 text-sm text-red-600">{errors.phone}</p>}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label htmlFor="specialty" className="block text-sm font-medium text-gray-700 mb-1">
              Specialty <span className="text-red-500">*</span>
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Stethoscope className="h-5 w-5 text-gray-400" />
              </div>
              <select
                id="specialty"
                name="specialty"
                value={formData.specialty}
                onChange={handleChange}
                className={`block w-full pl-10 pr-3 py-2 border ${errors.specialty ? 'border-red-300' : 'border-gray-300'} rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 appearance-none bg-white`}
              >
                <option value="">Select Specialty</option>
                {specialties.map(specialty => (
                  <option key={specialty} value={specialty}>
                    {specialty}
                  </option>
                ))}
              </select>
            </div>
            {errors.specialty && <p className="mt-1 text-sm text-red-600">{errors.specialty}</p>}
          </div>

          <div>
            <label htmlFor="doctor" className="block text-sm font-medium text-gray-700 mb-1">
              Doctor <span className="text-red-500">*</span>
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <User className="h-5 w-5 text-gray-400" />
              </div>
              <select
                id="doctor"
                name="doctor"
                value={formData.doctor}
                onChange={handleChange}
                disabled={!formData.specialty}
                className={`block w-full pl-10 pr-3 py-2 border ${errors.doctor ? 'border-red-300' : 'border-gray-300'} rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 appearance-none ${!formData.specialty ? 'bg-gray-100' : 'bg-white'}`}
              >
                <option value="">Select Doctor</option>
                {availableDoctors.map(doctor => (
                  <option key={doctor} value={doctor}>
                    {doctor}
                  </option>
                ))}
              </select>
            </div>
            {errors.doctor && <p className="mt-1 text-sm text-red-600">{errors.doctor}</p>}
          </div>
        </div>

        <div>
          <label htmlFor="date" className="block text-sm font-medium text-gray-700 mb-1">
            Preferred Date <span className="text-red-500">*</span>
          </label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Clock className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="date"
              id="date"
              name="date"
              value={formData.date}
              min={today}
              max={maxDateStr}
              onChange={handleChange}
              className={`block w-full pl-10 pr-3 py-2 border ${errors.date ? 'border-red-300' : 'border-gray-300'} rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500`}
            />
          </div>
          {errors.date && <p className="mt-1 text-sm text-red-600">{errors.date}</p>}
        </div>

        <div>
          <label htmlFor="notes" className="block text-sm font-medium text-gray-700 mb-1">
            Additional Notes (Optional)
          </label>
          <textarea
            id="notes"
            name="notes"
            rows={3}
            value={formData.notes}
            onChange={handleChange}
            className="block w-full border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            placeholder="Any specific concerns or questions you'd like to discuss?"
          />
        </div>

        <div className="pt-2">
          <button
            type="submit"
            disabled={isSubmitting}
            className={`w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white ${isSubmitting ? 'bg-blue-400' : 'bg-blue-600 hover:bg-blue-700'} focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500`}
          >
            {isSubmitting ? (
              <>
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Booking...
              </>
            ) : 'Book Appointment'}
          </button>
        </div>
      </form>
    </motion.div>
  );
};

export default AppointmentForm;
