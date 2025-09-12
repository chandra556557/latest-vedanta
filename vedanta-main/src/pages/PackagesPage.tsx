import React, { useState } from 'react';
import { Heart, Users, Clock, CheckCircle, Star, Calendar, Phone, Mail, Shield, Activity, Eye, Brain } from 'lucide-react';
import { motion } from 'framer-motion';

const PackagesPage = () => {
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedPackage, setSelectedPackage] = useState<number | null>(null);

  const packages = [
    {
      id: 1,
      name: 'Basic Health Checkup',
      category: 'basic',
      price: 2500,
      originalPrice: 3500,
      duration: '2-3 hours',
      tests: 25,
      icon: Heart,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
      borderColor: 'border-blue-200',
      description: 'Essential health screening for general wellness monitoring',
      includes: [
        'Complete Blood Count (CBC)',
        'Blood Sugar (Fasting)',
        'Lipid Profile',
        'Liver Function Test',
        'Kidney Function Test',
        'Thyroid Profile (T3, T4, TSH)',
        'Urine Analysis',
        'ECG',
        'Chest X-Ray',
        'General Physical Examination',
        'Doctor Consultation',
        'Health Report with Recommendations'
      ],
      benefits: [
        'Early detection of common health issues',
        'Baseline health assessment',
        'Preventive care guidance',
        'Annual health monitoring'
      ],
      idealFor: 'Adults aged 18-40 years for routine health monitoring'
    },
    {
      id: 2,
      name: 'Comprehensive Kidney Checkup',
      category: 'comprehensive',
      price: 5500,
      originalPrice: 7500,
      duration: '3-4 hours',
      tests: 50,
      icon: Activity,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
      borderColor: 'border-blue-200',
      description: 'Advanced kidney function assessment and early detection of kidney disease',
      includes: [
        'Complete Blood Count with ESR',
        'Kidney Function Tests (12 parameters)', 
        'Urine Analysis (Complete with Microscopy)',
        'Urine Albumin/Creatinine Ratio',
        '24-Hour Urine Protein',
        'Serum Electrolytes (Sodium, Potassium, Chloride)',
        'Serum Uric Acid',
        'Serum Calcium & Phosphorus',
        'Intact PTH (Parathyroid Hormone)',
        'Vitamin D3 Levels',
        'Lipid Profile',
        'HbA1c (Diabetes Screening)',
        'Liver Function Tests',
        'Thyroid Profile (T3, T4, TSH)',
        'Ultrasound KUB (Kidney, Ureter, Bladder)',
        'ECG',
        'Nephrologist Consultation',
        'Dietician Consultation',
        'Blood Pressure Monitoring',
        'Body Composition Analysis',
        'Detailed Kidney Health Report'
      ],
      benefits: [
        'Comprehensive kidney function evaluation',
        'Early detection of kidney disease',
        'Personalized dietary recommendations',
        'Expert nephrology consultation',
        'Prevention of kidney disease progression'
      ],
      idealFor: 'Individuals with diabetes, hypertension, family history of kidney disease, or those on long-term medications'
    },
    {
      id: 3,
      name: 'Renal-Uro-Ortho Executive Checkup',
      category: 'executive',
      price: 18000,
      originalPrice: 25000,
      duration: '4-5 hours',
      tests: 32,
      icon: Activity,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
      borderColor: 'border-blue-200',
      description: 'Comprehensive assessment focusing on kidney, urinary, and musculoskeletal health',
      includes: [
        'NEPHROLOGY TESTS',
        'Complete Kidney Function Panel',
        '24-Hour Urine Protein & Creatinine Clearance',
        'Urine Albumin/Creatinine Ratio',
        'Serum Electrolytes (Sodium, Potassium, Chloride, Bicarbonate)',
        'Renal Ultrasound with Doppler',
        'Estimated GFR (eGFR) Calculation',
        'Serum Uric Acid',
        'Serum Calcium & Phosphorus',
        'Intact PTH (Parathyroid Hormone)',
        'Vitamin D3 (25-Hydroxy)',
        'Autoimmune Markers (ANA, Anti-dsDNA, ANCA)',
        'Serum Protein Electrophoresis',
        'Urine Microscopy & Culture',
        'UROLOGY TESTS',
        'PSA (Prostate Specific Antigen) - For Men',
        'Digital Rectal Exam (DRE) - For Men',
        'Testicular Ultrasound - For Men',
        'Pelvic Ultrasound - For Women',
        'Urine Cytology',
        'Uroflowmetry',
        'Post-Void Residual (PVR) Volume',
        'Cystoscopy (if clinically indicated)',
        'Erectile Function Assessment',
        'Hormonal Profile (Testosterone, FSH, LH, Prolactin)',
        'ORTHOPEDIC TESTS',
        'Bone Profile (Calcium, Phosphorus, Alkaline Phosphatase)',
        'Vitamin D3 & Parathyroid Hormone',
        'Rheumatoid Factor',
        'Anti-CCP Antibody',
        'HLA-B27 (for spondyloarthropathies)',
        'Uric Acid (for gout)',
        'DEXA Scan (Bone Density)',
        'X-Rays (as indicated by symptoms)',
        'MRI Joints (as indicated by symptoms)',
        'Nerve Conduction Studies (if indicated)',
        'CONSULTATIONS',
        'Nephrologist Consultation',
        'Urologist Consultation',
        'Orthopedic Specialist Consultation',
        'Physiotherapist Assessment',
        'Nutritionist Consultation (Renal Diet)'
      ],
      benefits: [
        '✓ Comprehensive kidney function assessment',
        '✓ Early detection of renal disorders',
        '✓ Prostate/urinary health evaluation',
        '✓ Bone and joint health screening',
        '✓ Personalized treatment plans',
        '✓ Multispecialty coordination',
        '✓ Preventive care strategies',
        '✓ Lifestyle modification guidance',
        '✓ Digital health records',
        '✓ Follow-up care planning'
      ],
      idealFor: 'Individuals with family history of kidney disease, urinary issues, or orthopedic concerns; those with diabetes/hypertension; and anyone seeking specialized renal-uro-ortho evaluation'
    },
    {
      id: 4,
      name: 'Diabetic Health Package',
      category: 'specialized',
      price: 1200,
      originalPrice: 1800,
      duration: '2-3 hours',
      tests: 25,
      icon: Activity,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
      borderColor: 'border-blue-200',
      description: 'Comprehensive screening and management for diabetes and related conditions',
      includes: [
        'Fasting Blood Sugar',
        'Post Prandial Blood Sugar',
        'HbA1c (Glycated Hemoglobin)',
        'Complete Blood Count',
        'Lipid Profile',
        'Kidney Function Test',
        'Liver Function Test',
        'Urine Microalbumin',
        'Serum Creatinine',
        'ECG',
        'Fundus Examination',
        'Foot Examination',
        'BMI & Body Composition Analysis',
        'Endocrinologist Consultation',
        'Diabetic Diet Counseling',
        'Lifestyle Management'
      ],
      benefits: [
        'Comprehensive diabetes screening',
        'Early detection of complications',
        'Personalized diet and exercise plan',
        'Expert consultation for diabetes management'
      ],
      idealFor: 'Individuals with diabetes, pre-diabetes, or family history of diabetes'
    },
    {
      id: 5,
      name: 'Women\'s Health Package',
      category: 'specialized',
      price: 4000,
      originalPrice: 5500,
      duration: '3-4 hours',
      tests: 35,
      icon: Users,
      color: 'text-pink-600',
      bgColor: 'bg-pink-50',
      borderColor: 'border-pink-200',
      description: 'Comprehensive health screening designed specifically for women',
      includes: [
        'Complete Blood Count',
        'Comprehensive Metabolic Panel',
        'Thyroid Profile (Complete)',
        'Hormone Profile (FSH, LH, Estrogen, Progesterone)',
        'PCOS Panel',
        'Iron Studies with Ferritin',
        'Vitamin D3, B12, Folate',
        'Pap Smear',
        'Mammography',
        'Pelvic Ultrasound',
        'Bone Density Scan',
        'Breast Examination',
        'Gynecological Consultation',
        'Nutritionist Consultation',
        'Women\'s Health Counseling'
      ],
      benefits: [
        'Gender-specific health screening',
        'Reproductive health assessment',
        'Breast and cervical cancer screening',
        'Hormonal health evaluation'
      ],
      idealFor: 'Women aged 25+ years for comprehensive reproductive and general health'
    },
    {
      id: 6,
      name: 'Senior Citizen Package',
      category: 'specialized',
      price: 5500,
      originalPrice: 7500,
      duration: '4-5 hours',
      tests: 50,
      icon: Shield,
      color: 'text-orange-600',
      bgColor: 'bg-orange-50',
      borderColor: 'border-orange-200',
      description: 'Comprehensive health package tailored for senior citizens',
      includes: [
        'Complete Blood Count with ESR',
        'Comprehensive Metabolic Panel',
        'HbA1c & Glucose Tolerance Test',
        'Complete Lipid Profile',
        'Liver & Kidney Function Tests',
        'Thyroid Profile',
        'Vitamin D3, B12 levels',
        'Prostate Specific Antigen (Men)',
        'Tumor Markers (Basic)',
        'ECG & 2D Echo',
        'Chest X-Ray',
        'Ultrasound Abdomen',
        'Bone Density Scan (DEXA)',
        'Eye Examination',
        'Audiometry',
        'Cognitive Assessment',
        'Geriatrician Consultation',
        'Physiotherapy Assessment',
        'Medication Review',
        'Fall Risk Assessment'
      ],
      benefits: [
        'Age-appropriate health screening',
        'Geriatric specialist consultation',
        'Cognitive and mobility assessment',
        'Medication optimization'
      ],
      idealFor: 'Adults aged 60+ years for comprehensive geriatric health assessment'
    }
  ];

  const categories = [
    { id: 'all', name: 'All Packages', count: packages.length },
    { id: 'basic', name: 'Basic', count: packages.filter(p => p.category === 'basic').length },
    { id: 'comprehensive', name: 'Comprehensive', count: packages.filter(p => p.category === 'comprehensive').length },
    { id: 'executive', name: 'Executive', count: packages.filter(p => p.category === 'executive').length },
    { id: 'specialized', name: 'Specialized', count: packages.filter(p => p.category === 'specialized').length }
  ];

  const filteredPackages = selectedCategory === 'all' 
    ? packages 
    : packages.filter(pkg => pkg.category === selectedCategory);

  const features = [
    {
      icon: Clock,
      title: 'Quick Results',
      description: 'Get your reports within 24-48 hours'
    },
    {
      icon: Shield,
      title: 'NABL Accredited',
      description: 'All tests performed in certified labs'
    },
    {
      icon: Users,
      title: 'Expert Consultation',
      description: 'Specialist doctors review all reports'
    },
    {
      icon: Calendar,
      title: 'Easy Booking',
      description: 'Flexible scheduling as per your convenience'
    }
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
              Health <span className="text-sky-600">Packages</span>
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
              Comprehensive health checkup packages designed to detect health issues early 
              and help you maintain optimal wellness throughout your life.
            </p>
          </motion.div>

          {/* Features */}
          <div className="grid md:grid-cols-4 gap-6 max-w-4xl mx-auto">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="text-center bg-white rounded-xl p-6 shadow-lg"
              >
                <feature.icon className="h-8 w-8 text-sky-600 mx-auto mb-4" />
                <h3 className="font-semibold text-gray-900 mb-2">{feature.title}</h3>
                <p className="text-gray-600 text-sm">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Package Categories */}
      <section className="py-12 bg-white border-b">
        <div className="container mx-auto px-4">
          <div className="flex flex-wrap justify-center gap-4">
            {categories.map((category) => (
              <button
                key={category.id}
                onClick={() => setSelectedCategory(category.id)}
                className={`px-6 py-3 rounded-full font-medium transition-all duration-300 ${
                  selectedCategory === category.id
                    ? 'bg-sky-600 text-white shadow-lg'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {category.name} ({category.count})
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Packages Grid */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="grid lg:grid-cols-2 xl:grid-cols-3 gap-8">
            {filteredPackages.map((pkg, index) => (
              <motion.div
                key={pkg.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className={`${pkg.bgColor} rounded-2xl p-6 border-2 ${pkg.borderColor} hover:shadow-xl transition-all duration-300 hover:-translate-y-1`}
              >
                <div className="flex items-center space-x-4 mb-6">
                  <div className="bg-white p-4 rounded-full shadow-lg">
                    <pkg.icon className={`h-8 w-8 ${pkg.color}`} />
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-gray-900">{pkg.name}</h3>
                    <p className="text-gray-600 text-sm">{pkg.description}</p>
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-4 mb-6">
                  <div className="text-center bg-white/70 rounded-lg p-3">
                    <div className={`text-lg font-bold ${pkg.color}`}>₹{pkg.price.toLocaleString()}</div>
                    <div className="text-xs text-gray-500 line-through">₹{pkg.originalPrice.toLocaleString()}</div>
                  </div>
                  <div className="text-center bg-white/70 rounded-lg p-3">
                    <div className={`text-lg font-bold ${pkg.color}`}>{pkg.tests}</div>
                    <div className="text-xs text-gray-600">Tests</div>
                  </div>
                  <div className="text-center bg-white/70 rounded-lg p-3">
                    <div className={`text-lg font-bold ${pkg.color}`}>{pkg.duration.split('-')[0]}-{pkg.duration.split('-')[1]}</div>
                    <div className="text-xs text-gray-600">Hours</div>
                  </div>
                </div>

                <div className="mb-6">
                  <h4 className="font-semibold text-gray-900 mb-2">Ideal For:</h4>
                  <p className="text-gray-600 text-sm">{pkg.idealFor}</p>
                </div>

                <div className="flex space-x-2 mb-4">
                  <button 
                    onClick={() => setSelectedPackage(selectedPackage === pkg.id ? null : pkg.id)}
                    className="flex-1 bg-white text-gray-900 px-4 py-2 rounded-lg hover:shadow-lg transition-all duration-300 font-medium text-sm"
                  >
                    {selectedPackage === pkg.id ? 'Hide Details' : 'View Details'}
                  </button>
                  <button className={`flex-1 bg-gradient-to-r from-sky-600 to-emerald-600 text-white px-4 py-2 rounded-lg hover:shadow-lg transition-all duration-300 font-medium text-sm`}>
                    Book Now
                  </button>
                </div>

                {selectedPackage === pkg.id && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    exit={{ opacity: 0, height: 0 }}
                    className="bg-white/70 rounded-lg p-4 mt-4"
                  >
                    <h4 className="font-semibold text-gray-900 mb-3">Package Includes:</h4>
                    <div className="grid grid-cols-1 gap-1 max-h-40 overflow-y-auto">
                      {pkg.includes.map((item, i) => (
                        <div key={i} className="flex items-start space-x-2 text-sm">
                          <CheckCircle className="h-3 w-3 text-green-500 mt-1 flex-shrink-0" />
                          <span className="text-gray-700">{item}</span>
                        </div>
                      ))}
                    </div>
                  </motion.div>
                )}
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Booking Section */}
      <section className="py-20 bg-gradient-to-br from-sky-600 to-emerald-600 text-white">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-4xl font-bold mb-6">Ready to Book Your Health Checkup?</h2>
          <p className="text-xl mb-8 opacity-90 max-w-2xl mx-auto">
            Take the first step towards better health. Our packages are designed to give you 
            comprehensive insights into your health status.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center max-w-md mx-auto">
            <button className="bg-white text-sky-600 px-8 py-3 rounded-lg hover:bg-gray-100 transition-colors font-semibold flex items-center justify-center space-x-2">
              <Phone className="h-5 w-5" />
              <span>Call Now</span>
            </button>
            <button className="border border-white text-white px-8 py-3 rounded-lg hover:bg-white/10 transition-colors font-semibold flex items-center justify-center space-x-2">
              <Mail className="h-5 w-5" />
              <span>Email Us</span>
            </button>
          </div>
          <div className="mt-8 text-center">
            <p className="text-lg font-semibold">📞 +91-863-234-5678</p>
            <p className="opacity-90">Available 24/7 for bookings and inquiries</p>
          </div>
        </div>
      </section>
    </div>
  );
};

export default PackagesPage;