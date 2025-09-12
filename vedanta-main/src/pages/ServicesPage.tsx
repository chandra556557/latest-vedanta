import React, { useState } from 'react';
import { Heart, Bone, Activity, UserCheck, Stethoscope, ArrowRight, Users, Award } from 'lucide-react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';

const ServicesPage = () => {
  const [activeService, setActiveService] = useState(0);

  const services = [
    {
      id: 'nephrology',
      icon: Stethoscope,
      title: 'Nephrology',
      description: 'Comprehensive kidney care including CKD evaluation, management and follow-up.',
      color: 'text-sky-600',
      bgColor: 'bg-sky-50',
      borderColor: 'border-sky-200',
      procedures: ['CKD Evaluation', 'Biopsy Coordination', 'AKI Management', 'Electrolyte Disorders'],
      doctors: 6,
      successRate: '97%',
      waitTime: '1-2 days'
    },
    {
      id: 'urology',
      icon: Activity,
      title: 'Urology',
      description: 'Endourology, laparoscopic urology and reconstructive procedures for urinary tract conditions.',
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
      borderColor: 'border-blue-200',
      procedures: ['URS/RIRS', 'PCNL', 'TURP', 'Urethroplasty'],
      doctors: 5,
      successRate: '96%',
      waitTime: '2-3 days'
    },
    {
      id: 'orthopedics',
      icon: Bone,
      title: 'Orthopedics',
      description: 'Comprehensive bone, joint and musculoskeletal care including trauma and joint replacement.',
      color: 'text-orange-600',
      bgColor: 'bg-orange-50',
      borderColor: 'border-orange-200',
      procedures: ['Joint Replacement', 'Arthroscopy', 'Fracture Fixation', 'Sports Medicine'],
      doctors: 8,
      successRate: '95%',
      waitTime: '3-5 days'
    },
    {
      id: 'general-medicine',
      icon: UserCheck,
      title: 'General Medicine',
      description: 'Primary care, preventive health and management of common medical conditions.',
      color: 'text-emerald-600',
      bgColor: 'bg-emerald-50',
      borderColor: 'border-emerald-200',
      procedures: ['Preventive Health', 'Diabetes Care', 'Hypertension Clinic', 'Infection Management'],
      doctors: 7,
      successRate: '98%',
      waitTime: 'Same day'
    },
    {
      id: 'dental-care',
      icon: Heart,
      title: 'Dental Care',
      description: 'Preventive, restorative and cosmetic dental treatments for all ages.',
      color: 'text-purple-600',
      bgColor: 'bg-purple-50',
      borderColor: 'border-purple-200',
      procedures: ['Scaling & Polishing', 'Fillings', 'Root Canal', 'Crowns & Bridges'],
      doctors: 4,
      successRate: '99%',
      waitTime: '1-3 days'
    }
  ];

  const emergencyServices = [
    { title: '24/7 Emergency Room', description: 'Round-the-clock emergency medical care' },
    { title: 'Trauma Center', description: 'Level 1 trauma care facility' },
    { title: 'Cardiac Emergency', description: 'Immediate cardiac intervention services' },
    { title: 'Stroke Unit', description: 'Specialized stroke treatment and rehabilitation' }
  ];

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
              Departments - <span className="text-sky-600">Best Kidney Specialist Hospital</span>
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
              Our core departments offering comprehensive care across nephrology, urology, orthopedics, general medicine, and dental care.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Services Grid */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="grid lg:grid-cols-2 gap-12">
            {/* Services List */}
            <div className="space-y-6">
              {services.map((service, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className={`p-6 rounded-xl border-2 cursor-pointer transition-all duration-300 ${
                    activeService === index
                      ? `${service.borderColor} ${service.bgColor} shadow-lg`
                      : 'border-gray-200 bg-white hover:border-gray-300 hover:shadow-md'
                  }`}
                  onClick={() => setActiveService(index)}
                >
                  <div className="flex items-start space-x-4">
                    <div className={`${service.bgColor} p-3 rounded-lg`}>
                      <service.icon className={`h-6 w-6 ${service.color}`} />
                    </div>
                    <div className="flex-1">
                      <h3 className="text-xl font-semibold text-gray-900 mb-2">{service.title}</h3>
                      <p className="text-gray-600 mb-4">{service.description}</p>
                      
                      <div className="grid grid-cols-2 gap-4 text-sm">
                        <div className="text-center">
                          <Users className="h-4 w-4 mx-auto mb-1 text-gray-500" />
                          <div className="font-medium">{service.doctors} Doctors</div>
                        </div>
                        <div className="text-center">
                          <Award className="h-4 w-4 mx-auto mb-1 text-gray-500" />
                          <div className="font-medium">{service.successRate} Success</div>
                        </div>
                      </div>
                    </div>
                    <Link
                      to={`/services/${service.id}`}
                      className={`${service.color} hover:underline font-medium flex items-center space-x-1`}
                    >
                      <span>Learn More</span>
                      <ArrowRight className="h-4 w-4" />
                    </Link>
                  </div>
                </motion.div>
              ))}
            </div>

            {/* Service Details */}
            <div className="sticky top-8">
              <motion.div 
                key={activeService}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className={`${services[activeService].bgColor} rounded-2xl p-8 border ${services[activeService].borderColor}`}
              >
                <div className="flex items-center space-x-4 mb-6">
                  <div className="bg-white p-4 rounded-full shadow-lg">
                    {React.createElement(services[activeService].icon, {
                      className: `h-8 w-8 ${services[activeService].color}`
                    })}
                  </div>
                  <div>
                    <h3 className="text-2xl font-bold text-gray-900">{services[activeService].title}</h3>
                    <p className="text-gray-600">Department Overview</p>
                  </div>
                </div>

                <div className="space-y-6">
                  <div>
                    <h4 className="text-lg font-semibold text-gray-900 mb-3">Key Procedures</h4>
                    <div className="grid grid-cols-2 gap-2">
                      {services[activeService].procedures.map((procedure, index) => (
                        <div key={index} className="bg-white/70 rounded-lg p-3 text-sm font-medium">
                          {procedure}
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4 text-center">
                    <div className="bg-white/70 rounded-lg p-4">
                      <Users className={`h-6 w-6 mx-auto mb-2 ${services[activeService].color}`} />
                      <div className="text-lg font-bold">{services[activeService].doctors}</div>
                      <div className="text-sm text-gray-600">Expert Doctors</div>
                    </div>
                    <div className="bg-white/70 rounded-lg p-4">
                      <Award className={`h-6 w-6 mx-auto mb-2 ${services[activeService].color}`} />
                      <div className="text-lg font-bold">{services[activeService].successRate}</div>
                      <div className="text-sm text-gray-600">Success Rate</div>
                    </div>
                  </div>

                  <div className="flex space-x-4">
                    <Link
                      to={`/services/${services[activeService].id}`}
                      className="flex-1 bg-white text-gray-900 px-6 py-3 rounded-lg hover:shadow-lg transition-all duration-300 font-medium text-center"
                    >
                      View Details
                    </Link>
                    <Link
                      to="/appointment"
                      className={`flex-1 bg-gradient-to-r from-sky-600 to-emerald-600 text-white px-6 py-3 rounded-lg hover:shadow-lg transition-all duration-300 font-medium text-center`}
                    >
                      Book Appointment
                    </Link>
                  </div>
                </div>
              </motion.div>
            </div>
          </div>
        </div>
      </section>

      {/* Emergency Services */}
      <section className="py-20 bg-red-50">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-gray-900 text-center mb-16">Emergency Services</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {emergencyServices.map((service, index) => (
              <motion.div 
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="bg-white rounded-xl p-6 shadow-lg hover:shadow-xl transition-shadow"
              >
                <Stethoscope className="h-8 w-8 text-red-600 mb-4" />
                <h3 className="text-lg font-semibold text-gray-900 mb-2">{service.title}</h3>
                <p className="text-gray-600 text-sm">{service.description}</p>
              </motion.div>
            ))}
          </div>
          
          <div className="text-center mt-12">
            <div className="bg-red-600 text-white rounded-2xl p-8 max-w-2xl mx-auto">
              <h3 className="text-2xl font-bold mb-4">24/7 Emergency Helpline</h3>
              <p className="text-xl font-semibold mb-4">+91-XXX-XXX-XXXX</p>
              <p className="opacity-90">For life-threatening emergencies, call immediately or visit our emergency department.</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default ServicesPage;