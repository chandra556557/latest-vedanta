import { Shield, Users, Award, Heart, CheckCircle, TrendingUp, Activity, Clock } from 'lucide-react';
import { motion } from 'framer-motion';
import About from '../components/About';
import vedantaLogo from '../assets/images/vedanta-logo.jpg';
import BlogGallery from '../components/BlogGallery';
import EquipmentGallery from '../components/EquipmentGallery';

const AboutPage = () => {
  const leadership = [
    {
      name: 'Dr. Chinta Rama Krishna',
      position: 'Chairman & Managing Director',
      image: 'https://vedantahospitals.in/wp-content/uploads/2023/08/dr-rk.jpg',
      bio: 'Distinguished nephrologist and healthcare leader with 15+ years of clinical expertise. As Founder & CEO of Vedanta Hospitals and HelloKidney.ai, he leads one of the most comprehensive renal care services in coastal Andhra Pradesh.'
    },
    {
      name: 'Dr. Srinivas Polisetty',
      position: 'orthopedic surgeon',
      image: 'https://vedantahospitals.in/wp-content/uploads/2023/08/Dr-Srinivas.jpg',
      bio: 'Enhanced achievements list with "Minimally Invasive Surgeries" and "Rapid Recovery Procedures"Added "Knee Replacement" to procedures.'
    },
    {
      name: 'Dr. K.S.N. Chary',
      position: 'Senior Consultant Urologist',
      image: 'https://www.asterhospitals.in/sites/default/files/styles/doctors_details_xl/public/2023-06/Dr.K%20S%20Chary.jpg.webp?itok=SDOSZ7nl',
      bio: 'Distinguished urologist with over 30 years of experience, specializing in General Urology, Reconstructive Urology, and Renal Transplantation. Past President of Apsogus and active member of the Association of Southern Urologists.'
    }
  ];

  const achievements = [
    { icon: Award, title: 'NABH Accreditation', description: 'National Accreditation Board for Hospitals certification' },
    { icon: Shield, title: 'NABH Accredited', description: 'National quality assurance recognition' },
    { icon: TrendingUp, title: 'ISO 9001:2015', description: 'Quality management system certification' },
    { icon: Heart, title: 'Best Multi-Specialty Hospital', description: 'Regional Healthcare Excellence Award' }
  ];

  return (
    <div className="min-h-screen bg-white">
      {/* Shared About section (reused from Home) */}
      <About />
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-sky-50 to-emerald-50 py-20">
        <div className="container mx-auto px-4">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center mb-16"
          >
            <div className="flex justify-center mb-8">
              <img 
                src={vedantaLogo}
                alt="Vedanta Hospitals Logo" 
                className="h-24 w-auto"
                onError={(e) => {
                  console.error('Failed to load image:', e.currentTarget.src);
                }}
              />
            </div>
            <h1 className="text-5xl lg:text-6xl font-bold text-gray-900 mb-6">
              About <span className="text-sky-600">Vedanta Hospitals</span>
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
              Pioneering healthcare excellence since 1995, combining cutting-edge medical technology 
              with compassionate care to serve the community in Guntur and surrounding regions.
            </p>
          </motion.div>

          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <motion.div 
              initial={{ opacity: 0, x: -50 }}
              animate={{ opacity: 1, x: 0 }}
              className="space-y-6"
            >
              <h2 className="text-3xl font-bold text-gray-900">Our Mission</h2>
              <p className="text-gray-600 leading-relaxed">
                To provide accessible, affordable, and quality healthcare services to all sections of society. 
                We are committed to delivering compassionate care with the highest standards of medical excellence, 
                ensuring the well-being of our patients and their families.
              </p>
              
              <h2 className="text-3xl font-bold text-gray-900">Our Vision</h2>
              <p className="text-gray-600 leading-relaxed">
                To be the most trusted healthcare provider in Andhra Pradesh, recognized for our commitment 
                to medical excellence, patient safety, and community health in Guntur and surrounding regions.
              </p>

              <h2 className="text-3xl font-bold text-gray-900">Our Values</h2>
              <div className="space-y-3">
                <div className="flex items-start space-x-3">
                  <CheckCircle className="h-6 w-6 text-emerald-600 mt-1" />
                  <div>
                    <h3 className="font-semibold text-gray-900">Compassionate Care</h3>
                    <p className="text-gray-600">Treating every patient with empathy, respect, and dignity</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <CheckCircle className="h-6 w-6 text-emerald-600 mt-1" />
                  <div>
                    <h3 className="font-semibold text-gray-900">Medical Excellence</h3>
                    <p className="text-gray-600">Maintaining the highest standards of clinical care and safety</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <CheckCircle className="h-6 w-6 text-emerald-600 mt-1" />
                  <div>
                    <h3 className="font-semibold text-gray-900">Community Service</h3>
                    <p className="text-gray-600">Contributing to the health and well-being of our community</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <CheckCircle className="h-6 w-6 text-emerald-600 mt-1" />
                  <div>
                    <h3 className="font-semibold text-gray-900">Continuous Innovation</h3>
                    <p className="text-gray-600">Embracing new technologies and treatment methods</p>
                  </div>
                </div>
              </div>
            </motion.div>

            <motion.div 
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              className="relative"
            >
              <img
                src="https://vedantahospitals.in/wp-content/uploads/2022/06/PHOTO-2022-06-13-16-49-16.jpg"
                alt="Hospital building"
                className="w-full h-96 object-cover rounded-2xl shadow-lg"
              />
            </motion.div>
          </div>
        </div>
      </section>

      

      {/* Leadership Section */}
      <section className="py-20 bg-white">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-gray-900 text-center mb-16">Leadership Team</h2>
          <p className="text-center text-gray-600 mb-12 max-w-2xl mx-auto">
            Our experienced leadership team brings together decades of healthcare expertise, 
            medical knowledge, and administrative excellence to guide Vedanta Hospitals.
          </p>
          <div className="grid md:grid-cols-3 gap-8">
            {leadership.map((leader, index) => (
              <motion.div 
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="text-center"
              >
                <img
                  src={leader.image}
                  alt={leader.name}
                  className="w-48 h-48 object-cover rounded-full mx-auto mb-6"
                />
                <h3 className="text-xl font-bold text-gray-900 mb-2">{leader.name}</h3>
                <p className="text-sky-600 font-medium mb-4">{leader.position}</p>
                <p className="text-gray-600 text-sm">{leader.bio}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Achievements Section */}
      <section className="py-20 bg-gradient-to-br from-sky-50 to-emerald-50">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-gray-900 text-center mb-16">Awards & Certifications</h2>
          <p className="text-center text-gray-600 mb-12 max-w-2xl mx-auto">
            Our commitment to quality healthcare has been recognized through various accreditations 
            and awards from national and regional healthcare organizations.
          </p>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {achievements.map((achievement, index) => (
              <motion.div 
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="text-center bg-white p-6 rounded-xl shadow-lg"
              >
                <achievement.icon className="h-12 w-12 text-sky-600 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-gray-900 mb-2">{achievement.title}</h3>
                <p className="text-gray-600 text-sm">{achievement.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Blog Gallery Section */}
      <section className="py-20 bg-white">
        <div className="container mx-auto px-4">
          <BlogGallery />
        </div>
      </section>

      {/* Why Choose Us Section */}
      <section className="py-20 bg-white">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-gray-900 text-center mb-16">Why Choose Vedanta Hospitals</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="text-center p-6"
            >
              <div className="bg-sky-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Users className="h-8 w-8 text-sky-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">Experienced Team</h3>
              <p className="text-gray-600">Highly qualified doctors and healthcare professionals with years of experience</p>
            </motion.div>
            
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="text-center p-6"
            >
              <div className="bg-emerald-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Activity className="h-8 w-8 text-emerald-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">Advanced Technology</h3>
              <p className="text-gray-600">State-of-the-art medical equipment and modern diagnostic facilities</p>
            </motion.div>
            
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="text-center p-6"
            >
              <div className="bg-purple-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Heart className="h-8 w-8 text-purple-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">Compassionate Care</h3>
              <p className="text-gray-600">Patient-centered approach with personalized attention and care</p>
            </motion.div>
            
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="text-center p-6"
            >
              <div className="bg-orange-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Clock className="h-8 w-8 text-orange-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">24/7 Emergency</h3>
              <p className="text-gray-600">Round-the-clock emergency services and critical care facilities</p>
            </motion.div>
            
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="text-center p-6"
            >
              <div className="bg-red-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Shield className="h-8 w-8 text-red-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">Quality Assurance</h3>
              <p className="text-gray-600">NABH accredited hospital maintaining highest quality standards</p>
            </motion.div>
            
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
              className="text-center p-6"
            >
              <div className="bg-teal-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Award className="h-8 w-8 text-teal-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">Affordable Care</h3>
              <p className="text-gray-600">Quality healthcare services at affordable prices for all sections of society</p>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Equipment Gallery Section */}
      <section className="py-16 bg-gray-50">
        <div className="container mx-auto px-4">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
            className="text-center mb-12"
          >
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Our Advanced Medical Equipment</h2>
            <div className="w-24 h-1 bg-blue-600 mx-auto mb-6"></div>
            <p className="text-lg text-gray-600 max-w-3xl mx-auto">
              Explore our state-of-the-art medical technology and facilities that help us deliver exceptional healthcare services.
            </p>
          </motion.div>
          <EquipmentGallery />
        </div>
      </section>
    </div>
  );
};

export default AboutPage;