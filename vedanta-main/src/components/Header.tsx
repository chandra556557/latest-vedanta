import * as React from 'react';
import { useState } from 'react';
import { Menu, X, Phone, Clock, MapPin } from 'lucide-react';

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
    <header className="bg-goldLight shadow-lg sticky top-0 z-50">
      {/* Top Bar */}
      <div className="bg-gold text-goldLight py-2">
        <div className="container mx-auto px-4">
          <div className="flex justify-between items-center text-sm">
            <div className="flex items-center space-x-6">
              <div className="flex items-center space-x-2">
                <Phone className="h-4 w-4" />
                <span>Emergency: +91-XXX-XXX-XXXX</span>
              </div>
              <div className="hidden md:flex items-center space-x-2">
                <Clock className="h-4 w-4" />
                <span>24/7 Emergency Services</span>
              </div>
            </div>
            <div className="hidden md:flex items-center space-x-2">
              <MapPin className="h-4 w-4" />
              <span>Guntur, Andhra Pradesh</span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Navigation */}
      <nav className="container mx-auto px-4 py-3">
        <div className="flex justify-between items-center">
          <div className="flex items-center">
            <a href="/" className="flex items-center">
              <div className="flex items-center p-2">
                <span className="text-2xl font-extrabold text-goldDark">Vedanta</span>
                <span className="text-2xl font-extrabold text-goldDark ml-1">Hospitals</span>
              </div>
            </a>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden lg:flex items-center space-x-8">
            <a href="#home" className="text-gray-700 hover:text-goldDark font-medium transition-colors">Home</a>
            <a href="#about" className="text-gray-700 hover:text-goldDark font-medium transition-colors">About</a>
            <a href="#services" className="text-gray-700 hover:text-goldDark font-medium transition-colors">Services</a>
            <a href="#doctors" className="text-gray-700 hover:text-goldDark font-medium transition-colors">Doctors</a>
            <a href="#testimonials" className="text-gray-700 hover:text-goldDark font-medium transition-colors">Testimonials</a>
            <a href="#news" className="text-gray-700 hover:text-goldDark font-medium transition-colors">News</a>
            <a href="#contact" className="text-gray-700 hover:text-goldDark font-medium transition-colors">Contact</a>
          </div>

          {/* CTA Button */}
          <div className="hidden lg:block">
            <button className="bg-goldDark text-white px-6 py-2 rounded-lg hover:bg-gold transition-colors font-medium">
              Book Appointment
            </button>
          </div>

          {/* Mobile Menu Button */}
          <button
            className="lg:hidden p-2 rounded-md text-gray-700 hover:text-goldDark"
            onClick={toggleMenu}
          >
            {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="lg:hidden mt-4 py-4 border-t">
            <div className="flex flex-col space-y-4">
              <a href="#home" className="text-gray-700 hover:text-goldDark font-medium transition-colors">Home</a>
              <a href="#about" className="text-gray-700 hover:text-goldDark font-medium transition-colors">About</a>
              <a href="#services" className="text-gray-700 hover:text-goldDark font-medium transition-colors">Services</a>
              <a href="#doctors" className="text-gray-700 hover:text-goldDark font-medium transition-colors">Doctors</a>
              <a href="#testimonials" className="text-gray-700 hover:text-goldDark font-medium transition-colors">Testimonials</a>
              <a href="#news" className="text-gray-700 hover:text-goldDark font-medium transition-colors">News</a>
              <a href="#contact" className="text-gray-700 hover:text-goldDark font-medium transition-colors">Contact</a>
              <button className="bg-goldDark text-white px-6 py-2 rounded-lg hover:bg-gold transition-colors font-medium w-full mt-4">
                Book Appointment
              </button>
            </div>
          </div>
        )}
      </nav>
    </header>
  );
};

export default Header;