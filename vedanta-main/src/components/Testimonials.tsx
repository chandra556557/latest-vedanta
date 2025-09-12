import { useState } from 'react';
import { Play } from 'lucide-react';

type VideoType = {
  id: string;
  title: string;
  description: string;
  thumbnail: string;
  type: 'patient' | 'doctor';
};

const Testimonials = () => {
  // All videos from Vedanta Hospitals
  const allVideos: VideoType[] = [
    // Patient Testimonials
    {
      id: '3vF9PA_vcBQ',
      title: 'Patient Testimonial - Kidney Care',
      description: 'Hear from our patients about their kidney care journey at Vedanta Hospitals.',
      thumbnail: 'https://img.youtube.com/vi/3vF9PA_vcBQ/maxresdefault.jpg',
      type: 'patient'
    },
    {
      id: 'XTXXFVjVTRM',
      title: 'Patient Success Story',
      description: 'A patient shares their successful treatment experience at Vedanta Hospitals.',
      thumbnail: 'https://img.youtube.com/vi/XTXXFVjVTRM/maxresdefault.jpg',
      type: 'patient'
    },
    {
      id: 'eSjep3h0Btk',
      title: 'Comprehensive Healthcare',
      description: 'Learn about our comprehensive healthcare services from our patients.',
      thumbnail: 'https://img.youtube.com/vi/eSjep3h0Btk/maxresdefault.jpg',
      type: 'patient'
    },
    {
      id: 'xAmkv79PwPs',
      title: 'Featured on News',
      description: 'Vedanta Hospitals featured on news for exceptional patient care.',
      thumbnail: 'https://img.youtube.com/vi/xAmkv79PwPs/maxresdefault.jpg',
      type: 'patient'
    },
    // Doctor Interviews
    {
      id: 'Bj3flPRThIc',
      title: 'Meet Our Nephrologist',
      description: 'Interview with our lead nephrologist about advanced kidney care.',
      thumbnail: 'https://img.youtube.com/vi/Bj3flPRThIc/maxresdefault.jpg',
      type: 'doctor'
    },
    {
      id: '71IY8Vl1n8w',
      title: 'Expert Care Team',
      description: 'Our doctors discuss the comprehensive care approach at Vedanta Hospitals.',
      thumbnail: 'https://img.youtube.com/vi/71IY8Vl1n8w/maxresdefault.jpg',
      type: 'doctor'
    },
    {
      id: 'WILPVI_nWBU',
      title: 'Medical Expertise',
      description: 'Our specialists share insights into advanced medical treatments.',
      thumbnail: 'https://img.youtube.com/vi/WILPVI_nWBU/maxresdefault.jpg',
      type: 'doctor'
    },
    {
      id: 'Nln7cExn9pg',
      title: 'Surgical Excellence',
      description: 'Our surgeons discuss minimally invasive surgical techniques.',
      thumbnail: 'https://img.youtube.com/vi/Nln7cExn9pg/maxresdefault.jpg',
      type: 'doctor'
    },
    {
      id: 'sQ2nDkXbJlw',
      title: 'Patient-Centered Care',
      description: 'Our doctors explain the importance of personalized treatment plans.',
      thumbnail: 'https://img.youtube.com/vi/sQ2nDkXbJlw/maxresdefault.jpg',
      type: 'doctor'
    }
  ];

  const [activeTab, setActiveTab] = useState<'patient' | 'doctor'>('patient');
  const [selectedVideo, setSelectedVideo] = useState<string | null>(null);
  const [videoErrors, setVideoErrors] = useState<Record<string, boolean>>({});
  const videos = allVideos.filter(video => video.type === activeTab);

  const handleVideoError = (videoId: string) => {
    setVideoErrors(prev => ({ ...prev, [videoId]: true }));
  };

  return (
    <section id="testimonials" className="py-20 bg-gradient-to-br from-sky-50 to-emerald-50">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-4xl lg:text-5xl font-bold text-gray-900 mb-6">
            Video Gallery
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed mb-8">
            Watch real stories from our patients and insights from our expert doctors.
          </p>
          
          {/* Tab Navigation */}
          <div className="flex justify-center mb-8">
            <div className="inline-flex rounded-lg border border-gray-200 p-1 bg-gray-50">
              <button
                onClick={() => setActiveTab('patient')}
                className={`px-6 py-2 rounded-md text-sm font-medium transition-colors ${
                  activeTab === 'patient' 
                    ? 'bg-white shadow-sm text-sky-600' 
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Patient Testimonials
              </button>
              <button
                onClick={() => setActiveTab('doctor')}
                className={`px-6 py-2 rounded-md text-sm font-medium transition-colors ${
                  activeTab === 'doctor' 
                    ? 'bg-white shadow-sm text-sky-600' 
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Doctor Interviews
              </button>
            </div>
          </div>
        </div>

        {/* Video Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {videos.map((video) => (
            <div 
              key={video.id}
              className="bg-white rounded-xl overflow-hidden shadow-lg hover:shadow-xl transition-all duration-300 cursor-pointer"
              onClick={() => !videoErrors[video.id] && setSelectedVideo(video.id)}
            >
              <div className="relative aspect-video">
                {videoErrors[video.id] ? (
                  <div className="w-full h-full bg-gray-100 flex items-center justify-center p-4 text-center">
                    <p className="text-gray-500">Video coming soon</p>
                  </div>
                ) : (
                  <>
                    <img 
                      src={video.thumbnail} 
                      alt={video.title}
                      className="w-full h-full object-cover"
                      onError={() => handleVideoError(video.id)}
                    />
                    <div className="absolute inset-0 bg-black bg-opacity-30 flex items-center justify-center">
                      <div className="w-16 h-16 bg-white bg-opacity-90 rounded-full flex items-center justify-center">
                        <Play className="h-8 w-8 text-sky-600 ml-1" fill="currentColor" />
                      </div>
                    </div>
                  </>
                )}
              </div>
              <div className="p-4">
                <h3 className="font-semibold text-lg text-gray-900 mb-1 line-clamp-2">
                  {video.title}
                </h3>
                <p className="text-gray-600 text-sm line-clamp-2">
                  {video.description}
                </p>
              </div>
            </div>
          ))}
        </div>

        {/* Video Modal */}
        {selectedVideo && (
          <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4" onClick={() => setSelectedVideo(null)}>
            <div className="relative w-full max-w-4xl" onClick={e => e.stopPropagation()}>
              <button 
                className="absolute -top-10 right-0 text-white hover:text-gray-300"
                onClick={() => setSelectedVideo(null)}
              >
                <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
              </button>
              <div className="aspect-w-16 aspect-h-9">
                <iframe 
                  className="w-full h-[70vh]"
                  src={`https://www.youtube.com/embed/${selectedVideo}?autoplay=1`}
                  title="Video Player"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowFullScreen
                ></iframe>
              </div>
            </div>
          </div>
        )}
        
        {/* Call to Action */}
        <div className="text-center mt-16">
          <h3 className="text-2xl font-semibold text-gray-800 mb-4">
            Share Your Experience With Us
          </h3>
          <a 
            href="https://vedantahospitals.in/contact/" 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-block bg-sky-600 text-white px-8 py-3 rounded-lg hover:bg-sky-700 transition-colors font-semibold"
          >
            Share Your Story
          </a>
        </div>
      </div>
    </section>
  );
};

export default Testimonials;