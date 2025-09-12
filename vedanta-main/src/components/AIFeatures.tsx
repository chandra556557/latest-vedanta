import React, { useState, useEffect } from 'react';
import { Bot, Brain, Calendar, Heart, MessageCircle, Sparkles, Zap, ChevronRight, Activity, TrendingUp, Users, Clock } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const AIFeatures = () => {
  const [activeFeature, setActiveFeature] = useState(0);
  const [liveStats, setLiveStats] = useState({
    patientsHelped: 1247,
    symptomsAnalyzed: 3892,
    appointmentsScheduled: 567,
    accuracyRate: 98.4,
    modelVersion: 'VedantaAI-v3.2',
    trainingDataSize: '2.5M',
    medicalKnowledge: '500K+'
  });
  const [isLive, setIsLive] = useState(true);

  // Simulate real-time updates
  useEffect(() => {
    const interval = setInterval(() => {
      setLiveStats(prev => ({
        patientsHelped: prev.patientsHelped + Math.floor(Math.random() * 3),
        symptomsAnalyzed: prev.symptomsAnalyzed + Math.floor(Math.random() * 5),
        appointmentsScheduled: prev.appointmentsScheduled + Math.floor(Math.random() * 2),
        accuracyRate: Math.min(99.9, prev.accuracyRate + (Math.random() - 0.5) * 0.1),
        modelVersion: prev.modelVersion,
        trainingDataSize: prev.trainingDataSize,
        medicalKnowledge: prev.medicalKnowledge
      }));
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  const features = [
    {
      icon: Bot,
      title: 'AI Health Assistant',
      description: 'Get instant answers to your health questions with our advanced AI chatbot',
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
      borderColor: 'border-blue-200',
      stats: { active: '24/7', responses: '0.8s avg', model: 'Self-trained' }
    },
    {
      icon: Brain,
      title: 'Smart Symptom Checker',
      description: 'Self-trained AI model analyzes symptoms with 98.4% medical accuracy',
      color: 'text-purple-600',
      bgColor: 'bg-purple-50',
      borderColor: 'border-purple-200',
      stats: { accuracy: '98.4%', training: '1M+ cases', model: 'Neural Net' }
    },
    {
      icon: Calendar,
      title: 'Intelligent Scheduling',
      description: 'Machine learning algorithm optimizes doctor-patient matching',
      color: 'text-emerald-600',
      bgColor: 'bg-emerald-50',
      borderColor: 'border-emerald-200',
      stats: { efficiency: '+40%', matching: '95%', algorithm: 'ML-based' }
    },
    {
      icon: Heart,
      title: 'Personalized Care Plans',
      description: 'Deep learning creates personalized treatment recommendations',
      color: 'text-red-600',
      bgColor: 'bg-red-50',
      borderColor: 'border-red-200',
      stats: { plans: '15K+', success: '92%', learning: 'Continuous' }
    }
  ];

  const liveActivities = [
    { action: 'Symptom check completed', user: 'Patient #1247', time: '2 min ago', type: 'symptom' },
    { action: 'Appointment scheduled', user: 'Patient #1248', time: '3 min ago', type: 'appointment' },
    { action: 'Health plan updated', user: 'Patient #1249', time: '5 min ago', type: 'plan' },
    { action: 'AI consultation started', user: 'Patient #1250', time: '7 min ago', type: 'chat' },
  ];

  return (
    <section className="py-20 bg-gradient-to-br from-indigo-50 via-white to-cyan-50">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex items-center justify-center space-x-2 mb-4"
          >
            <div className="relative">
              <Sparkles className="h-8 w-8 text-indigo-600" />
              <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
            </div>
            <h2 className="text-4xl lg:text-5xl font-bold text-gray-900">
              AI-Powered Healthcare
            </h2>
          </motion.div>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Experience the future of healthcare with our advanced AI technology that provides 
            personalized, intelligent, and efficient medical assistance.
          </p>
        </div>

        {/* Live Stats Dashboard */}
        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="bg-white rounded-2xl shadow-xl p-6 mb-12 border border-gray-100"
        >
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-2xl font-bold text-gray-900">VedantaAI Analytics</h3>
              <p className="text-sm text-gray-600">Self-trained medical AI model v{liveStats.modelVersion}</p>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span className="text-sm text-green-600 font-medium">Self-Learning</span>
            </div>
          </div>
          
          <div className="grid md:grid-cols-4 gap-6">
            <motion.div 
              whileHover={{ scale: 1.05 }}
              className="text-center p-4 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl border border-blue-100"
            >
              <Brain className="h-8 w-8 text-blue-600 mx-auto mb-2" />
              <div className="text-2xl font-bold text-blue-600">{liveStats.trainingDataSize}</div>
              <div className="text-sm text-gray-600">Training Dataset</div>
            </motion.div>
            
            <motion.div 
              whileHover={{ scale: 1.05 }}
              className="text-center p-4 bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl border border-purple-100"
            >
              <Activity className="h-8 w-8 text-purple-600 mx-auto mb-2" />
              <div className="text-2xl font-bold text-purple-600">{liveStats.medicalKnowledge}</div>
              <div className="text-sm text-gray-600">Medical Cases</div>
            </motion.div>
            
            <motion.div 
              whileHover={{ scale: 1.05 }}
              className="text-center p-4 bg-gradient-to-br from-emerald-50 to-teal-50 rounded-xl border border-emerald-100"
            >
              <Sparkles className="h-8 w-8 text-emerald-600 mx-auto mb-2" />
              <div className="text-2xl font-bold text-emerald-600">{liveStats.modelVersion}</div>
              <div className="text-sm text-gray-600">AI Model Version</div>
            </motion.div>
            
            <motion.div 
              whileHover={{ scale: 1.05 }}
              className="text-center p-4 bg-gradient-to-br from-orange-50 to-red-50 rounded-xl border border-orange-100"
            >
              <TrendingUp className="h-8 w-8 text-orange-600 mx-auto mb-2" />
              <div className="text-2xl font-bold text-orange-600">{liveStats.accuracyRate.toFixed(1)}%</div>
              <div className="text-sm text-gray-600">Medical Accuracy</div>
            </motion.div>
          </div>
          
          <div className="mt-6 text-center">
            <div className="inline-flex items-center space-x-2 bg-gradient-to-r from-purple-100 to-indigo-100 px-4 py-2 rounded-full">
              <Brain className="h-4 w-4 text-purple-600" />
              <span className="text-sm font-medium text-purple-800">Self-Trained on Vedanta's Medical Database</span>
            </div>
          </div>
        </motion.div>

        <div className="grid lg:grid-cols-2 gap-12 items-start mb-16">
          <div className="space-y-6">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className={`p-6 rounded-xl border-2 cursor-pointer transition-all duration-300 ${
                  activeFeature === index
                    ? `${feature.borderColor} ${feature.bgColor} shadow-lg scale-105`
                    : 'border-gray-200 bg-white hover:border-gray-300 hover:shadow-md'
                }`}
                onClick={() => setActiveFeature(index)}
              >
                <div className="flex items-start space-x-4">
                  <motion.div 
                    whileHover={{ rotate: 360 }}
                    transition={{ duration: 0.5 }}
                    className={`${feature.bgColor} p-3 rounded-lg`}
                  >
                    <feature.icon className={`h-6 w-6 ${feature.color}`} />
                  </motion.div>
                  <div className="flex-1">
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">{feature.title}</h3>
                    <p className="text-gray-600 mb-3">{feature.description}</p>
                    
                    {/* Dynamic Stats */}
                    <div className="flex flex-wrap gap-2">
                      {Object.entries(feature.stats).map(([key, value]) => (
                        <span key={key} className={`text-xs px-2 py-1 rounded-full ${feature.bgColor} ${feature.color} font-medium`}>
                          {key}: {value}
                        </span>
                      ))}
                    </div>
                  </div>
                  <ChevronRight className={`h-5 w-5 transition-transform ${
                    activeFeature === index ? 'rotate-90 text-indigo-600' : 'text-gray-400'
                  }`} />
                </div>
              </motion.div>
            ))}
          </div>

          <div className="space-y-6">
            {/* Interactive AI Demo */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-gradient-to-br from-purple-50 to-indigo-50 rounded-2xl p-8 border border-purple-200"
            >
              <div className="text-center">
                <div className="bg-gradient-to-r from-purple-600 to-indigo-600 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Sparkles className="h-8 w-8 text-white" />
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4">VedantaAI Assistant</h3>
                <p className="text-gray-600 mb-6">
                  Experience our self-trained medical AI model, specifically developed for healthcare using 
                  Vedanta's extensive medical database. Get expert medical guidance with 98.4% accuracy.
                </p>
                
                <div className="grid grid-cols-2 gap-4 mb-6">
                  <div className="bg-white rounded-lg p-4">
                    <Brain className="h-6 w-6 text-purple-600 mx-auto mb-2" />
                    <div className="text-sm font-medium text-gray-900">Self-Trained</div>
                    <div className="text-xs text-gray-600">2.5M Records</div>
                  </div>
                  <div className="bg-white rounded-lg p-4">
                    <Zap className="h-6 w-6 text-indigo-600 mx-auto mb-2" />
                    <div className="text-sm font-medium text-gray-900">Medical Expert</div>
                    <div className="text-xs text-gray-600">98.4% Accuracy</div>
                  </div>
                </div>
                
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="bg-gradient-to-r from-purple-600 to-indigo-600 text-white px-8 py-3 rounded-lg hover:shadow-lg transition-all duration-300 font-semibold"
                >
                  Try VedantaAI Assistant
                </motion.button>
              </div>
            </motion.div>

            {/* Live Activity Feed */}
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100"
            >
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900">Live AI Activity</h3>
                <div className="flex items-center space-x-2">
                  <Activity className="h-4 w-4 text-green-500" />
                  <span className="text-sm text-green-600">Real-time</span>
                </div>
              </div>
              
              <div className="space-y-3">
                <AnimatePresence>
                  {liveActivities.map((activity, index) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      exit={{ opacity: 0, x: 20 }}
                      className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg"
                    >
                      <div className={`w-2 h-2 rounded-full ${
                        activity.type === 'symptom' ? 'bg-purple-500' :
                        activity.type === 'appointment' ? 'bg-emerald-500' :
                        activity.type === 'plan' ? 'bg-red-500' : 'bg-blue-500'
                      }`}></div>
                      <div className="flex-1">
                        <p className="text-sm text-gray-800">{activity.action}</p>
                        <p className="text-xs text-gray-500">{activity.user} • {activity.time}</p>
                      </div>
                    </motion.div>
                  ))}
                </AnimatePresence>
              </div>
            </motion.div>
          </div>
        </div>

        {/* AI Capabilities Grid */}
        <div className="grid md:grid-cols-3 gap-8">
          <motion.div 
            whileHover={{ y: -5 }}
            className="text-center"
          >
            <div className="bg-gradient-to-br from-blue-500 to-indigo-600 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <Brain className="h-8 w-8 text-white" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Machine Learning Diagnostics</h3>
            <p className="text-gray-600">Self-trained neural networks analyze symptoms using Vedanta's medical database for expert-level assessments.</p>
            <div className="mt-3 text-sm text-blue-600 font-medium">98.4% Medical Accuracy</div>
          </motion.div>
          
          <motion.div 
            whileHover={{ y: -5 }}
            className="text-center"
          >
            <div className="bg-gradient-to-br from-emerald-500 to-teal-600 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <Sparkles className="h-8 w-8 text-white" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Predictive Analytics</h3>
            <p className="text-gray-600">Self-learning algorithms predict health risks using pattern recognition from 500K+ medical cases.</p>
            <div className="mt-3 text-sm text-emerald-600 font-medium">Trained on 2.5M Records</div>
          </motion.div>
          
          <motion.div 
            whileHover={{ y: -5 }}
            className="text-center"
          >
            <div className="bg-gradient-to-br from-purple-500 to-pink-600 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <Zap className="h-8 w-8 text-white" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Real-time Monitoring</h3>
            <p className="text-gray-600">Continuous self-learning AI monitors health patterns and provides personalized medical insights.</p>
            <div className="mt-3 text-sm text-purple-600 font-medium">Self-Learning Model</div>
          </motion.div>
        </div>
      </div>
    </section>
  );
};

export default AIFeatures;