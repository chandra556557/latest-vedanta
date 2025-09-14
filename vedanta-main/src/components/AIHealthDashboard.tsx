import React, { useState } from 'react';
import { Activity, Heart, Brain, TrendingUp, Calendar, Bell, User, Settings } from 'lucide-react';
import AISymptomChecker from './AISymptomChecker';

const AIHealthDashboard = () => {
  const [activeTab, setActiveTab] = useState('overview');

  const healthMetrics = [
    {
      icon: Heart,
      title: 'Heart Rate',
      value: '72 BPM',
      trend: '+2%',
      status: 'normal',
      color: 'text-red-500'
    },
    {
      icon: Activity,
      title: 'Blood Pressure',
      value: '120/80',
      trend: 'stable',
      status: 'normal',
      color: 'text-blue-500'
    },
    {
      icon: Brain,
      title: 'Stress Level',
      value: 'Low',
      trend: '-5%',
      status: 'good',
      color: 'text-purple-500'
    }
  ];

  const upcomingAppointments = [
    {
      doctor: 'Dr. Rajesh Sharma',
      specialty: 'Cardiology',
      date: '2024-01-20',
      time: '10:00 AM',
      type: 'Follow-up'
    },
    {
      doctor: 'Dr. Srinivas Polisetty',
      specialty: 'Neurology',
      date: '2024-01-25',
      time: '2:30 PM',
      type: 'Consultation'
    }
  ];

  const aiInsights = [
    {
      type: 'recommendation',
      title: 'Exercise Reminder',
      message: 'Based on your activity levels, consider adding 30 minutes of cardio to your routine.',
      priority: 'medium'
    },
    {
      type: 'alert',
      title: 'Medication Reminder',
      message: 'Time to take your prescribed medication for blood pressure.',
      priority: 'high'
    },
    {
      type: 'insight',
      title: 'Sleep Pattern',
      message: 'Your sleep quality has improved by 15% this week. Keep up the good routine!',
      priority: 'low'
    }
  ];

  const tabs = [
    { id: 'overview', label: 'Overview', icon: Activity },
    { id: 'symptoms', label: 'Symptom Checker', icon: Brain },
    { id: 'appointments', label: 'Appointments', icon: Calendar },
    { id: 'insights', label: 'AI Insights', icon: TrendingUp }
  ];

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-2xl shadow-lg p-6 mb-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="bg-gradient-to-r from-indigo-500 to-purple-600 p-3 rounded-full">
                <User className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">AI Health Dashboard</h1>
                <p className="text-gray-600">Welcome back! Here's your health overview.</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <button className="p-2 text-gray-400 hover:text-gray-600 transition-colors">
                <Bell className="h-6 w-6" />
              </button>
              <button className="p-2 text-gray-400 hover:text-gray-600 transition-colors">
                <Settings className="h-6 w-6" />
              </button>
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="bg-white rounded-2xl shadow-lg mb-6">
          <div className="flex space-x-1 p-2">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 px-6 py-3 rounded-xl font-medium transition-all duration-300 ${
                  activeTab === tab.id
                    ? 'bg-gradient-to-r from-indigo-500 to-purple-600 text-white shadow-lg'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                <tab.icon className="h-5 w-5" />
                <span>{tab.label}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Content */}
        {activeTab === 'overview' && (
          <div className="grid lg:grid-cols-3 gap-6">
            {/* Health Metrics */}
            <div className="lg:col-span-2 space-y-6">
              <div className="bg-white rounded-2xl shadow-lg p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-6">Health Metrics</h2>
                <div className="grid md:grid-cols-2 gap-4">
                  {healthMetrics.map((metric, index) => (
                    <div key={index} className="bg-gray-50 rounded-xl p-4">
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center space-x-3">
                          <metric.icon className={`h-6 w-6 ${metric.color}`} />
                          <span className="font-medium text-gray-900">{metric.title}</span>
                        </div>
                        <span className={`text-sm px-2 py-1 rounded-full ${
                          metric.status === 'excellent' ? 'bg-green-100 text-green-700' :
                          metric.status === 'good' ? 'bg-blue-100 text-blue-700' :
                          'bg-gray-100 text-gray-700'
                        }`}>
                          {metric.status}
                        </span>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-2xl font-bold text-gray-900">{metric.value}</span>
                        <span className="text-sm text-green-600">{metric.trend}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* AI Insights */}
              <div className="bg-white rounded-2xl shadow-lg p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-6">AI Health Insights</h2>
                <div className="space-y-4">
                  {aiInsights.map((insight, index) => (
                    <div key={index} className={`p-4 rounded-xl border-l-4 ${
                      insight.priority === 'high' ? 'bg-red-50 border-red-500' :
                      insight.priority === 'medium' ? 'bg-yellow-50 border-yellow-500' :
                      'bg-blue-50 border-blue-500'
                    }`}>
                      <h3 className="font-semibold text-gray-900 mb-1">{insight.title}</h3>
                      <p className="text-gray-600 text-sm">{insight.message}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Sidebar */}
            <div className="space-y-6">
              {/* Upcoming Appointments */}
              <div className="bg-white rounded-2xl shadow-lg p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-6">Upcoming Appointments</h2>
                <div className="space-y-4">
                  {upcomingAppointments.map((appointment, index) => (
                    <div key={index} className="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-xl p-4">
                      <div className="flex items-center justify-between mb-2">
                        <h3 className="font-semibold text-gray-900">{appointment.doctor}</h3>
                        <span className="text-xs bg-indigo-100 text-indigo-700 px-2 py-1 rounded-full">
                          {appointment.type}
                        </span>
                      </div>
                      <p className="text-sm text-gray-600 mb-2">{appointment.specialty}</p>
                      <div className="flex items-center justify-between text-sm">
                        <span className="text-gray-500">{appointment.date}</span>
                        <span className="font-medium text-indigo-600">{appointment.time}</span>
                      </div>
                    </div>
                  ))}
                </div>
                <button className="w-full mt-4 bg-gradient-to-r from-indigo-500 to-purple-600 text-white py-2 rounded-lg hover:shadow-lg transition-all duration-300">
                  Book New Appointment
                </button>
              </div>

              {/* Quick Actions */}
              <div className="bg-white rounded-2xl shadow-lg p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-6">Quick Actions</h2>
                <div className="space-y-3">
                  <button className="w-full bg-gradient-to-r from-emerald-500 to-teal-600 text-white py-3 rounded-lg hover:shadow-lg transition-all duration-300 flex items-center justify-center space-x-2">
                    <Brain className="h-5 w-5" />
                    <span>Check Symptoms</span>
                  </button>
                  <button className="w-full bg-gradient-to-r from-blue-500 to-indigo-600 text-white py-3 rounded-lg hover:shadow-lg transition-all duration-300 flex items-center justify-center space-x-2">
                    <Calendar className="h-5 w-5" />
                    <span>Schedule Appointment</span>
                  </button>
                  <button className="w-full bg-gradient-to-r from-purple-500 to-pink-600 text-white py-3 rounded-lg hover:shadow-lg transition-all duration-300 flex items-center justify-center space-x-2">
                    <Activity className="h-5 w-5" />
                    <span>View Health Records</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'symptoms' && (
          <div className="max-w-4xl mx-auto">
            <AISymptomChecker />
          </div>
        )}

        {activeTab === 'appointments' && (
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Appointment Management</h2>
            <p className="text-gray-600">Appointment management interface would be implemented here.</p>
          </div>
        )}

        {activeTab === 'insights' && (
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">AI Health Insights</h2>
            <p className="text-gray-600">Detailed AI insights and analytics would be displayed here.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default AIHealthDashboard;