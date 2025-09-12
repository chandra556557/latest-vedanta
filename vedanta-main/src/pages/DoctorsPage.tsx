import { useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import { Star, Calendar, Award, MapPin, Search, Users } from 'lucide-react';
import { motion } from 'framer-motion';
import { doctors } from '../data/doctorsList';

const DoctorsPage = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedSpecialty, setSelectedSpecialty] = useState('all');
  const [selectedLocation, setSelectedLocation] = useState('all');

  // Ensure uniqueness by doctor name to prevent accidental duplicates
  const uniqueDoctors = useMemo(() => {
    const map = new Map<string, typeof doctors[number]>();
    doctors.forEach((d) => {
      if (!map.has(d.name)) map.set(d.name, d);
    });
    return Array.from(map.values());
  }, []);

  const specialties = ['all', ...new Set(uniqueDoctors.map(doctor => doctor.specialty))];
  const locations = ['all', ...new Set(uniqueDoctors.map(doctor => doctor.location))];

  const filteredDoctors = uniqueDoctors.filter(doctor => {
    const matchesSearch = doctor.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         doctor.specialty.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesSpecialty = selectedSpecialty === 'all' || doctor.specialty === selectedSpecialty;
    const matchesLocation = selectedLocation === 'all' || doctor.location === selectedLocation;
    
    return matchesSearch && matchesSpecialty && matchesLocation;
  });

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
              Meet Our Expert <span className="text-sky-600">Doctors</span>
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
              Our team of highly qualified and experienced physicians are committed to providing 
              exceptional healthcare with personalized attention to every patient.
            </p>
          </motion.div>

          {/* Search and Filters */}
          <div className="max-w-4xl mx-auto">
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <div className="grid md:grid-cols-3 gap-4">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                  <input
                    type="text"
                    placeholder="Search doctors..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500 outline-none"
                  />
                </div>
                
                <select
                  value={selectedSpecialty}
                  onChange={(e) => setSelectedSpecialty(e.target.value)}
                  className="px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500 outline-none"
                >
                  {specialties.map(specialty => (
                    <option key={specialty} value={specialty}>
                      {specialty === 'all' ? 'All Specialties' : specialty}
                    </option>
                  ))}
                </select>
                
                <select
                  value={selectedLocation}
                  onChange={(e) => setSelectedLocation(e.target.value)}
                  className="px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500 outline-none"
                >
                  {locations.map(location => (
                    <option key={location} value={location}>
                      {location === 'all' ? 'All Locations' : location}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Doctors Grid */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="grid lg:grid-cols-2 xl:grid-cols-3 gap-8">
            {filteredDoctors.map((doctor, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="bg-white border border-gray-200 rounded-2xl p-6 hover:shadow-xl transition-all duration-300 hover:-translate-y-1"
              >
                <div className="flex flex-col items-center text-center mb-6">
                  <div className="relative mb-4">
                    <img
                      src={doctor.image}
                      alt={doctor.name}
                      className="w-24 h-24 object-cover rounded-full"
                    />
                    <div className="absolute -top-2 -right-2 bg-white rounded-full p-2 shadow-lg">
                      <div className="flex items-center space-x-1">
                        <Star className="h-4 w-4 text-yellow-400 fill-current" />
                        <span className="text-sm font-semibold text-gray-700">{doctor.rating}</span>
                      </div>
                    </div>
                  </div>
                  
                  <h3 className="text-xl font-bold text-gray-900 mb-1">{doctor.name}</h3>
                  <p className="text-sky-600 font-semibold mb-2">{doctor.specialty}</p>
                  <p className="text-gray-600 text-sm">{doctor.education}</p>
                </div>

                <div className="space-y-4 mb-6">
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div className="flex items-center space-x-2">
                      <Award className="h-4 w-4 text-gray-500" />
                      <span className="text-gray-600">{doctor.experience}</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <MapPin className="h-4 w-4 text-gray-500" />
                      <span className="text-gray-600">{doctor.location}</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Users className="h-4 w-4 text-gray-500" />
                      <span className="text-gray-600">{doctor.patients} Patients</span>
                    </div>
                  </div>

                  <div>
                    <h4 className="font-semibold text-gray-900 mb-2 text-sm">Specializations:</h4>
                    <div className="flex flex-wrap gap-1">
                      {doctor.achievements.map((achievement, i) => (
                        <span
                          key={i}
                          className="bg-sky-50 text-sky-700 px-2 py-1 rounded-full text-xs font-medium"
                        >
                          {achievement}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div className="flex items-center space-x-2 text-sm text-gray-600">
                    <Calendar className="h-4 w-4" />
                    <span>{doctor.availability}</span>
                  </div>

                  <div>
                    <h4 className="font-semibold text-gray-900 mb-1 text-sm">Languages:</h4>
                    <p className="text-gray-600 text-sm">{doctor.languages.join(', ')}</p>
                  </div>
                </div>

                <div className="flex space-x-2">
                  <Link
                    to={`/appointment?doctor=${encodeURIComponent(doctor.name)}&specialty=${encodeURIComponent(doctor.specialty)}`}
                    className="bg-sky-600 text-white px-4 py-2 rounded-lg hover:bg-sky-700 transition-colors font-medium flex-1 text-sm text-center"
                    aria-label={`Book appointment with ${doctor.name}`}
                  >
                    Book Appointment
                  </Link>
                  <Link
                    to={`/doctor/${doctor.name.toLowerCase().replace(/\s+/g, '-')}`}
                    state={{ doctor }}
                    className="border border-sky-600 text-sky-600 px-4 py-2 rounded-lg hover:bg-sky-50 transition-colors font-medium text-sm text-center"
                    aria-label={`View profile of ${doctor.name}`}
                  >
                    View Profile
                  </Link>
                </div>
              </motion.div>
            ))}
          </div>

          {filteredDoctors.length === 0 && (
            <div className="text-center py-12">
              <p className="text-gray-500 text-lg">No doctors found matching your criteria.</p>
            </div>
          )}
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-br from-sky-50 to-emerald-50">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold text-gray-900 mb-6">Can't Find the Right Doctor?</h2>
          <p className="text-gray-600 mb-8 max-w-2xl mx-auto">
            Our patient care team is here to help you find the perfect specialist for your needs. 
            Contact us for personalized assistance.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="bg-sky-600 text-white px-8 py-3 rounded-lg hover:bg-sky-700 transition-colors font-semibold">
              Contact Patient Care
            </button>
            <button className="border border-sky-600 text-sky-600 px-8 py-3 rounded-lg hover:bg-sky-50 transition-colors font-semibold">
              Request Callback
            </button>
          </div>
        </div>
      </section>
    </div>
  );
};

export default DoctorsPage;