import React, { useState } from 'react';
import { Video, Phone, MessageCircle, Calendar, Clock, User, Shield, Wifi, Camera, Mic, MicOff, VideoOff } from 'lucide-react';
import { motion } from 'framer-motion';

const TelemedConsultation = () => {
  const [activeTab, setActiveTab] = useState('video');
  const [isCallActive, setIsCallActive] = useState(false);
  const [isMuted, setIsMuted] = useState(false);
  const [isVideoOff, setIsVideoOff] = useState(false);

  const consultationTypes = [
    {
      id: 'video',
      icon: Video,
      title: 'Video Consultation',
      description: 'Face-to-face consultation with HD video quality',
      price: '₹800',
      duration: '15-30 mins'
    },
    {
      id: 'audio',
      icon: Phone,
      title: 'Audio Consultation',
      description: 'Voice-only consultation for privacy',
      price: '₹500',
      duration: '10-20 mins'
    },
    {
      id: 'chat',
      icon: MessageCircle,
      title: 'Chat Consultation',
      description: 'Text-based consultation with instant responses',
      price: '₹300',
      duration: '24 hours'
    }
  ];

  const availableDoctors = [
    {
      name: 'Dr. K. Srinivasa Rao',
      specialty: 'Cardiology',
      rating: 4.9,
      nextSlot: '2:30 PM Today',
      image: 'https://images.pexels.com/photos/612608/pexels-photo-612608.jpeg?auto=compress&cs=tinysrgb&w=400'
    },
    {
      name: 'Dr. P. Lakshmi Prasanna',
      specialty: 'Gynecology',
      rating: 4.8,
      nextSlot: '4:00 PM Today',
      image: 'https://images.pexels.com/photos/5452293/pexels-photo-5452293.jpeg?auto=compress&cs=tinysrgb&w=400'
    },
    {
      name: 'Dr. B. Srinivasa Rao',
      specialty: 'Pediatrics',
      rating: 4.8,
      nextSlot: '5:15 PM Today',
      image: 'https://images.pexels.com/photos/5452201/pexels-photo-5452201.jpeg?auto=compress&cs=tinysrgb&w=400'
    }
  ];

  return (
    <div className="bg-white rounded-2xl shadow-lg p-6">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">Telemedicine Consultation</h2>
        <p className="text-gray-600 max-w-2xl mx-auto">
          Connect with our expert doctors from the comfort of your home. 
          Secure, convenient, and available 24/7 for non-emergency consultations.
        </p>
      </div>

      {/* Consultation Types */}
      <div className="grid md:grid-cols-3 gap-6 mb-8">
        {consultationTypes.map((type) => (
          <motion.div
            key={type.id}
            whileHover={{ y: -5 }}
            className={`p-6 rounded-xl border-2 cursor-pointer transition-all duration-300 ${
              activeTab === type.id
                ? 'border-blue-500 bg-blue-50 shadow-lg'
                : 'border-gray-200 hover:border-gray-300'
            }`}
            onClick={() => setActiveTab(type.id)}
          >
            <type.icon className={`h-8 w-8 mx-auto mb-4 ${
              activeTab === type.id ? 'text-blue-600' : 'text-gray-600'
            }`} />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">{type.title}</h3>
            <p className="text-gray-600 text-sm mb-4">{type.description}</p>
            <div className="flex justify-between items-center">
              <span className="text-blue-600 font-bold">{type.price}</span>
              <span className="text-gray-500 text-sm">{type.duration}</span>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Available Doctors */}
      <div className="mb-8">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">Available Doctors</h3>
        <div className="grid md:grid-cols-3 gap-4">
          {availableDoctors.map((doctor, index) => (
            <div key={index} className="bg-gray-50 rounded-lg p-4">
              <div className="flex items-center space-x-3 mb-3">
                <img
                  src={doctor.image}
                  alt={doctor.name}
                  className="w-12 h-12 rounded-full object-cover"
                />
                <div>
                  <h4 className="font-semibold text-gray-900">{doctor.name}</h4>
                  <p className="text-sm text-gray-600">{doctor.specialty}</p>
                </div>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-green-600 font-medium">{doctor.nextSlot}</span>
                <button className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700">
                  Book Now
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Security Features */}
      <div className="bg-green-50 rounded-lg p-6 mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <Shield className="h-5 w-5 text-green-600 mr-2" />
          Security & Privacy
        </h3>
        <div className="grid md:grid-cols-3 gap-4 text-sm">
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            <span>End-to-end encryption</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            <span>HIPAA compliant</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            <span>Secure data storage</span>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="flex flex-col sm:flex-row gap-4">
        <button className="flex-1 bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition-colors font-semibold">
          Start Consultation Now
        </button>
        <button className="flex-1 border border-blue-600 text-blue-600 py-3 rounded-lg hover:bg-blue-50 transition-colors font-semibold">
          Schedule for Later
        </button>
      </div>
    </div>
  );
};

export default TelemedConsultation;