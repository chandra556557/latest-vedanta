import React, { useState, useRef, ChangeEvent } from 'react';
import { motion } from 'framer-motion';
import { FiX, FiPlus } from 'react-icons/fi';

interface EquipmentItem {
  id: number;
  title: string;
  description: string;
  image: string;
  category: string;
}

const EquipmentGallery: React.FC = () => {
  const [activeCategory, setActiveCategory] = useState<string>('all');

  // Medical equipment data from Vedanta Hospitals
  const equipmentData: EquipmentItem[] = [
    {
      id: 1,
      title: '3T MRI Scanner',
      description: 'High-field MRI system for advanced diagnostic imaging with superior image quality',
      image: 'https://www.vedantahospitals.in/wp-content/uploads/2023/06/mri-scanner-1.jpg',
      category: 'imaging'
    },
    {
      id: 2,
      title: '128-Slice CT Scanner',
      description: 'Advanced CT imaging system for high-resolution diagnostic capabilities',
      image: 'https://www.vedantahospitals.in/wp-content/uploads/2023/06/ct-scanner-1.jpg',
      category: 'imaging'
    },
    {
      id: 3,
      title: '4D Ultrasound System',
      description: 'Advanced ultrasound technology for detailed imaging in obstetrics and gynecology',
      image: 'https://www.vedantahospitals.in/wp-content/uploads/2023/06/ultrasound-1.jpg',
      category: 'imaging'
    },
    {
      id: 4,
      title: 'ICU Ventilator',
      description: 'Advanced critical care ventilator with multiple ventilation modes',
      image: 'https://www.vedantahospitals.in/wp-content/uploads/2023/06/ventilator-1.jpg',
      category: 'critical-care'
    },
    {
      id: 5,
      title: 'Hemodialysis Machine',
      description: 'Advanced dialysis system for renal replacement therapy',
      image: 'https://www.vedantahospitals.in/wp-content/uploads/2023/06/dialysis-1.jpg',
      category: 'nephrology'
    },
    {
      id: 6,
      title: 'Robotic Surgery System',
      description: 'State-of-the-art robotic surgical system for minimally invasive procedures',
      image: 'https://www.vedantahospitals.in/wp-content/uploads/2023/06/robotic-surgery-1.jpg',
      category: 'surgery'
    },
    {
      id: 7,
      title: 'Cath Lab',
      description: 'Advanced cardiac catheterization laboratory for interventional procedures',
      image: 'https://www.vedantahospitals.in/wp-content/uploads/2023/06/cath-lab-1.jpg',
      category: 'cardiology'
    },
    {
      id: 8,
      title: 'Digital X-Ray',
      description: 'High-resolution digital radiography system for accurate diagnosis',
      image: 'https://www.vedantahospitals.in/wp-content/uploads/2023/06/xray-1.jpg',
      category: 'imaging'
    },
    {
      id: 9,
      title: 'Endoscopy Suite',
      description: 'Advanced endoscopic equipment for diagnostic and therapeutic procedures',
      image: 'https://www.vedantahospitals.in/wp-content/uploads/2023/06/endoscopy-1.jpg',
      category: 'gastroenterology'
    }
  ];

  const categories = ['all', 'imaging', 'critical-care', 'nephrology', 'surgery', 'cardiology', 'gastroenterology'];
  const [selectedImage, setSelectedImage] = useState<EquipmentItem | null>(null);
  const [showUploadForm, setShowUploadForm] = useState(false);
  const [newEquipment, setNewEquipment] = useState<Omit<EquipmentItem, 'id'>>({ 
    title: '', 
    description: '', 
    image: '',
    category: 'imaging' 
  });
  const [previewImage, setPreviewImage] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreviewImage(reader.result as string);
        setNewEquipment(prev => ({ ...prev, image: reader.result as string }));
      };
      reader.readAsDataURL(file);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setNewEquipment(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newEquipment.title || !newEquipment.description || !newEquipment.image) return;
    
    // In a real app, you would upload the image to a server here
    // and then add the new item to your database/state
    // const newItem: EquipmentItem = {
    //   ...newEquipment,
    //   id: equipmentData.length + 1
    // };
    alert('In a real application, this would upload the image and save the equipment details.');
    
    // Reset form
    setNewEquipment({ 
      title: '', 
      description: '', 
      image: '',
      category: 'imaging' 
    });
    setPreviewImage(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
    setShowUploadForm(false);
  };

  const filteredEquipment = activeCategory === 'all' 
    ? equipmentData 
    : equipmentData.filter(item => item.category === activeCategory);

  return (
    <section className="py-16 bg-gray-50">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl font-bold text-center mb-12 text-gray-800">Medical Equipment & Resources</h2>
        
        {/* Category Filter */}
        <div className="flex flex-wrap justify-center gap-4 mb-12">
          {categories.map((category) => (
            <button
              key={category}
              onClick={() => setActiveCategory(category)}
              className={`px-6 py-2 rounded-full text-sm font-medium transition-colors ${
                activeCategory === category
                  ? 'bg-blue-600 text-white'
                  : 'bg-white text-gray-700 hover:bg-gray-100'
              }`}
            >
              {category.split('-').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
            </button>
          ))}
        </div>

        {/* Equipment Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
          {filteredEquipment.map((item) => (
            <motion.div
              key={item.id}
              className="bg-white rounded-lg overflow-hidden shadow-md hover:shadow-xl transition-shadow duration-300 flex flex-col h-full"
              whileHover={{ y: -5 }}
            >
              <div className="relative h-48 overflow-hidden group">
                <img
                  src={item.image}
                  alt={item.title}
                  className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent flex items-end p-4">
                  <h3 className="text-xl font-bold text-white">{item.title}</h3>
                </div>
                <button 
                  onClick={() => setSelectedImage(item)}
                  className="absolute inset-0 w-full h-full flex items-center justify-center opacity-0 hover:opacity-100 bg-black/30 transition-opacity duration-300"
                >
                  <span className="bg-white text-blue-600 font-medium px-4 py-2 rounded-full">View Details</span>
                </button>
              </div>
              <div className="p-6 flex-1 flex flex-col">
                <p className="text-gray-600 flex-1">{item.description}</p>
                <div className="mt-4 pt-4 border-t border-gray-100">
                  <span className="inline-block px-3 py-1 text-xs font-semibold text-blue-600 bg-blue-50 rounded-full">
                    {item.category.split('-').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
                  </span>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Image Modal */}
        {selectedImage && (
          <div 
            className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center p-4 z-50"
            onClick={() => setSelectedImage(null)}
          >
            <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-hidden">
              <div className="relative h-[70vh]">
                <img
                  src={selectedImage.image}
                  alt={selectedImage.title}
                  className="w-full h-full object-contain"
                />
                <button
                  className="absolute top-4 right-4 bg-white rounded-full p-2 shadow-lg"
                  onClick={(e) => {
                    e.stopPropagation();
                    setSelectedImage(null);
                  }}
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-6 w-6 text-gray-700"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M6 18L18 6M6 6l12 12"
                    />
                  </svg>
                </button>
              </div>
              <div className="p-6">
                <h3 className="text-2xl font-bold text-gray-800 mb-2">{selectedImage.title}</h3>
                <p className="text-gray-600">{selectedImage.description}</p>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Upload Section */}
      <div className="mt-16 text-center">
        {!showUploadForm ? (
          <button
            onClick={() => setShowUploadForm(true)}
            className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-6 rounded-full inline-flex items-center gap-2 transition-colors"
          >
            <FiPlus /> Add New Equipment
          </button>
        ) : (
          <div className="max-w-2xl mx-auto bg-white rounded-lg shadow-lg p-6">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-xl font-semibold text-gray-800">Upload New Equipment</h3>
              <button 
                onClick={() => setShowUploadForm(false)}
                className="text-gray-500 hover:text-gray-700"
              >
                <FiX size={24} />
              </button>
            </div>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Title</label>
                  <input
                    type="text"
                    name="title"
                    value={newEquipment.title}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    required
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Category</label>
                  <select
                    name="category"
                    value={newEquipment.category}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    required
                  >
                    <option value="imaging">Imaging</option>
                    <option value="critical-care">Critical Care</option>
                    <option value="nephrology">Nephrology</option>
                    <option value="surgery">Surgery</option>
                  </select>
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                <textarea
                  name="description"
                  value={newEquipment.description}
                  onChange={handleInputChange}
                  rows={3}
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Upload Image</label>
                <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md">
                  <div className="space-y-1 text-center">
                    {previewImage ? (
                      <div className="relative">
                        <img 
                          src={previewImage} 
                          alt="Preview" 
                          className="mx-auto h-32 w-auto object-cover rounded-md"
                        />
                        <button
                          type="button"
                          onClick={() => {
                            setPreviewImage(null);
                            setNewEquipment(prev => ({ ...prev, image: '' }));
                            if (fileInputRef.current) {
                              fileInputRef.current.value = '';
                            }
                          }}
                          className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1"
                        >
                          <FiX size={16} />
                        </button>
                      </div>
                    ) : (
                      <>
                        <div className="flex text-sm text-gray-600 justify-center">
                          <label className="relative cursor-pointer bg-white rounded-md font-medium text-blue-600 hover:text-blue-500 focus-within:outline-none">
                            <span>Upload a file</span>
                            <input
                              ref={fileInputRef}
                              name="image"
                              type="file"
                              className="sr-only"
                              accept="image/*"
                              onChange={handleFileChange}
                              required
                            />
                          </label>
                          <p className="pl-1">or drag and drop</p>
                        </div>
                        <p className="text-xs text-gray-500">PNG, JPG, GIF up to 5MB</p>
                      </>
                    )}
                  </div>
                </div>
              </div>
              
              <div className="flex justify-end space-x-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowUploadForm(false)}
                  className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                  disabled={!newEquipment.title || !newEquipment.description || !newEquipment.image}
                >
                  Upload Equipment
                </button>
              </div>
            </form>
          </div>
        )}
      </div>
    </section>
  );
};

export default EquipmentGallery;
