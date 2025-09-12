import React, { useState } from 'react';
import { FileText, Download, Upload, Eye, Calendar, Activity, Heart, Brain, Shield, Search, Filter } from 'lucide-react';
import { motion } from 'framer-motion';

const HealthRecords = () => {
  const [activeTab, setActiveTab] = useState('records');
  const [searchTerm, setSearchTerm] = useState('');

  const healthRecords = [
    {
      id: 1,
      type: 'Lab Report',
      title: 'Complete Blood Count',
      date: '2024-01-15',
      doctor: 'Dr. K. Srinivasa Rao',
      department: 'Pathology',
      status: 'Normal',
      icon: Activity
    },
    {
      id: 2,
      type: 'Prescription',
      title: 'Cardiac Medication',
      date: '2024-01-10',
      doctor: 'Dr. K. Srinivasa Rao',
      department: 'Cardiology',
      status: 'Active',
      icon: Heart
    },
    {
      id: 3,
      type: 'Imaging',
      title: 'Chest X-Ray',
      date: '2024-01-08',
      doctor: 'Dr. M. Prasad',
      department: 'Radiology',
      status: 'Normal',
      icon: Brain
    },
    {
      id: 4,
      type: 'Consultation',
      title: 'Follow-up Visit',
      date: '2024-01-05',
      doctor: 'Dr. P. Lakshmi Prasanna',
      department: 'Gynecology',
      status: 'Completed',
      icon: FileText
    }
  ];

  const vitalSigns = [
    { label: 'Blood Pressure', value: '120/80 mmHg', status: 'Normal', color: 'text-green-600' },
    { label: 'Heart Rate', value: '72 BPM', status: 'Normal', color: 'text-green-600' },
    { label: 'Temperature', value: '98.6°F', status: 'Normal', color: 'text-green-600' },
    { label: 'Weight', value: '70 kg', status: 'Stable', color: 'text-blue-600' },
    { label: 'Blood Sugar', value: '95 mg/dL', status: 'Normal', color: 'text-green-600' },
    { label: 'Cholesterol', value: '180 mg/dL', status: 'Normal', color: 'text-green-600' }
  ];

  const upcomingAppointments = [
    {
      date: '2024-01-20',
      time: '10:00 AM',
      doctor: 'Dr. K. Srinivasa Rao',
      department: 'Cardiology',
      type: 'Follow-up'
    },
    {
      date: '2024-01-25',
      time: '2:30 PM',
      doctor: 'Dr. B. Srinivasa Rao',
      department: 'Pediatrics',
      type: 'Consultation'
    }
  ];

  const tabs = [
    { id: 'records', label: 'Medical Records', icon: FileText },
    { id: 'vitals', label: 'Vital Signs', icon: Activity },
    { id: 'appointments', label: 'Appointments', icon: Calendar }
  ];

  return (
    <div className="bg-white rounded-2xl shadow-lg p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-3xl font-bold text-gray-900">Digital Health Records</h2>
          <p className="text-gray-600">Secure access to your complete medical history</p>
        </div>
        <div className="flex items-center space-x-2">
          <Shield className="h-5 w-5 text-green-600" />
          <span className="text-sm text-green-600 font-medium">Blockchain Secured</span>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex space-x-1 mb-6 bg-gray-100 rounded-lg p-1">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex items-center space-x-2 px-4 py-2 rounded-md font-medium transition-all duration-300 ${
              activeTab === tab.id
                ? 'bg-white text-blue-600 shadow-sm'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            <tab.icon className="h-4 w-4" />
            <span>{tab.label}</span>
          </button>
        ))}
      </div>

      {/* Medical Records Tab */}
      {activeTab === 'records' && (
        <div>
          <div className="flex items-center space-x-4 mb-6">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search records..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
              />
            </div>
            <button className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
              <Upload className="h-4 w-4" />
              <span>Upload</span>
            </button>
          </div>

          <div className="space-y-4">
            {healthRecords.map((record) => (
              <motion.div
                key={record.id}
                whileHover={{ y: -2 }}
                className="bg-gray-50 rounded-lg p-4 hover:shadow-md transition-all duration-300"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <div className="bg-blue-100 p-2 rounded-lg">
                      <record.icon className="h-5 w-5 text-blue-600" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900">{record.title}</h3>
                      <p className="text-sm text-gray-600">{record.type} • {record.doctor}</p>
                      <p className="text-xs text-gray-500">{record.date} • {record.department}</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-3">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      record.status === 'Normal' ? 'bg-green-100 text-green-700' :
                      record.status === 'Active' ? 'bg-blue-100 text-blue-700' :
                      'bg-gray-100 text-gray-700'
                    }`}>
                      {record.status}
                    </span>
                    <button className="p-2 text-gray-400 hover:text-blue-600">
                      <Eye className="h-4 w-4" />
                    </button>
                    <button className="p-2 text-gray-400 hover:text-blue-600">
                      <Download className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      )}

      {/* Vital Signs Tab */}
      {activeTab === 'vitals' && (
        <div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
            {vitalSigns.map((vital, index) => (
              <motion.div
                key={index}
                whileHover={{ scale: 1.02 }}
                className="bg-gray-50 rounded-lg p-4"
              >
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-medium text-gray-900">{vital.label}</h3>
                  <Activity className="h-4 w-4 text-gray-400" />
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-2xl font-bold text-gray-900">{vital.value}</span>
                  <span className={`text-sm font-medium ${vital.color}`}>{vital.status}</span>
                </div>
              </motion.div>
            ))}
          </div>
          
          <div className="bg-blue-50 rounded-lg p-4">
            <h3 className="font-semibold text-blue-900 mb-2">Health Trends</h3>
            <p className="text-blue-700 text-sm">Your vital signs are within normal ranges. Keep up the good work!</p>
          </div>
        </div>
      )}

      {/* Appointments Tab */}
      {activeTab === 'appointments' && (
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Upcoming Appointments</h3>
          <div className="space-y-4">
            {upcomingAppointments.map((appointment, index) => (
              <div key={index} className="bg-gray-50 rounded-lg p-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <div className="bg-blue-100 p-2 rounded-lg">
                      <Calendar className="h-5 w-5 text-blue-600" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-900">{appointment.doctor}</h4>
                      <p className="text-sm text-gray-600">{appointment.department} • {appointment.type}</p>
                      <p className="text-xs text-gray-500">{appointment.date} at {appointment.time}</p>
                    </div>
                  </div>
                  <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
                    Reschedule
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default HealthRecords;