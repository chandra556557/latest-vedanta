import { useState, useEffect } from 'react';
import { Menu, X, Phone, Clock, MapPin, ChevronDown, Search } from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';
import vedantaLogo from '../assets/images/vedanta-logo.jpg';

const Navigation = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [activeDropdown, setActiveDropdown] = useState<string | null>(null);
  const [isScrolled, setIsScrolled] = useState(false);
  const location = useLocation();

  // Handle scroll effect for header
  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const toggleDropdown = (path: string) => {
    setActiveDropdown(activeDropdown === path ? null : path);
  };

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  const navigationItems = [
    { path: '/', label: 'Home' },
    { 
      path: '/about', 
      label: 'About',
      dropdown: [
        { path: '/about', label: 'About Us' },
        { path: '/blog', label: 'Blog' },
        { path: '/news', label: 'News & Updates' },
        { path: '/testimonials', label: 'Testimonials' },
        { path: '/gallery', label: 'Gallery' }
      ]
    },
    { 
      path: '/services', 
      label: 'Services',
      dropdown: [
        { path: '/services/nephrology', label: 'Nephrology' },
        { path: '/services/urology', label: 'Urology' },
        { path: '/services/orthopedics', label: 'Orthopedics' },
        { path: '/services/general-medicine', label: 'General Medicine' },
        { path: '/services/dental-care', label: 'Dental Care' },
        { path: '/services/emergency', label: 'Emergency Care' },
        { path: '/services/icu', label: 'Intensive Care' }
      ]
    },
    { 
      path: '/doctors', 
      label: 'Doctors',
      dropdown: [
        { path: '/doctors', label: 'All Doctors' },
        { path: '/doctors/nephrology', label: 'Nephrology' },
        { path: '/doctors/urology', label: 'Urology' },
        { path: '/doctors/orthopedics', label: 'Orthopedics' },
        { path: '/doctors/general-medicine', label: 'General Medicine' },
        { path: '/doctors/dental-care', label: 'Dental Care' }
      ]
    },
    { 
      path: '/patient-info', 
      label: 'Patient Info',
      dropdown: [
        { path: '/patient-info/visiting-hours', label: 'Visiting Hours' },
        { path: '/patient-info/admission', label: 'Admission Process' },
        { path: '/patient-info/insurance', label: 'Insurance' },
        { path: '/patient-info/faq', label: 'FAQs' }
      ]
    },
    { path: '/contact', label: 'Contact' }
  ];

  return (
    <header 
      className={`sticky top-0 z-50 transition-all duration-300 ${
        isScrolled ? 'bg-white shadow-md' : 'bg-white/95 backdrop-blur-sm'
      }`}
      role="banner"
    >
      {/* Top Bar */}
      <div className="bg-gold text-white text-sm py-2">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex flex-wrap justify-center md:justify-start items-center gap-x-6 gap-y-2">
              <div className="flex items-center space-x-2">
                <Phone className="h-4 w-4 text-white/80" />
                <span>Emergency: +91-XXX-XXX-XXXX</span>
              </div>
              <div className="hidden md:flex items-center space-x-2">
                <Clock className="h-4 w-4 text-white/80" />
                <span>24/7 Emergency Services</span>
              </div>
              <div className="hidden lg:flex items-center space-x-2">
                <MapPin className="h-4 w-4 text-white/80" />
                <span>Guntur, Andhra Pradesh 522001</span>
              </div>
            </div>
            
            <div className="flex items-center space-x-4 ml-auto">
              <a href="mailto:info@vedantahospitals.com" className="flex items-center space-x-1 text-white/90 hover:text-white transition-colors">
                <span>Email : info@vedantahospitals.com</span>
              </a>
              {/* Removed Patient Login link */}
            </div>
          </div>
        </div>
      </div>

      {/* Main Navigation */}
      <nav className="container mx-auto px-4 py-3" role="navigation" aria-label="Main navigation">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <Link to="/" className="flex items-center">
              <img 
                src={vedantaLogo} 
                alt="Vedanta Hospital Logo" 
                className="h-12 w-12 mr-3 rounded-full object-cover shadow-md"
              />
              <div className="text-2xl font-bold mr-12">
                <span className="text-gold" style={{color: '#C9A227'}}>Vedanta</span>
                <span className="text-goldDark ml-1" style={{color: '#A98500'}}>Hospitals</span>
              </div>
            </Link>

            {/* Desktop Navigation */}
            <div className="hidden lg:flex items-center space-x-1">
              {navigationItems.map((item) => (
                <div key={item.path} className="relative group">
                  {item.dropdown ? (
                    <div
                      className="relative"
                      onMouseEnter={() => setActiveDropdown(item.path)}
                      onMouseLeave={() => setActiveDropdown(null)}
                    >
                      <button 
                        className={`flex items-center space-x-1 px-4 py-3 font-medium transition-colors whitespace-nowrap rounded-md ${
                          isActive(item.path) 
                            ? 'text-goldDark bg-ivory' 
                            : 'text-gray-700 hover:text-goldDark hover:bg-ivory'
                        }`}
                        onClick={() => toggleDropdown(item.path)}
                      >
                        <span>{item.label}</span>
                        <ChevronDown className={`h-4 w-4 transition-transform ${activeDropdown === item.path ? 'rotate-180' : ''}`} />
                      </button>
                      {activeDropdown === item.path && (
                        <div 
                          className="absolute top-full left-0 w-56 bg-ivory backdrop-blur-md rounded-lg shadow-2xl border border-goldDark py-2 z-50 animate-fadeIn"
                          onMouseEnter={() => setActiveDropdown(item.path)}
                        >
                          {item.dropdown.map((dropdownItem) => (
                            <Link
                              key={dropdownItem.path}
                              to={dropdownItem.path}
                              className={`block px-6 py-2.5 text-sm ${
                                isActive(dropdownItem.path)
                                  ? 'bg-ivory text-goldDark font-medium'
                                  : 'text-gray-700 hover:bg-ivory hover:text-goldDark'
                              }`}
                              onClick={() => setActiveDropdown(null)}
                            >
                              {dropdownItem.label}
                            </Link>
                          ))}
                        </div>
                      )}
                    </div>
                  ) : (
                    <Link
                      to={item.path}
                      className={`px-4 py-3 font-medium ${
                        isActive(item.path) 
                          ? 'text-goldDark bg-ivory' 
                          : 'text-gray-700 hover:text-goldDark hover:bg-ivory'
                      }`}
                    >
                      {item.label}
                    </Link>
                  )}
                </div>
              ))}
            </div>

          </div>

          {/* Right Side - Search and CTA */}
          <div className="flex items-center space-x-4">
            {/* Search Button */}
            <button className="p-2 text-gray-600 hover:text-goldDark rounded-full hover:bg-ivory transition-colors">
              <Search className="h-5 w-5" />
            </button>
            
            {/* CTA Button */}
            <div className="hidden lg:block">
              <Link
                to="/appointment"
                className="bg-goldDark hover:bg-gold text-white px-6 py-2.5 rounded-md transition-all duration-300 font-medium whitespace-nowrap shadow-md hover:shadow-lg transform hover:-translate-y-0.5 inline-flex items-center"
              >
                Book Appointment
              </Link>
            </div>

            {/* Mobile Menu Button */}
            <button
              className="lg:hidden p-2 text-gray-700 hover:text-goldDark hover:bg-ivory rounded-md transition-colors"
              onClick={toggleMenu}
              aria-label="Toggle menu"
            >
              {isMenuOpen ? (
                <X className="h-6 w-6" />
              ) : (
                <Menu className="h-6 w-6" />
              )}
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="lg:hidden mt-3 py-4 border-t border-goldDark bg-ivory backdrop-blur-md shadow-lg rounded-b-lg">
            <div className="flex flex-col space-y-1">
              {navigationItems.map((item) => (
                <div key={item.path} className="border-b border-goldDark last:border-0">
                  <div className="flex flex-col">
                    {item.dropdown ? (
                      <>
                        <button
                          onClick={() => toggleDropdown(item.path)}
                          className={`px-4 py-3 text-left font-medium flex items-center justify-between ${
                            isActive(item.path) ? 'text-goldDark' : 'text-gray-700'
                          }`}
                        >
                          <span>{item.label}</span>
                          <ChevronDown 
                            className={`h-4 w-4 transition-transform ${
                              activeDropdown === item.path ? 'rotate-180' : ''
                            }`} 
                          />
                        </button>
                        {activeDropdown === item.path && (
                          <div className="pl-6 pb-2 space-y-1 bg-ivory">
                            {item.dropdown.map((dropdownItem) => (
                              <Link
                                key={dropdownItem.path}
                                to={dropdownItem.path}
                                className={`block px-4 py-2.5 text-sm ${
                                  isActive(dropdownItem.path)
                                    ? 'text-goldDark font-medium'
                                    : 'text-gray-600 hover:text-goldDark'
                                }`}
                                onClick={() => {
                                  setIsMenuOpen(false);
                                  setActiveDropdown(null);
                                }}
                              >
                                {dropdownItem.label}
                              </Link>
                            ))}
                          </div>
                        )}
                      </>
                    ) : (
                      <Link
                        to={item.path}
                        className={`px-4 py-3 text-left font-medium ${
                          isActive(item.path) ? 'text-goldDark' : 'text-gray-700 hover:text-goldDark'
                        }`}
                        onClick={() => setIsMenuOpen(false)}
                      >
                        {item.label}
                      </Link>
                    )}
                  </div>
                </div>
              ))}
              <div className="px-4 pt-4">
                <Link
                  to="/appointment"
                  className="block w-full text-center bg-gradient-to-r from-amber-600 via-yellow-600 to-amber-700 hover:from-amber-700 hover:via-yellow-700 hover:to-amber-800 text-white px-6 py-3 rounded-md transition-all duration-300 font-medium shadow-md hover:shadow-lg"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Book Appointment
                </Link>
              </div>
            </div>
          </div>
        )}
      </nav>
    </header>
  );
};

export default Navigation;