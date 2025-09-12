import React from 'react';
import { Stethoscope, Activity, Bone, UserCheck, Heart } from 'lucide-react';
import { motion } from 'framer-motion';

const Services = () => {
  const services = [
    {
      icon: Stethoscope,
      title: 'Nephrology',
      description: 'Advanced kidney care including dialysis, transplants, CKD management, and stone treatment.',
      color: 'text-sky-700',
      bgColor: 'bg-sky-50',
      borderColor: 'border-sky-200'
    },
    {
      icon: Activity,
      title: 'Urology',
      description: 'Minimally invasive urological procedures, stone management, and reconstructive surgeries.',
      color: 'text-blue-700',
      bgColor: 'bg-blue-50',
      borderColor: 'border-blue-200'
    },
    {
      icon: Bone,
      title: 'Orthopedics',
      description: 'Comprehensive bone, joint and musculoskeletal care including trauma and joint replacement.',
      color: 'text-orange-700',
      bgColor: 'bg-orange-50',
      borderColor: 'border-orange-200'
    },
    {
      icon: UserCheck,
      title: 'General Medicine',
      description: 'Primary care, preventive health and management of common medical conditions.',
      color: 'text-emerald-700',
      bgColor: 'bg-emerald-50',
      borderColor: 'border-emerald-200'
    },
    {
      icon: Heart,
      title: 'Dental Care',
      description: 'Comprehensive dental services including preventive, restorative and cosmetic treatments.',
      color: 'text-purple-700',
      bgColor: 'bg-purple-50',
      borderColor: 'border-purple-200'
    }
  ];

  return (
    <section id="services" className="py-20 bg-gradient-to-br from-gray-50 via-white to-blue-50" itemScope itemType="https://schema.org/MedicalBusiness">
      <div className="container mx-auto px-4">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl lg:text-5xl font-bold bg-gradient-to-r from-gray-900 via-blue-900 to-gray-900 bg-clip-text text-transparent mb-6" itemProp="name">
            Premier Kidney Care & Multi-Specialty Services
          </h2>
          <div className="w-24 h-1 bg-gradient-to-r from-blue-600 to-purple-600 mx-auto mb-6 rounded-full"></div>
          <p className="text-xl text-gray-700 max-w-3xl mx-auto leading-relaxed" itemProp="description">
            Leading nephrology and kidney care center with comprehensive multi-specialty support services for complete patient care.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {services.map((service, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ 
                y: -10,
                scale: 1.02,
                boxShadow: "0 20px 40px rgba(0, 0, 0, 0.1)"
              }}
              className="bg-white/80 backdrop-blur-sm rounded-2xl p-6 shadow-lg border border-white/20 group cursor-pointer"
              itemScope
              itemType="https://schema.org/MedicalSpecialty"
            >
              <motion.div 
                whileHover={{ rotate: 360 }}
                transition={{ duration: 0.6 }}
                className="bg-gradient-to-br from-blue-500 to-purple-600 w-16 h-16 rounded-2xl flex items-center justify-center mb-4 shadow-lg"
              >
                <service.icon className="h-8 w-8 text-white" />
              </motion.div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2" itemProp="name">{service.title}</h3>
              <p className="text-gray-700 leading-relaxed text-sm" itemProp="description">{service.description}</p>
              <div className="mt-4">
                <motion.button 
                  whileHover={{ x: 5 }}
                  className="text-blue-600 hover:text-purple-600 font-medium text-sm transition-colors flex items-center group"
                >
                  Learn More →
                </motion.button>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Additional Features */}
        <div className="grid md:grid-cols-3 gap-8 mt-16">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
            whileHover={{ y: -5 }}
            className="text-center bg-white/60 backdrop-blur-sm rounded-2xl p-8 shadow-lg border border-white/20"
          >
            <div className="bg-gradient-to-br from-blue-500 to-cyan-500 w-20 h-20 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg">
              <Activity className="h-10 w-10 text-white" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Advanced Technology</h3>
            <p className="text-gray-700">Latest medical equipment and diagnostic tools for accurate results.</p>
          </motion.div>
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.4 }}
            whileHover={{ y: -5 }}
            className="text-center bg-white/60 backdrop-blur-sm rounded-2xl p-8 shadow-lg border border-white/20"
          >
            <div className="bg-gradient-to-br from-emerald-500 to-teal-500 w-20 h-20 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg">
              <Heart className="h-10 w-10 text-white" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Compassionate Care</h3>
            <p className="text-gray-700">Patient-centered approach with empathy and understanding.</p>
          </motion.div>
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.6 }}
            whileHover={{ y: -5 }}
            className="text-center bg-white/60 backdrop-blur-sm rounded-2xl p-8 shadow-lg border border-white/20"
          >
            <div className="bg-gradient-to-br from-orange-500 to-red-500 w-20 h-20 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg">
              <UserCheck className="h-10 w-10 text-white" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Expert Physicians</h3>
            <p className="text-gray-700">Highly qualified doctors with extensive experience and expertise.</p>
          </motion.div>
        </div>
      </div>
    </section>
  );
};

export default Services;