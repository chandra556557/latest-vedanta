import React, { useState, useEffect } from 'react';
import { Phone, MapPin, Clock, Ambulance, Heart, AlertTriangle, Navigation, Shield, Activity } from 'lucide-react';
import { motion } from 'framer-motion';

const EmergencyServices = () => {
  const [emergencyStats, setEmergencyStats] = useState({
    responseTime: '8 mins',
    ambulancesActive: 12,
    emergencyCases: 247,
    successRate: 98.7
  });

  const emergencyTypes = [
    {
      icon: Heart,
      title: 'Cardiac Emergency',
      description: 'Heart attack, chest pain, cardiac arrest',
      responseTime: '5-8 mins',
      color: 'text-red-600',
      bgColor: 'bg-red-50'
    },
    {
      icon: Brain,
      title: 'Stroke Emergency',
      description: 'Sudden weakness, speech problems, confusion',
      responseTime: '6-10 mins',
      color: 'text-purple-600',
      bgColor: 'bg-purple-50'
    },
    {
      icon: AlertTriangle,
      title: 'Trauma Emergency',
      description: 'Accidents, injuries, severe bleeding',
      responseTime: '8-12 mins',
      color: 'text-orange-600',
      bgColor: 'bg-orange-50'
    },
    {
      icon: Activity,
      title: 'Medical Emergency',
      description: 'Severe pain, breathing difficulty, poisoning',
      responseTime: '10-15 mins',
      color: 'text-blue-600',
      bgColor: 'bg-blue-50'
    }
  ];

  const emergencyContacts = [
    { type: 'Emergency Helpline', number: '+91-863-234-5678', available: '24/7' },
    { type: 'Ambulance Service', number: '+91-863-234-5679', available: '24/7' },
    { type: 'Trauma Center', number: '+91-863-234-5680', available: '24/7' },
    { type: 'Poison Control', number: '+91-863-234-5681', available: '24/7' }
  ];

  const ambulanceFeatures = [
    'Advanced Life Support (ALS)',
    'Cardiac Monitor & Defibrillator',
    'Ventilator Support',
    'Emergency Medications',
    'GPS Tracking',
    'Trained Paramedics',
    'Direct Hospital Communication',
    'Real-time Patient Monitoring'
  ];

  // Simulate real-time updates
  useEffect(() => {
    const interval = setInterval(() => {
      setEmergencyStats(prev => ({
        responseTime: `${Math.floor(Math.random() * 5) + 6} mins`,
        ambulancesActive: Math.floor(Math.random() * 5) + 10,
        emergencyCases: prev.emergencyCases + Math.floor(Math.random() * 3),
        successRate: Math.min(99.9, prev.successRate + (Math.random() - 0.5) * 0.1)
      }));
    }, 10000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="bg-white rounded-2xl shadow-lg p-6">
      <div className="text-center mb-8">
        <div className="flex items-center justify-center space-x-2 mb-4">
          <div className="bg-red-600 p-3 rounded-full">
            <Ambulance className="h-8 w-8 text-white" />
          </div>
          <h2 className="text-3xl font-bold text-gray-900">Emergency Services</h2>
        </div>
        <p className="text-gray-600 max-w-2xl mx-auto">
          24/7 emergency medical services with rapid response ambulances and 
          specialized trauma care for life-threatening situations.
        </p>
      </div>

      {/* Emergency Stats */}
      <div className="grid md:grid-cols-4 gap-6 mb-8">
        <motion.div 
          whileHover={{ scale: 1.05 }}
          className="text-center p-4 bg-red-50 rounded-xl border border-red-200"
        >
          <Clock className="h-8 w-8 text-red-600 mx-auto mb-2" />
          <div className="text-2xl font-bold text-red-600">{emergencyStats.responseTime}</div>
          <div className="text-sm text-gray-600">Avg Response Time</div>
        </motion.div>
        
        <motion.div 
          whileHover={{ scale: 1.05 }}
          className="text-center p-4 bg-blue-50 rounded-xl border border-blue-200"
        >
          <Ambulance className="h-8 w-8 text-blue-600 mx-auto mb-2" />
          <div className="text-2xl font-bold text-blue-600">{emergencyStats.ambulancesActive}</div>
          <div className="text-sm text-gray-600">Active Ambulances</div>
        </motion.div>
        
        <motion.div 
          whileHover={{ scale: 1.05 }}
          className="text-center p-4 bg-green-50 rounded-xl border border-green-200"
        >
          <Activity className="h-8 w-8 text-green-600 mx-auto mb-2" />
          <div className="text-2xl font-bold text-green-600">{emergencyStats.emergencyCases}</div>
          <div className="text-sm text-gray-600">Cases This Month</div>
        </motion.div>
        
        <motion.div 
          whileHover={{ scale: 1.05 }}
          className="text-center p-4 bg-purple-50 rounded-xl border border-purple-200"
        >
          <Shield className="h-8 w-8 text-purple-600 mx-auto mb-2" />
          <div className="text-2xl font-bold text-purple-600">{emergencyStats.successRate.toFixed(1)}%</div>
          <div className="text-sm text-gray-600">Success Rate</div>
        </motion.div>
      </div>

      {/* Emergency Types */}
      <div className="mb-8">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">Emergency Response Types</h3>
        <div className="grid md:grid-cols-2 gap-4">
          {emergencyTypes.map((emergency, index) => (
            <motion.div
              key={index}
              whileHover={{ y: -2 }}
              className={`${emergency.bgColor} rounded-lg p-4 border border-gray-200`}
            >
              <div className="flex items-start space-x-3">
                <emergency.icon className={`h-6 w-6 ${emergency.color} mt-1`} />
                <div>
                  <h4 className="font-semibold text-gray-900 mb-1">{emergency.title}</h4>
                  <p className="text-gray-600 text-sm mb-2">{emergency.description}</p>
                  <div className="flex items-center space-x-2">
                    <Clock className="h-4 w-4 text-gray-500" />
                    <span className="text-sm text-gray-600">Response: {emergency.responseTime}</span>
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Emergency Contacts */}
      <div className="mb-8">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">Emergency Contacts</h3>
        <div className="grid md:grid-cols-2 gap-4">
          {emergencyContacts.map((contact, index) => (
            <div key={index} className="bg-gray-50 rounded-lg p-4">
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-semibold text-gray-900">{contact.type}</h4>
                  <p className="text-2xl font-bold text-red-600">{contact.number}</p>
                  <p className="text-sm text-gray-600">{contact.available}</p>
                </div>
                <button className="bg-red-600 text-white p-3 rounded-full hover:bg-red-700">
                  <Phone className="h-5 w-5" />
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Ambulance Features */}
      <div className="mb-8">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">Advanced Ambulance Features</h3>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-3">
          {ambulanceFeatures.map((feature, index) => (
            <div key={index} className="flex items-center space-x-2 bg-blue-50 rounded-lg p-3">
              <div className="w-2 h-2 bg-blue-600 rounded-full"></div>
              <span className="text-sm text-gray-700">{feature}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Emergency Action */}
      <div className="bg-red-600 text-white rounded-xl p-6 text-center">
        <h3 className="text-2xl font-bold mb-4">Medical Emergency?</h3>
        <p className="mb-6 opacity-90">
          Don't wait - call our emergency helpline immediately for life-threatening situations
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="bg-white text-red-600 px-8 py-3 rounded-lg font-bold text-lg hover:bg-gray-100 flex items-center justify-center space-x-2"
          >
            <Phone className="h-5 w-5" />
            <span>Call Emergency: +91-863-234-5678</span>
          </motion.button>
          <button className="border border-white text-white px-8 py-3 rounded-lg hover:bg-white/10 font-semibold flex items-center justify-center space-x-2">
            <MapPin className="h-5 w-5" />
            <span>Find Nearest Hospital</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default EmergencyServices;