import React from 'react';
import { Star, Calendar, Award, MapPin } from 'lucide-react';

const Doctors = () => {
  const doctors = [
    {
      name: 'Dr. Chinta Rama Krishna',
      specialty: 'Nephrologist',
      experience: '15+ years',
      rating: 4.9,
      education: 'MBBS, MD (Nephrology), DM',
      location: 'Guntur',
      image: 'https://vedantahospitals.in/wp-content/uploads/2022/06/team1.png',
      achievements: ['Kidney Surgery Specialist', 'Published 50+ Research Papers'],
      availability: 'Mon - Sat, 9:00 AM - 6:00 PM'
    },
    {
      name: 'Dr. Srinivas Polisetty',
      specialty: 'Orthopedics',
      experience: '10+ years',
      rating: 4.0,
      education: 'M.S Ortho, FAGE, FIJR (South Korea)',
      location: 'Guntur',
      image: 'https://vedantahospitals.in/wp-content/uploads/2023/08/Dr-Srinivas.jpg',
      achievements: ['Fellowship in Joint Replacement', 'Arthroplasty Specialist'],
      availability: 'Mon - Sat, 9:00 AM - 6:00 PM'
    },
    {
      name: 'Dr. K.S.N. Chary',
      specialty: 'Urology',
      experience: '30+ years',
      rating: 4.8,
      education: 'MBBS, MS, MCh (Urology)',
      location: 'Guntur',
      image: 'https://www.asterhospitals.in/sites/default/files/styles/doctors_details_xl/public/2023-06/Dr.K%20S%20Chary.jpg.webp?itok=SDOSZ7nl',
      achievements: [
        'General Urology',
        'Reconstructive Urology',
        'Renal Transplantation',
        'Paediatric Urology',
        'Female Urology',
        'Urodynamics',
        'Past President Apsogus',
        'Association of Southern Urologist',
        'Member of Stone Society of India'
      ],
      availability: 'Mon - Sat, 10:00 AM - 5:00 PM',
    },
    {
      name: 'Dr. Chinta Vasavi',
      specialty: 'Periodontics & Cosmetic Dentistry',
      experience: '18+ years',
      rating: 4.9,
      education: 'BDS, MDS (Periodontics)',
      location: 'Vedanta Hospitals, Guntur',
      image: 'https://vedantahospitals.in/wp-content/uploads/2022/06/team3.png',
      achievements: ['Gum Diseases', 'Dental Implants', 'Smile Designing', 'Cosmetic Dentistry'],
      availability: 'Mon - Sat, 10:00 AM - 2:00 PM & 3:00 PM - 4:00 PM'
    }
  ];

  return (
    <section id="doctors" className="py-20 bg-white" itemScope itemType="https://schema.org/MedicalOrganization">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-4xl lg:text-5xl font-bold text-gray-900 mb-6">
            Meet Our Expert Doctors
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Our team of highly qualified and experienced physicians are committed to providing 
            exceptional healthcare with personalized attention to every patient.
          </p>
        </div>

        <div className="grid lg:grid-cols-2 xl:grid-cols-2 gap-8">
          {doctors.map((doctor, index) => (
            <div
              key={index}
              className="bg-white border border-gray-200 rounded-2xl p-6 hover:shadow-xl transition-all duration-300 hover:-translate-y-1"
              itemScope
              itemType="https://schema.org/Physician"
            >
              <div className="flex flex-col md:flex-row gap-6">
                <div className="md:w-1/3">
                  <div className="relative">
                    <img
                      src={doctor.image}
                      alt={doctor.name}
                      itemProp="image"
                      className="w-full h-48 md:h-full object-cover rounded-xl"
                    />
                    <div className="absolute top-4 right-4 bg-white rounded-full p-2 shadow-lg">
                      <div className="flex items-center space-x-1">
                        <Star className="h-4 w-4 text-yellow-400 fill-current" />
                        <span className="text-sm font-semibold text-gray-700">{doctor.rating}</span>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="md:w-2/3 space-y-4">
                  <div>
                    <h3 className="text-2xl font-bold text-gray-900" itemProp="name">{doctor.name}</h3>
                    <p className="text-sky-600 font-semibold text-lg" itemProp="medicalSpecialty">{doctor.specialty}</p>
                    <p className="text-gray-600" itemProp="qualifications">{doctor.education}</p>
                  </div>

                  <div className="flex items-center space-x-4 text-sm text-gray-600">
                    <div className="flex items-center space-x-1">
                      <Award className="h-4 w-4" />
                      <span>{doctor.experience} Experience</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <MapPin className="h-4 w-4" />
                      <span>{doctor.location}</span>
                    </div>
                  </div>

                  <div>
                    <h4 className="font-semibold text-gray-900 mb-2">Specializations:</h4>
                    <div className="flex flex-wrap gap-2">
                      {doctor.achievements.map((achievement, i) => (
                        <span
                          key={i}
                          className="bg-sky-50 text-sky-700 px-3 py-1 rounded-full text-sm font-medium"
                        >
                          {achievement}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div className="flex items-center space-x-2 text-sm text-gray-600">
                    <Calendar className="h-4 w-4" />
                    <span>Available: {doctor.availability}</span>
                  </div>

                  <div className="flex space-x-3 pt-2">
                    <button className="bg-sky-600 text-white px-6 py-2 rounded-lg hover:bg-sky-700 transition-colors font-medium flex-1">
                      Book Appointment
                    </button>
                    <button 
                      className="border border-sky-600 text-sky-600 px-6 py-2 rounded-lg hover:bg-sky-50 transition-colors font-medium"
                      onClick={() => window.location.href = `/doctor/${doctor.name.replace(/\s+/g, '-').toLowerCase()}`}
                    >
                      View Profile
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Call to Action */}
        <div className="text-center mt-12">
          <button className="bg-emerald-600 text-white px-8 py-3 rounded-lg hover:bg-emerald-700 transition-colors font-semibold">
            View All Doctors
          </button>
        </div>
      </div>
    </section>
  );
};

export default Doctors;