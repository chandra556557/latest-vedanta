import { Link, useNavigate, useLocation } from 'react-router-dom';
import { ArrowLeft, Star, Award, MapPin, Calendar, Users } from 'lucide-react';
import { useEffect, useState } from 'react';

interface Doctor {
  name: string;
  specialty: string;
  experience: string;
  rating: number;
  education: string;
  location: string;
  image: string;
  achievements: string[];
  availability: string;
  languages: string[];
  patients: string;
  procedures: string;
  about?: string;
}

const DoctorProfilePage: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [doctor, setDoctor] = useState<Doctor | null>(null);
  
  useEffect(() => {
    // Get doctor data from route state
    if (location.state?.doctor) {
      setDoctor(location.state.doctor);
    } else {
      // If no state, redirect to doctors list
      navigate('/doctors', { replace: true });
    }
  }, [location, navigate]);

  if (!doctor) {
    return null; // Show loading state or redirecting message if needed
  }

  return (
    <div className="min-h-screen bg-white">
      <section className="bg-gradient-to-br from-sky-50 to-emerald-50 py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-5xl mx-auto">
            <div className="flex items-center gap-3 mb-6">
              <Link to="/doctors" className="inline-flex items-center text-sky-700 hover:underline">
                <ArrowLeft className="h-4 w-4 mr-1" /> Back to Doctors
              </Link>
            </div>
            <div className="flex flex-col md:flex-row gap-8 items-start">
              <div className="shrink-0">
                <img src={doctor.image} alt={doctor.name} className="w-36 h-36 rounded-full object-cover border border-gray-200" />
              </div>
              <div className="flex-1">
                <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-1">{doctor.name}</h1>
                <p className="text-sky-700 font-semibold mb-2">{doctor.specialty}</p>
                <p className="text-gray-600">{doctor.education}</p>

                <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 mt-6 text-sm">
                  <div className="flex items-center gap-2"><Star className="h-4 w-4 text-yellow-400" /><span className="text-gray-700">{doctor.rating} rating</span></div>
                  <div className="flex items-center gap-2"><Award className="h-4 w-4 text-gray-500" /><span className="text-gray-700">{doctor.experience}</span></div>
                  <div className="flex items-center gap-2"><MapPin className="h-4 w-4 text-gray-500" /><span className="text-gray-700">{doctor.location}</span></div>
                  <div className="flex items-center gap-2"><Calendar className="h-4 w-4 text-gray-500" /><span className="text-gray-700">{doctor.availability}</span></div>
                  <div className="flex items-center gap-2"><Users className="h-4 w-4 text-gray-500" /><span className="text-gray-700">{doctor.patients} Patients</span></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="py-12">
        <div className="container mx-auto px-4">
          <div className="max-w-5xl mx-auto grid md:grid-cols-3 gap-8">
            <div className="md:col-span-2 bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
              <h2 className="text-xl font-semibold text-gray-900 mb-3">About</h2>
              <p className="text-gray-700 leading-relaxed whitespace-pre-line">
                {doctor.about || `${doctor.name} is an experienced ${doctor.specialty.toLowerCase()} with a strong focus on patient-centered care. ${doctor.procedures ? 'Procedures include ' + doctor.procedures + '.' : ''}`}
              </p>

              <h3 className="mt-6 font-semibold text-gray-900">Specializations</h3>
              <div className="mt-2 flex flex-wrap gap-2">
                {doctor.achievements.map((a, i) => (
                  <span key={i} className="bg-sky-50 text-sky-700 px-2 py-1 rounded-full text-xs font-medium">{a}</span>
                ))}
              </div>

              <h3 className="mt-6 font-semibold text-gray-900">Languages</h3>
              <p className="text-gray-700">{doctor.languages.join(', ')}</p>
            </div>

            <div className="md:col-span-1 bg-white rounded-2xl shadow-lg p-6 border border-gray-100 h-max">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Book an Appointment</h2>
              <Link
                to={`/appointment?doctor=${encodeURIComponent(doctor.name)}&specialty=${encodeURIComponent(doctor.specialty)}`}
                className="block text-center bg-sky-600 text-white px-4 py-3 rounded-lg hover:bg-sky-700 transition-colors font-medium"
              >
                Book with {doctor.name}
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default DoctorProfilePage;
