import React from 'react';
import { MapPin, Phone, Mail, Clock, Heart, Facebook, Twitter, Instagram, Linkedin, Youtube } from 'lucide-react';

const Footer = () => {
  const locations = [
    {
      city: 'Guntur',
      address: 'Vedanta Hospital, Brodipet, Near Railway Station, Guntur - 522002, AP',
      phone: '+91-863-234-5678',
      email: 'guntur@vedantahospitals.in'
    }
  ];

  const services = [
    'Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics', 
    'Oncology', 'Ophthalmology', 'Emergency Care', 'Dental Care'
  ];

  const quickLinks = [
    'About Us', 'Our Doctors', 'Medical Services', 'Health Packages',
    'Insurance', 'International Patients'
  ];

  return (
    <footer id="contact" className="bg-gray-900 text-white" itemScope itemType="https://schema.org/Hospital">
      {/* Emergency Banner */}
      <div className="bg-gradient-to-r from-amber-600 to-yellow-600 py-3">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-center space-x-4 text-center">
            <Phone className="h-5 w-5" />
            <span className="font-semibold" itemProp="telephone">24/7 Emergency Helpline: +91-863-234-5678</span>
          </div>
        </div>
      </div>

      {/* Main Footer */}
      <div className="container mx-auto px-4 py-16">
        <div className="grid lg:grid-cols-4 gap-8">
          {/* Hospital Info */}
          <div className="lg:col-span-1">
            <a href="/" className="flex items-center mb-6">
              <img 
                src="/images/vedanta-logo.jpg" 
                alt="Vedanta Hospital Logo" 
                className="h-12 w-12 mr-3 rounded-full object-cover shadow-md"
                itemProp="logo"
              />
              <div className="text-3xl font-bold bg-gradient-to-r from-amber-400 to-yellow-400 bg-clip-text text-transparent" itemProp="name">
                Vedanta<span className="bg-gradient-to-r from-yellow-400 to-amber-400 bg-clip-text text-transparent">Hospitals</span>
              </div>
            </a>
            <p className="text-gray-300 mb-6 leading-relaxed" itemProp="description">
              Leading healthcare provider committed to delivering exceptional medical care 
              with cutting-edge technology and compassionate service across India.
            </p>
            
            {/* Social Media */}
            <div className="flex space-x-4">
              <a href="#" className="bg-gray-800 p-3 rounded-full hover:bg-gradient-to-r hover:from-amber-600 hover:to-yellow-600 transition-all duration-300">
                <Facebook className="h-5 w-5" />
              </a>
              <a href="#" className="bg-gray-800 p-3 rounded-full hover:bg-gradient-to-r hover:from-amber-600 hover:to-yellow-600 transition-all duration-300">
                <Twitter className="h-5 w-5" />
              </a>
              <a href="#" className="bg-gray-800 p-3 rounded-full hover:bg-gradient-to-r hover:from-amber-600 hover:to-yellow-600 transition-all duration-300">
                <Instagram className="h-5 w-5" />
              </a>
              <a href="#" className="bg-gray-800 p-3 rounded-full hover:bg-gradient-to-r hover:from-amber-600 hover:to-yellow-600 transition-all duration-300">
                <Linkedin className="h-5 w-5" />
              </a>
              <a href="#" className="bg-gray-800 p-3 rounded-full hover:bg-gradient-to-r hover:from-amber-600 hover:to-yellow-600 transition-all duration-300">
                <Youtube className="h-5 w-5" />
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-xl font-semibold mb-6">Quick Links</h3>
            <ul className="space-y-3">
              {quickLinks.map((link, index) => (
                <li key={index}>
                  <a href="#" className="text-gray-300 hover:text-amber-400 transition-colors">
                    {link}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Services */}
          <div>
            <h3 className="text-xl font-semibold mb-6">Medical Services</h3>
            <ul className="space-y-3">
              {services.map((service, index) => (
                <li key={index}>
                  <a href="#" className="text-gray-300 hover:text-amber-400 transition-colors">
                    {service}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h3 className="text-xl font-semibold mb-6">Contact Information</h3>
            <div className="space-y-4">
              <div className="flex items-start space-x-3">
                <Clock className="h-5 w-5 text-amber-400 mt-1 flex-shrink-0" />
                <div>
                  <div className="font-medium">Operating Hours</div>
                  <div className="text-gray-300 text-sm">24/7 Emergency Services</div>
                  <div className="text-gray-300 text-sm">OPD: Mon-Sat 8:00 AM - 8:00 PM</div>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <Phone className="h-5 w-5 text-amber-400 mt-1 flex-shrink-0" />
                <div>
                  <div className="font-medium">General Inquiry</div>
                  <div className="text-gray-300 text-sm">+91-XXX-XXX-XXXX</div>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <Mail className="h-5 w-5 text-amber-400 mt-1 flex-shrink-0" />
                <div>
                  <div className="font-medium">Email Us</div>
                  <div className="text-gray-300 text-sm">info@vedantahospital.com</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Locations */}
        <div className="border-t border-gray-800 mt-12 pt-12">
          <h3 className="text-2xl font-semibold mb-8 text-center bg-gradient-to-r from-amber-400 to-yellow-400 bg-clip-text text-transparent">Our Locations</h3>
          <div className="grid md:grid-cols-3 gap-8">
            {locations.map((location, index) => (
              <div key={index} className="bg-gradient-to-br from-gray-800 to-gray-900 rounded-xl p-6 hover:from-gray-700 hover:to-gray-800 transition-all duration-300 shadow-lg">
                <h4 className="text-lg font-semibold mb-4 text-amber-400">{location.city}</h4>
                <div className="space-y-3 text-sm">
                  <div className="flex items-start space-x-2">
                    <MapPin className="h-4 w-4 text-gray-400 mt-1 flex-shrink-0" />
                    <span className="text-gray-300">{location.address}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Phone className="h-4 w-4 text-gray-400" />
                    <span className="text-gray-300">{location.phone}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Mail className="h-4 w-4 text-gray-400" />
                    <div className="text-gray-300 text-sm">info@vedantahospitals.in</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Bottom Footer */}
      <div className="border-t border-gray-800 py-6">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
            <div className="text-gray-400 text-sm">
              © 2024 Vedanta Hospital. All rights reserved. Licensed by Healthcare Regulatory Board.
            </div>
            <div className="flex items-center space-x-6 text-sm">
              <a href="#" className="text-gray-400 hover:text-amber-400 transition-colors">Privacy Policy</a>
              <a href="#" className="text-gray-400 hover:text-amber-400 transition-colors">Terms of Service</a>
              <a href="#" className="text-gray-400 hover:text-amber-400 transition-colors">Sitemap</a>
            </div>
            <div className="flex items-center space-x-2 text-sm text-gray-400">
              <Heart className="h-4 w-4 text-red-400" />
              <span>Made with care for your health</span>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;