import React from 'react';
import { Bot, Brain, Activity, Sparkles, MessageCircle, TrendingUp, Users, Clock } from 'lucide-react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import AISymptomChecker from '../components/AISymptomChecker';

const AIServicesPage = () => {
  const [activeTab, setActiveTab] = React.useState('overview');

  const aiServices = [
    {
      id: 'chatbot',
      icon: Bot,
      title: 'AI Health Assistant',
      description: 'Get instant answers to your health questions with our advanced AI chatbot',
      features: ['24/7 Availability', 'Multi-language Support', 'Symptom Analysis', 'Appointment Booking'],
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
      stats: { users: '50K+', accuracy: '96%', response: '1.2s' }
    },
    {
      id: 'symptom-checker',
      icon: Brain,
      title: 'Smart Symptom Checker',
      description: 'AI-powered symptom analysis to help identify potential health concerns',
      features: ['500+ Conditions', '94.7% Accuracy', 'Instant Results', 'Specialist Recommendations'],
      color: 'text-purple-600',
      bgColor: 'bg-purple-50',
      stats: { checks: '100K+', conditions: '500+', accuracy: '94.7%' }
    },
    {
      id: 'dashboard',
      icon: Activity,
      title: 'Health Dashboard',
      description: 'Personalized health monitoring and insights powered by AI',
      features: ['Real-time Monitoring', 'Predictive Analytics', 'Health Trends', 'Custom Alerts'],
      color: 'text-emerald-600',
      bgColor: 'bg-emerald-50',
      stats: { patients: '25K+', insights: '1M+', accuracy: '92%' }
    }
  ];

  const benefits = [
    {
      icon: Clock,
      title: 'Instant Access',
      description: 'Get immediate health assistance anytime, anywhere'
    },
    {
      icon: Brain,
      title: 'Smart Analysis',
      description: 'Advanced AI algorithms provide accurate health insights'
    },
    {
      icon: Users,
      title: 'Personalized Care',
      description: 'Tailored recommendations based on your health profile'
    },
    {
      icon: TrendingUp,
      title: 'Continuous Learning',
      description: 'AI improves with every interaction for better results'
    }
  ];

  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-indigo-50 via-white to-cyan-50 py-20">
        <div className="container mx-auto px-4">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center mb-16"
          >
            <div className="flex items-center justify-center space-x-2 mb-4">
              <Sparkles className="h-8 w-8 text-indigo-600" />
              <h1 className="text-5xl lg:text-6xl font-bold text-gray-900">
                AI-Powered <span className="text-indigo-600">Healthcare</span>
              </h1>
            </div>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
              Experience the future of healthcare with our advanced AI technology that provides 
              personalized, intelligent, and efficient medical assistance.
            </p>
          </motion.div>

          {/* Live Stats */}
          <div className="grid md:grid-cols-4 gap-6 max-w-4xl mx-auto">
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="text-center p-6 bg-white rounded-xl shadow-lg"
            >
              <Users className="h-8 w-8 text-blue-600 mx-auto mb-2" />
              <div className="text-2xl font-bold text-blue-600">175K+</div>
              <div className="text-sm text-gray-600">Users Served</div>
            </motion.div>
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="text-center p-6 bg-white rounded-xl shadow-lg"
            >
              <Brain className="h-8 w-8 text-purple-600 mx-auto mb-2" />
              <div className="text-2xl font-bold text-purple-600">500K+</div>
              <div className="text-sm text-gray-600">Symptoms Analyzed</div>
            </motion.div>
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="text-center p-6 bg-white rounded-xl shadow-lg"
            >
              <Activity className="h-8 w-8 text-emerald-600 mx-auto mb-2" />
              <div className="text-2xl font-bold text-emerald-600">95.2%</div>
              <div className="text-sm text-gray-600">Accuracy Rate</div>
            </motion.div>
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="text-center p-6 bg-white rounded-xl shadow-lg"
            >
              <Clock className="h-8 w-8 text-orange-600 mx-auto mb-2" />
              <div className="text-2xl font-bold text-orange-600">1.2s</div>
              <div className="text-sm text-gray-600">Avg Response</div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* AI Services */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-gray-900 text-center mb-16">Our AI Services</h2>
          
          <div className="grid lg:grid-cols-3 gap-8">
            {aiServices.map((service, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className={`${service.bgColor} rounded-2xl p-8 border-2 border-transparent hover:border-gray-200 transition-all duration-300 hover:shadow-lg`}
              >
                <div className="flex items-center space-x-4 mb-6">
                  <div className="bg-white p-4 rounded-full shadow-lg">
                    <service.icon className={`h-8 w-8 ${service.color}`} />
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-gray-900">{service.title}</h3>
                    <p className="text-gray-600">{service.description}</p>
                  </div>
                </div>

                <div className="space-y-4 mb-6">
                  <h4 className="font-semibold text-gray-900">Key Features:</h4>
                  <ul className="space-y-2">
                    {service.features.map((feature, i) => (
                      <li key={i} className="flex items-center space-x-2">
                        <div className={`w-2 h-2 rounded-full ${service.color.replace('text-', 'bg-')}`}></div>
                        <span className="text-gray-700 text-sm">{feature}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="grid grid-cols-3 gap-2 mb-6">
                  {Object.entries(service.stats).map(([key, value]) => (
                    <div key={key} className="text-center bg-white/70 rounded-lg p-2">
                      <div className={`text-lg font-bold ${service.color}`}>{value}</div>
                      <div className="text-xs text-gray-600 capitalize">{key}</div>
                    </div>
                  ))}
                </div>

                <Link
                  to={`/ai-services/${service.id}`}
                  className="block w-full bg-white text-gray-900 px-6 py-3 rounded-lg hover:shadow-lg transition-all duration-300 font-medium text-center"
                >
                  Try {service.title}
                </Link>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Interactive Demo */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-gray-900 text-center mb-16">Try Our AI Symptom Checker</h2>
          <AISymptomChecker />
        </div>
      </section>

      {/* Benefits */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-gray-900 text-center mb-16">Why Choose AI Healthcare?</h2>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {benefits.map((benefit, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="text-center"
              >
                <div className="bg-gradient-to-br from-indigo-100 to-purple-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <benefit.icon className="h-8 w-8 text-indigo-600" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">{benefit.title}</h3>
                <p className="text-gray-600">{benefit.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-br from-indigo-600 to-purple-600 text-white">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-4xl font-bold mb-6">Ready to Experience AI Healthcare?</h2>
          <p className="text-xl mb-8 opacity-90 max-w-2xl mx-auto">
            Join thousands of patients who trust our AI-powered healthcare solutions 
            for better health outcomes and personalized care.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/ai-services/chatbot"
              className="bg-white text-indigo-600 px-8 py-3 rounded-lg hover:bg-gray-100 transition-colors font-semibold flex items-center justify-center space-x-2"
            >
              <MessageCircle className="h-5 w-5" />
              <span>Start AI Chat</span>
            </Link>
            <Link
              to="/ai-services/symptom-checker"
              className="border border-white text-white px-8 py-3 rounded-lg hover:bg-white/10 transition-colors font-semibold flex items-center justify-center space-x-2"
            >
              <Brain className="h-5 w-5" />
              <span>Check Symptoms</span>
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default AIServicesPage;