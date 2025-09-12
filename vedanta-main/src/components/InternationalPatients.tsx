import React, { useState } from 'react';
import { Globe, Plane, CreditCard, Languages, Shield, MapPin, Phone, Mail, Users, Calendar } from 'lucide-react';
import { motion } from 'framer-motion';

const InternationalPatients = () => {
  const [selectedCountry, setSelectedCountry] = useState('');

  const services = [
    {
      icon: Plane,
      title: 'Travel Assistance',
      description: 'Visa support, airport pickup, accommodation arrangements',
      features: ['Medical Visa Support', 'Airport Transfer', 'Hotel Booking', 'Local Transportation']
    },
    {
      icon: Languages,
      title: 'Language Support',
      description: 'Professional interpreters for seamless communication',
      features: ['English', 'Arabic', 'Russian', 'French', 'German', 'Spanish']
    },
    {
      icon: CreditCard,
      title: 'Payment Options',
      description: 'Flexible payment methods and insurance coordination',
      features: ['International Cards', 'Wire Transfer', 'Insurance Claims', 'EMI Options']
    },
    {
      icon: Shield,
      title: 'Medical Tourism',
      description: 'Complete healthcare packages with tourism options',
      features: ['Treatment Packages', 'Recovery Tourism', 'Family Accommodation', 'Sightseeing']
    }
  ];

  const popularTreatments = [
    { name: 'Cardiac Surgery', price: '$8,000 - $15,000', duration: '7-10 days' },
    { name: 'Orthopedic Surgery', price: '$5,000 - $12,000', duration: '5-8 days' },
    { name: 'Cancer Treatment', price: '$10,000 - $25,000', duration: '2-4 weeks' },
    { name: 'Neurosurgery', price: '$12,000 - $20,000', duration: '10-14 days' },
    { name: 'Organ Transplant', price: '$20,000 - $40,000', duration: '3-6 weeks' },
    { name: 'Cosmetic Surgery', price: '$2,000 - $8,000', duration: '3-5 days' }
  ];

  const countries = [
    'United States', 'United Kingdom', 'Canada', 'Australia', 'Germany', 
    'France', 'UAE', 'Saudi Arabia', 'Bangladesh', 'Sri Lanka', 'Nepal', 'Myanmar'
  ];

  const testimonials = [
    {
      name: 'John Smith',
      country: 'United States',
      treatment: 'Cardiac Surgery',
      rating: 5,
      comment: 'Excellent care and very affordable compared to US prices. The staff was incredibly helpful throughout my stay.',
      image: 'https://images.pexels.com/photos/1040881/pexels-photo-1040881.jpeg?auto=compress&cs=tinysrgb&w=400'
    },
    {
      name: 'Sarah Johnson',
      country: 'United Kingdom',
      treatment: 'Orthopedic Surgery',
      rating: 5,
      comment: 'World-class treatment at a fraction of the cost. The international patient coordinator made everything seamless.',
      image: 'https://images.pexels.com/photos/774909/pexels-photo-774909.jpeg?auto=compress&cs=tinysrgb&w=400'
    }
  ];

  return (
    <div className="bg-white rounded-2xl shadow-lg p-6">
      <div className="text-center mb-8">
        <div className="flex items-center justify-center space-x-2 mb-4">
          <Globe className="h-8 w-8 text-blue-600" />
          <h2 className="text-3xl font-bold text-gray-900">International Patients</h2>
        </div>
        <p className="text-gray-600 max-w-2xl mx-auto">
          World-class healthcare at affordable prices. We welcome patients from around the globe 
          with comprehensive support services and personalized care.
        </p>
      </div>

      {/* Key Statistics */}
      <div className="grid md:grid-cols-4 gap-6 mb-8">
        <motion.div 
          whileHover={{ scale: 1.05 }}
          className="text-center p-4 bg-blue-50 rounded-xl border border-blue-200"
        >
          <Users className="h-8 w-8 text-blue-600 mx-auto mb-2" />
          <div className="text-2xl font-bold text-blue-600">2,500+</div>
          <div className="text-sm text-gray-600">International Patients</div>
        </motion.div>
        
        <motion.div 
          whileHover={{ scale: 1.05 }}
          className="text-center p-4 bg-green-50 rounded-xl border border-green-200"
        >
          <Globe className="h-8 w-8 text-green-600 mx-auto mb-2" />
          <div className="text-2xl font-bold text-green-600">45+</div>
          <div className="text-sm text-gray-600">Countries Served</div>
        </motion.div>
        
        <motion.div 
          whileHover={{ scale: 1.05 }}
          className="text-center p-4 bg-purple-50 rounded-xl border border-purple-200"
        >
          <Languages className="h-8 w-8 text-purple-600 mx-auto mb-2" />
          <div className="text-2xl font-bold text-purple-600">12</div>
          <div className="text-sm text-gray-600">Languages Supported</div>
        </motion.div>
        
        <motion.div 
          whileHover={{ scale: 1.05 }}
          className="text-center p-4 bg-orange-50 rounded-xl border border-orange-200"
        >
          <Shield className="h-8 w-8 text-orange-600 mx-auto mb-2" />
          <div className="text-2xl font-bold text-orange-600">98.5%</div>
          <div className="text-sm text-gray-600">Satisfaction Rate</div>
        </motion.div>
      </div>

      {/* Services */}
      <div className="mb-8">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">Our International Services</h3>
        <div className="grid md:grid-cols-2 gap-6">
          {services.map((service, index) => (
            <motion.div
              key={index}
              whileHover={{ y: -2 }}
              className="bg-gray-50 rounded-lg p-6"
            >
              <div className="flex items-start space-x-4">
                <div className="bg-blue-100 p-3 rounded-lg">
                  <service.icon className="h-6 w-6 text-blue-600" />
                </div>
                <div>
                  <h4 className="font-semibold text-gray-900 mb-2">{service.title}</h4>
                  <p className="text-gray-600 text-sm mb-3">{service.description}</p>
                  <div className="flex flex-wrap gap-2">
                    {service.features.map((feature, i) => (
                      <span key={i} className="bg-blue-100 text-blue-700 px-2 py-1 rounded text-xs">
                        {feature}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Popular Treatments */}
      <div className="mb-8">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">Popular Treatment Packages</h3>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {popularTreatments.map((treatment, index) => (
            <div key={index} className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <h4 className="font-semibold text-gray-900 mb-2">{treatment.name}</h4>
              <div className="space-y-1 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">Cost:</span>
                  <span className="font-medium text-green-600">{treatment.price}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Duration:</span>
                  <span className="text-gray-900">{treatment.duration}</span>
                </div>
              </div>
              <button className="w-full mt-3 bg-blue-600 text-white py-2 rounded hover:bg-blue-700 text-sm">
                Get Quote
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* Contact Form */}
      <div className="grid lg:grid-cols-2 gap-8 mb-8">
        <div>
          <h3 className="text-xl font-semibold text-gray-900 mb-4">Get Started</h3>
          <form className="space-y-4">
            <div className="grid md:grid-cols-2 gap-4">
              <input
                type="text"
                placeholder="Full Name"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
              />
              <input
                type="email"
                placeholder="Email Address"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
              />
            </div>
            <div className="grid md:grid-cols-2 gap-4">
              <input
                type="tel"
                placeholder="Phone Number"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
              />
              <select
                value={selectedCountry}
                onChange={(e) => setSelectedCountry(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
              >
                <option value="">Select Country</option>
                {countries.map(country => (
                  <option key={country} value={country}>{country}</option>
                ))}
              </select>
            </div>
            <select className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none">
              <option value="">Treatment Required</option>
              {popularTreatments.map(treatment => (
                <option key={treatment.name} value={treatment.name}>{treatment.name}</option>
              ))}
            </select>
            <textarea
              placeholder="Medical History & Requirements"
              rows={4}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none resize-none"
            ></textarea>
            <button className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 font-semibold">
              Submit Inquiry
            </button>
          </form>
        </div>

        <div>
          <h3 className="text-xl font-semibold text-gray-900 mb-4">Contact Information</h3>
          <div className="space-y-4">
            <div className="flex items-center space-x-3">
              <Phone className="h-5 w-5 text-blue-600" />
              <div>
                <div className="font-medium">International Helpline</div>
                <div className="text-blue-600">+91-863-234-5678</div>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <Mail className="h-5 w-5 text-blue-600" />
              <div>
                <div className="font-medium">Email Support</div>
                <div className="text-blue-600">international@vedantahospitals.in</div>
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <MapPin className="h-5 w-5 text-blue-600 mt-1" />
              <div>
                <div className="font-medium">Hospital Address</div>
                <div className="text-gray-600">Vedanta Hospital, Brodipet, Near Railway Station, Guntur - 522002, AP</div>
              </div>
            </div>
          </div>

          <div className="mt-6 p-4 bg-green-50 rounded-lg">
            <h4 className="font-semibold text-green-800 mb-2">Why Choose Vedanta Hospitals?</h4>
            <ul className="text-sm text-green-700 space-y-1">
              <li>• 60-80% cost savings compared to Western countries</li>
              <li>• JCI accredited quality standards</li>
              <li>• English-speaking medical staff</li>
              <li>• No waiting lists for most procedures</li>
              <li>• Complete travel and accommodation support</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Patient Testimonials */}
      <div>
        <h3 className="text-xl font-semibold text-gray-900 mb-4">Patient Testimonials</h3>
        <div className="grid md:grid-cols-2 gap-6">
          {testimonials.map((testimonial, index) => (
            <div key={index} className="bg-gray-50 rounded-lg p-6">
              <div className="flex items-center space-x-4 mb-4">
                <img
                  src={testimonial.image}
                  alt={testimonial.name}
                  className="w-12 h-12 rounded-full object-cover"
                />
                <div>
                  <h4 className="font-semibold text-gray-900">{testimonial.name}</h4>
                  <p className="text-sm text-gray-600">{testimonial.country} • {testimonial.treatment}</p>
                </div>
              </div>
              <p className="text-gray-700 text-sm italic">"{testimonial.comment}"</p>
              <div className="flex items-center mt-3">
                {[...Array(testimonial.rating)].map((_, i) => (
                  <span key={i} className="text-yellow-400">★</span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default InternationalPatients;