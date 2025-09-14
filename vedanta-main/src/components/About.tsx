import React from 'react';
import { Shield, Users, Award, Heart, CheckCircle, Target } from 'lucide-react';
import { motion } from 'framer-motion';

const About = () => {
  const stats = [
    { number: '15,000+', label: 'Successful Procedures', icon: Award },
    { number: '10+', label: 'Expert Specialists', icon: Users },
    { number: '100+', label: 'Bed Facility', icon: Heart },
    { number: '24/7', label: 'Emergency Care', icon: Shield }
  ];

  const values = [
    {
      icon: Heart,
      title: 'Patient-Centric Care',
      description: 'We prioritize your health and wellbeing with personalized treatment plans and compassionate care.'
    },
    {
      icon: Shield,
      title: 'Advanced Technology',
      description: 'State-of-the-art facilities with cutting-edge medical technology for accurate diagnosis and treatment.'
    },
    {
      icon: Target,
      title: 'Clinical Excellence',
      description: 'Delivering exceptional healthcare services with a team of highly skilled medical professionals.'
    },
    {
      icon: Users,
      title: 'Teamwork',
      description: 'Collaborative approach among healthcare professionals for optimal patient outcomes.'
    }
  ];

  return (
    <section id="about" className="py-20 bg-gradient-to-br from-amber-50 via-yellow-50 to-amber-100" itemScope itemType="https://schema.org/AboutPage">
      <div className="container mx-auto px-4">
        {/* Header */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl lg:text-5xl font-bold mb-6" itemProp="name">
            Welcome to <span className="text-gold" style={{color: '#C9A227'}}>Vedanta</span> <span className="text-goldDark" style={{color: '#A98500'}}>Hospitals</span>
          </h2>
          <div className="w-24 h-1 bg-gradient-to-r from-gold to-goldDark mx-auto mb-6 rounded-full"></div>
          <p className="text-xl text-gray-700 max-w-3xl mx-auto leading-relaxed" itemProp="description">
            A premier multi-specialty hospital providing comprehensive kidney care and advanced medical treatments 
            with a perfect blend of expertise, innovation, and compassionate care.
          </p>
        </motion.div>

        {/* Main Content */}
        <div className="grid lg:grid-cols-2 gap-16 items-center mb-20">
          <motion.div 
            initial={{ opacity: 0, x: -50 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            className="space-y-6"
          >
            <h3 className="text-3xl font-bold bg-gradient-to-r from-amber-900 to-yellow-800 bg-clip-text text-transparent" itemProp="foundingDate" content="2008">
              Leading Kidney Care Excellence Since 1995
            </h3>
            <p className="text-gray-700 leading-relaxed text-lg">
              At Vedanta Hospitals, we are pioneers in nephrology and kidney care in Andhra Pradesh. 
              Our state-of-the-art facility combines advanced medical technology with compassionate care, 
              offering comprehensive healthcare services across multiple specialties.
            </p>
            <p className="text-gray-700 leading-relaxed text-lg">
              Our dedicated healthcare facility features advanced diagnostic units, specialized treatment facilities, 
              and cutting-edge medical technology. With a team of expert specialists across various disciplines, 
              we provide comprehensive care for a wide range of health conditions.
            </p>

            <div className="space-y-4">
              <motion.div 
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: 0.1 }}
                className="flex items-center space-x-3 p-3 bg-white/80 backdrop-blur-sm rounded-xl shadow-sm border border-amber-200/30"
              >
                <CheckCircle className="h-6 w-6 text-emerald-600" />
                <span className="text-gray-800 font-medium">State-of-the-art dialysis center with 50+ machines</span>
              </motion.div>
              <motion.div 
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: 0.2 }}
                className="flex items-center space-x-3 p-3 bg-white/80 backdrop-blur-sm rounded-xl shadow-sm border border-amber-200/30"
              >
                <CheckCircle className="h-6 w-6 text-emerald-600" />
                <span className="text-gray-800 font-medium">Expert multi-specialty healthcare hospital services with excellent patient outcomes</span>
              </motion.div>
              <motion.div 
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: 0.3 }}
                className="flex items-center space-x-3 p-3 bg-white/80 backdrop-blur-sm rounded-xl shadow-sm border border-amber-200/30"
              >
                <CheckCircle className="h-6 w-6 text-emerald-600" />
                <span className="text-gray-800 font-medium">Advanced stone management with laser technology</span>
              </motion.div>
              <motion.div 
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: 0.4 }}
                className="flex items-center space-x-3 p-3 bg-white/80 backdrop-blur-sm rounded-xl shadow-sm border border-amber-200/30"
              >
                <CheckCircle className="h-6 w-6 text-emerald-600" />
                <span className="text-gray-800 font-medium">24/7 nephrology emergency care and support</span>
              </motion.div>
            </div>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, x: 50 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            className="relative"
          >
            <div className="bg-gradient-to-br from-amber-50 to-yellow-50 rounded-3xl p-8 h-96 shadow-xl border border-amber-200/30">
              <img
                src="https://images.pexels.com/photos/263402/pexels-photo-263402.jpeg?auto=compress&cs=tinysrgb&w=600"
                alt="Hospital building"
                className="w-full h-full object-cover rounded-2xl shadow-2xl"
              />
            </div>
            
            {/* Floating Stats Cards */}
            <motion.div 
              initial={{ opacity: 0, scale: 0.8 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ delay: 0.3 }}
              whileHover={{ scale: 1.05 }}
              className="absolute -bottom-8 -left-8 bg-white/95 backdrop-blur-xl rounded-2xl shadow-2xl p-6 border border-amber-200/30"
            >
              <div className="text-3xl font-bold bg-gradient-to-r from-amber-600 to-yellow-600 bg-clip-text text-transparent">10K+</div>
              <div className="text-sm text-gray-700 font-medium">Successful Surgeries</div>
            </motion.div>
            <motion.div 
              initial={{ opacity: 0, scale: 0.8 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ delay: 0.5 }}
              whileHover={{ scale: 1.05 }}
              className="absolute -top-8 -right-8 bg-white/95 backdrop-blur-xl rounded-2xl shadow-2xl p-6 border border-amber-200/30"
            >
              <div className="text-3xl font-bold bg-gradient-to-r from-yellow-600 to-amber-600 bg-clip-text text-transparent">98%</div>
              <div className="text-sm text-gray-700 font-medium">Patient Satisfaction</div>
            </motion.div>
          </motion.div>
        </div>

        {/* Stats */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 mb-20">
          {stats.map((stat, index) => (
            <motion.div 
              key={index} 
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ 
                y: -10,
                scale: 1.05
              }}
              className="text-center bg-white/80 backdrop-blur-sm rounded-2xl p-6 shadow-lg border border-amber-200/30"
            >
              <div className="bg-gradient-to-br from-amber-500 to-yellow-600 w-20 h-20 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg">
                <stat.icon className="h-10 w-10 text-white" />
              </div>
              <div className="text-3xl font-bold bg-gradient-to-r from-amber-900 to-yellow-800 bg-clip-text text-transparent mb-2">{stat.number}</div>
              <div className="text-gray-700 font-medium">{stat.label}</div>
            </motion.div>
          ))}
        </div>

        {/* Values */}
        <div>
          <motion.h3 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-3xl font-bold bg-gradient-to-r from-amber-900 to-yellow-800 bg-clip-text text-transparent text-center mb-12"
          >
            Our Core Values
          </motion.h3>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {values.map((value, index) => (
              <motion.div 
                key={index} 
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                whileHover={{ 
                  y: -5,
                  scale: 1.02
                }}
                className="text-center bg-white/80 backdrop-blur-sm rounded-2xl p-6 shadow-lg border border-amber-200/30"
              >
                <div className="bg-gradient-to-br from-amber-500 to-yellow-600 w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg">
                  <value.icon className="h-8 w-8 text-white" />
                </div>
                <h4 className="text-xl font-semibold text-gray-900 mb-3">{value.title}</h4>
                <p className="text-gray-700 leading-relaxed text-sm">{value.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default About;