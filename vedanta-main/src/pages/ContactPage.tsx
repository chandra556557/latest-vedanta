import React, { useState } from 'react';
import { MapPin, Phone, Mail, Clock, Send, MessageCircle, Calendar, Users } from 'lucide-react';
import { motion } from 'framer-motion';

const ContactPage = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    subject: '',
    message: '',
    department: ''
  });

  const locations = [
    {
      city: 'Mumbai',
      address: 'Plot No. 123, Sector 15, CBD Belapur, Navi Mumbai - 400614',
      phone: '+91-22-2XXX-XXXX',
      email: 'mumbai@vedantahospital.com',
      hours: '24/7 Emergency Services | OPD: 9:00 AM - 9:00 PM',
      image: 'https://images.pexels.com/photos/263402/pexels-photo-263402.jpeg?auto=compress&cs=tinysrgb&w=600'
    }
  ];

  const departments = [
    'General Inquiry',
    'Book Appointment',
    'Emergency Services',
    'Patient Care',
    'Cardiology',
    'Orthopedics',
    'Neurology',
    'Pediatrics',
    'Gynecology',
    'General Surgery',
    'Insurance & Billing',
    'International Patients',
    'Feedback & Suggestions'
  ];

  const quickContacts = [
    {
      icon: Phone,
      title: '24/7 Emergency',
      info: '+91-863-234-5678',
      description: 'For medical emergencies'
    },
    {
      icon: Calendar,
      title: 'Appointments',
      info: '+91-863-234-5679',
      description: 'Book your appointment'
    },
    {
      icon: MessageCircle,
      title: 'Patient Care',
      info: 'info@vedantahospitals.in',
      description: 'General inquiries'
    },
    {
      icon: Users,
      title: 'International',
      info: 'international@vedantahospitals.in',
      description: 'For overseas patients'
    }
  ];

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle form submission
    console.log('Form submitted:', formData);
  };

  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-sky-50 to-emerald-50 py-20">
        <div className="container mx-auto px-4">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center mb-16"
          >
            <h1 className="text-5xl lg:text-6xl font-bold text-gray-900 mb-6">
              Contact <span className="text-sky-600">Vedanta Hospital</span>
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
              We're here to help you with all your healthcare needs. Reach out to us through 
              any of the channels below or visit one of our locations.
            </p>
          </motion.div>

          {/* Quick Contacts */}
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-6xl mx-auto">
            {quickContacts.map((contact, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="bg-white rounded-xl p-6 shadow-lg text-center hover:shadow-xl transition-shadow"
              >
                <contact.icon className="h-8 w-8 text-sky-600 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-gray-900 mb-2">{contact.title}</h3>
                <p className="text-sky-600 font-medium mb-1">{contact.info}</p>
                <p className="text-gray-600 text-sm">{contact.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Contact Form & Info */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="grid lg:grid-cols-2 gap-12">
            {/* Contact Form */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
            >
              <h2 className="text-3xl font-bold text-gray-900 mb-8">Send us a Message</h2>
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid md:grid-cols-2 gap-6">
                  <input
                    type="text"
                    name="name"
                    placeholder="Full Name *"
                    value={formData.name}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500 outline-none"
                    required
                  />
                  <input
                    type="email"
                    name="email"
                    placeholder="Email Address *"
                    value={formData.email}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500 outline-none"
                    required
                  />
                </div>
                
                <div className="grid md:grid-cols-2 gap-6">
                  <input
                    type="tel"
                    name="phone"
                    placeholder="Phone Number *"
                    value={formData.phone}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500 outline-none"
                    required
                  />
                  <select
                    name="department"
                    value={formData.department}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500 outline-none"
                    required
                  >
                    <option value="">Select Department *</option>
                    {departments.map((dept, index) => (
                      <option key={index} value={dept}>{dept}</option>
                    ))}
                  </select>
                </div>
                
                <input
                  type="text"
                  name="subject"
                  placeholder="Subject *"
                  value={formData.subject}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500 outline-none"
                  required
                />
                
                <textarea
                  name="message"
                  placeholder="Your Message *"
                  rows={6}
                  value={formData.message}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500 outline-none resize-none"
                  required
                ></textarea>
                
                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  type="submit"
                  className="w-full bg-sky-600 text-white py-3 rounded-lg hover:bg-sky-700 transition-colors font-semibold flex items-center justify-center space-x-2"
                >
                  <Send className="h-5 w-5" />
                  <span>Send Message</span>
                </motion.button>
              </form>
            </motion.div>

            {/* Contact Information */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
            >
              <h2 className="text-3xl font-bold text-gray-900 mb-8">Get in Touch</h2>
              
              <div className="space-y-6 mb-8">
                <div className="flex items-start space-x-4">
                  <MapPin className="h-6 w-6 text-sky-600 mt-1" />
                  <div>
                    <h3 className="font-semibold text-gray-900 mb-1">Our Locations</h3>
                    <p className="text-gray-600">Multiple locations across India for your convenience</p>
                  </div>
                </div>
                
                <div className="flex items-start space-x-4">
                  <Phone className="h-6 w-6 text-sky-600 mt-1" />
                  <div>
                    <h3 className="font-semibold text-gray-900 mb-1">24/7 Support</h3>
                    <p className="text-gray-600">Emergency helpline always available</p>
                  </div>
                </div>
                
                <div className="flex items-start space-x-4">
                  <Mail className="h-6 w-6 text-sky-600 mt-1" />
                  <div>
                    <h3 className="font-semibold text-gray-900 mb-1">Email Support</h3>
                    <p className="text-gray-600">Quick response to all inquiries</p>
                  </div>
                </div>
                
                <div className="flex items-start space-x-4">
                  <Clock className="h-6 w-6 text-sky-600 mt-1" />
                  <div>
                    <h3 className="font-semibold text-gray-900 mb-1">Response Time</h3>
                    <p className="text-gray-600">We respond within 24 hours</p>
                  </div>
                </div>
              </div>

              {/* Emergency Contact */}
              <div className="bg-red-50 border border-red-200 rounded-xl p-6">
                <h3 className="text-lg font-semibold text-red-800 mb-2">Emergency Contact</h3>
                <p className="text-red-700 mb-3">For medical emergencies, call immediately:</p>
                <p className="text-2xl font-bold text-red-600">+91-XXX-XXX-XXXX</p>
                <p className="text-red-600 text-sm mt-2">Available 24/7 for life-threatening situations</p>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Locations */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-gray-900 text-center mb-16">Our Locations</h2>
          
          <div className="grid lg:grid-cols-3 gap-8">
            {locations.map((location, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="bg-white rounded-2xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow"
              >
                <img
                  src={location.image}
                  alt={`${location.city} location`}
                  className="w-full h-48 object-cover"
                />
                <div className="p-6">
                  <h3 className="text-xl font-bold text-gray-900 mb-4">{location.city}</h3>
                  
                  <div className="space-y-3 text-sm">
                    <div className="flex items-start space-x-2">
                      <MapPin className="h-4 w-4 text-gray-500 mt-1" />
                      <span className="text-gray-600">{location.address}</span>
                    </div>
                    
                    <div className="flex items-center space-x-2">
                      <Phone className="h-4 w-4 text-gray-500" />
                      <span className="text-gray-600">{location.phone}</span>
                    </div>
                    
                    <div className="flex items-center space-x-2">
                      <Mail className="h-4 w-4 text-gray-500" />
                      <span className="text-gray-600">{location.email}</span>
                    </div>
                    
                    <div className="flex items-start space-x-2">
                      <Clock className="h-4 w-4 text-gray-500 mt-1" />
                      <span className="text-gray-600">{location.hours}</span>
                    </div>
                  </div>
                  
                  <button className="w-full mt-6 bg-sky-600 text-white py-2 rounded-lg hover:bg-sky-700 transition-colors font-medium">
                    Get Directions
                  </button>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
};

export default ContactPage;