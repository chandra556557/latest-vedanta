import React from 'react';
import { ArrowRight, Shield, Bot, TrendingUp, Play, Star, CheckCircle, Volume2, VolumeX } from 'lucide-react';
import { motion } from 'framer-motion';

const Hero = () => {
  const [isMuted, setIsMuted] = React.useState(true);
  const videoRef = React.useRef<HTMLVideoElement>(null);
  const [liveStats, setLiveStats] = React.useState({
    doctors: 50,
    patients: 10247,
    specialties: 25,
    experience: 15
  });

  // Simulate real-time updates
  React.useEffect(() => {
    const interval = setInterval(() => {
      setLiveStats(prev => ({
        ...prev,
        patients: prev.patients + Math.floor(Math.random() * 3)
      }));
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const toggleMute = () => {
    if (videoRef.current) {
      videoRef.current.muted = !videoRef.current.muted;
      setIsMuted(videoRef.current.muted);
    }
  };

  return (
    <section id="home" className="relative bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 py-20 overflow-hidden">
      {/* Background Video Layer */}
      <div className="absolute inset-0 overflow-hidden z-0">
        <video
          ref={videoRef}
          className="w-full h-full object-cover"
          src="/videos/home-background.mp4"
          autoPlay
          muted={isMuted}
          loop
          playsInline
        />
        {/* Dark overlay for readability */}
        <div className="absolute inset-0 bg-black/35" />
      </div>

      {/* Logo */}
      <div className="absolute top-8 left-1/2 transform -translate-x-1/2 z-10">
        <div className="flex items-center">
          <span className="text-4xl font-bold text-sky-600">Vedanta</span>
          <span className="text-4xl font-bold text-emerald-600 ml-1">Hospitals</span>
        </div>
      </div>
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute inset-0" style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='80' height='80' viewBox='0 0 80 80' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23000000' fill-opacity='0.03'%3E%3Cpath d='M40 40c0-11.046-8.954-20-20-20s-20 8.954-20 20 8.954 20 20 20 20-8.954 20-20zm20 0c0-11.046-8.954-20-20-20s-20 8.954-20 20 8.954 20 20 20 20-8.954 20-20z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`
        }}></div>
      </div>

      {/* Video Controls */}
      <button
        onClick={toggleMute}
        className="absolute top-6 right-6 z-20 bg-black/50 backdrop-blur-sm text-white p-3 rounded-full hover:bg-black/70 transition-all duration-300"
        aria-label={isMuted ? 'Unmute video' : 'Mute video'}
      >
        {isMuted ? <VolumeX className="h-5 w-5" /> : <Volume2 className="h-5 w-5" />}
      </button>

      {/* Floating Elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        {/* Kidney-shaped floating elements */}
        <motion.div
          animate={{ 
            y: [0, -30, 0],
            rotate: [0, 10, 0],
            scale: [1, 1.1, 1]
          }}
          transition={{ 
            duration: 8,
            repeat: Infinity,
            ease: "easeInOut"
          }}
          className="absolute top-20 left-10 w-24 h-32 bg-gradient-to-br from-red-400/40 to-pink-400/40 rounded-full blur-lg"
          style={{
            borderRadius: '50% 50% 50% 50% / 60% 60% 40% 40%',
            transform: 'rotate(-20deg)'
          }}
        />
        <motion.div
          animate={{ 
            y: [0, 25, 0],
            rotate: [0, -15, 0],
            scale: [1, 0.9, 1]
          }}
          transition={{ 
            duration: 10,
            repeat: Infinity,
            ease: "easeInOut",
            delay: 3
          }}
          className="absolute top-40 right-20 w-28 h-36 bg-gradient-to-br from-red-500/30 to-orange-400/30 rounded-full blur-lg"
          style={{
            borderRadius: '50% 50% 50% 50% / 60% 60% 40% 40%',
            transform: 'rotate(15deg)'
          }}
        />
        <motion.div
          animate={{ 
            y: [0, -20, 0],
            x: [0, 15, 0],
            rotate: [0, 8, 0]
          }}
          transition={{ 
            duration: 9,
            repeat: Infinity,
            ease: "easeInOut",
            delay: 6
          }}
          className="absolute bottom-20 left-1/4 w-20 h-28 bg-gradient-to-br from-pink-400/40 to-red-400/40 rounded-full blur-lg"
          style={{
            borderRadius: '50% 50% 50% 50% / 60% 60% 40% 40%',
            transform: 'rotate(-10deg)'
          }}
        />
        
        {/* Medical cross animations */}
        <motion.div
          animate={{ 
            rotate: [0, 360],
            scale: [1, 1.2, 1]
          }}
          transition={{ 
            duration: 12,
            repeat: Infinity,
            ease: "linear"
          }}
          className="absolute top-1/3 left-1/3 w-16 h-16 opacity-20"
        >
          <div className="w-full h-full relative">
            <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-12 h-3 bg-white/40 rounded-full"></div>
            <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-3 h-12 bg-white/40 rounded-full"></div>
          </div>
        </motion.div>
        
        {/* Heartbeat line animation */}
        <motion.div
          animate={{ 
            scaleX: [1, 1.5, 1],
            opacity: [0.3, 0.7, 0.3]
          }}
          transition={{ 
            duration: 2,
            repeat: Infinity,
            ease: "easeInOut"
          }}
          className="absolute bottom-1/3 right-1/3 w-32 h-1 bg-gradient-to-r from-red-400/50 to-pink-400/50 rounded-full"
        />
      </div>

      <header className="container mx-auto px-4 relative z-10">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div 
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 1, ease: "easeOut" }}
            className="space-y-8"
          >
            {/* Trust Indicators */}
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="flex flex-wrap justify-center items-center space-x-6 mb-4"
            >
              <div className="flex items-center space-x-2 bg-white/95 backdrop-blur-sm px-4 py-2 rounded-full shadow-lg border border-amber-200">
                <Star className="h-4 w-4 text-yellow-500 fill-current" />
                <span className="text-sm font-semibold text-gray-800">4.9/5 Rating</span>
              </div>
              <div className="flex items-center space-x-2 bg-white/95 backdrop-blur-sm px-4 py-2 rounded-full shadow-lg border border-amber-200">
                <CheckCircle className="h-4 w-4 text-green-500" />
                <span className="text-sm font-semibold text-gray-800">NABH Accredited</span>
              </div>
              <div className="flex items-center space-x-2 bg-white/95 backdrop-blur-sm px-4 py-2 rounded-full shadow-lg border border-amber-200">
                <Shield className="h-4 w-4 text-blue-500" />
                <span className="text-sm font-semibold text-gray-800">29+ Years</span>
              </div>
            </motion.div>

            <div className="space-y-8 mx-auto">
              <motion.h1 
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2, duration: 0.8 }}
                className="text-4xl lg:text-5xl font-bold text-white leading-tight drop-shadow-2xl"
              >
                <span className="bg-gradient-to-r from-amber-400 via-yellow-400 to-amber-500 bg-clip-text text-transparent">
                  Every Patient Matters, Every Recovery Inspires Us to Achieve the Impossible
                </span>
              </motion.h1>
              <motion.p 
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4, duration: 0.8 }}
                className="text-xl text-white/90 leading-relaxed max-w-2xl drop-shadow-lg"
              >
                Our deep medical expertise, advanced technology, and Modern Medical infrastructure transform complex diseases into stories of hope - making your healing journey our proudest achievement.
              </motion.p>
            </div>

            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6, duration: 0.8 }}
              className="flex flex-col sm:flex-row gap-4 justify-center"
            >

            </motion.div>

            {/* Stats */}
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.8, duration: 0.8 }}
              className="grid grid-cols-2 md:grid-cols-4 gap-6 pt-8 bg-white/10 backdrop-blur-md rounded-2xl p-6 shadow-2xl border border-white/20"
            >
              <motion.div 
                whileHover={{ 
                  y: -5,
                  scale: 1.05
                }}
                transition={{ type: "spring", stiffness: 300 }}
                className="text-center"
              >
                <div className="text-3xl font-bold text-white drop-shadow-lg">{liveStats.doctors}+</div>
                <div className="text-sm text-white/80 mt-1 font-medium">Expert Doctors</div>
              </motion.div>
              <motion.div 
                whileHover={{ 
                  y: -5,
                  scale: 1.05,
                  boxShadow: "0 10px 30px rgba(239, 68, 68, 0.3)"
                }}
                transition={{ type: "spring", stiffness: 300 }}
                className="text-center relative"
              >
                {/* Animated kidney icon for patients stat */}
                <motion.div
                  animate={{ 
                    y: [0, -3, 0],
                    rotate: [0, 5, 0]
                  }}
                  transition={{ 
                    duration: 2,
                    repeat: Infinity,
                    ease: "easeInOut",
                    delay: 0.5
                  }}
                  className="absolute -top-2 -right-2 text-lg opacity-60"
                >
                  🫀
                </motion.div>
                <div className="text-3xl font-bold text-white drop-shadow-lg flex items-center justify-center">
                  {(liveStats.patients / 1000).toFixed(1)}K+
                  <motion.div
                    animate={{ 
                      y: [0, -2, 0],
                      scale: [1, 1.1, 1]
                    }}
                    transition={{ 
                      duration: 1.5,
                      repeat: Infinity,
                      ease: "easeInOut"
                    }}
                  >
                    <TrendingUp className="h-4 w-4 ml-1 text-red-400" />
                  </motion.div>
                </div>
                <div className="text-sm text-white/80 mt-1 font-medium">Transplant Patients</div>
              </motion.div>
              <motion.div 
                whileHover={{ 
                  y: -5,
                  scale: 1.05
                }}
                transition={{ type: "spring", stiffness: 300 }}
                className="text-center"
              >
                <div className="text-3xl font-bold text-white drop-shadow-lg">{liveStats.specialties}+</div>
                <div className="text-sm text-white/80 mt-1 font-medium">Specialities</div>
              </motion.div>
              <motion.div 
                whileHover={{ 
                  y: -5,
                  scale: 1.05
                }}
                transition={{ type: "spring", stiffness: 300 }}
                className="text-center"
              >
                <div className="text-3xl font-bold text-white drop-shadow-lg">{liveStats.experience}+</div>
                <div className="text-sm text-white/80 mt-1 font-medium">Years Experience</div>
              </motion.div>
            </motion.div>

            {/* Specialty Focus Banner */}
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 1, duration: 0.8 }}
              className="relative bg-gradient-to-r from-red-600/90 via-pink-600/90 to-red-700/90 backdrop-blur-sm rounded-2xl p-6 shadow-2xl border border-red-400/30 overflow-hidden"
            >
              {/* Animated kidney icon */}
              <motion.div
                animate={{ 
                  scale: [1, 1.1, 1],
                  rotate: [0, 5, 0]
                }}
                transition={{ 
                  duration: 3,
                  repeat: Infinity,
                  ease: "easeInOut"
                }}
                className="absolute top-2 right-4 text-4xl opacity-30"
              >
                🫀
              </motion.div>
              
              {/* Pulsing background effect */}
              <motion.div
                animate={{ 
                  scale: [1, 1.05, 1],
                  opacity: [0.1, 0.3, 0.1]
                }}
                transition={{ 
                  duration: 4,
                  repeat: Infinity,
                  ease: "easeInOut"
                }}
                className="absolute inset-0 bg-gradient-to-r from-red-400/20 to-pink-400/20 rounded-2xl"
              />
              
              <div className="relative z-10">
                <motion.h3 
                  animate={{ 
                    textShadow: [
                      "0 0 10px rgba(255,255,255,0.5)",
                      "0 0 20px rgba(255,255,255,0.8)",
                      "0 0 10px rgba(255,255,255,0.5)"
                    ]
                  }}
                  transition={{ 
                    duration: 2,
                    repeat: Infinity,
                    ease: "easeInOut"
                  }}
                  className="text-2xl font-bold text-white mb-2"
                >
                  Multispeciality Hospital with precision and compassionate care
                </motion.h3>
              </div>
              <p className="text-white/90 text-lg">
                Nephrology • Kidney Transplant • Urology • Critical Care • General Medicine • Orthopaedics and Joint Replacement • Paediatrics and Neonatology • Cardiology and Neurology
              </p>
            </motion.div>
          </motion.div>
        </div>
      </header>

      {/* Scroll Indicator */}
      <motion.div 
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.5 }}
        className="absolute bottom-8 left-1/2 transform -translate-x-1/2 z-10"
      >
        <motion.div
          animate={{ y: [0, 10, 0] }}
          transition={{ duration: 2, repeat: Infinity }}
          className="w-6 h-10 border-2 border-white/50 rounded-full flex justify-center"
        >
          <motion.div
            animate={{ y: [0, 12, 0] }}
            transition={{ duration: 2, repeat: Infinity }}
            className="w-1 h-3 bg-white/70 rounded-full mt-2"
          />
        </motion.div>
      </motion.div>
    </section>
  );
};

export default Hero;