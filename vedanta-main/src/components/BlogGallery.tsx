import { useState } from 'react';
import { ArrowRight, Calendar, Clock, User, Search } from 'lucide-react';

type BlogPost = {
  id: number;
  title: string;
  excerpt: string;
  image: string;
  category: string;
  date: string;
  readTime: string;
  author: string;
};

const BlogGallery = () => {
  // Blog data from Vedanta Hospitals
  const allBlogPosts: BlogPost[] = [
    {
      id: 1,
      title: 'Comprehensive Kidney Care at Vedanta Hospitals',
      excerpt: 'Discover our advanced nephrology department offering complete kidney care services including dialysis, transplants, and preventive care. Our team of experienced nephrologists provides personalized treatment plans for all kidney-related conditions.',
      image: 'https://images.unsplash.com/photo-1576091160550-2173dba999ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
      category: 'Nephrology',
      date: '2023-11-25',
      readTime: '6 min read',
      author: 'Dr. K. Venkata Rao'
    },
    {
      id: 2,
      title: 'Heart Health Awareness Program',
      excerpt: 'Join our heart health initiative focusing on prevention, early detection, and management of cardiovascular diseases. Learn about our state-of-the-art cardiac care facilities and expert cardiology team.',
      image: 'https://images.unsplash.com/photo-1579684453423-f84349ef60b0?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
      category: 'Cardiology',
      date: '2023-11-20',
      readTime: '5 min read',
      author: 'Dr. A. Tirumala Naresh'
    },
    {
      id: 3,
      title: 'Kidney and Heart Health Camp Success',
      excerpt: 'Our recent health camp in Rompicharla Mandal ZP High School successfully provided free checkups and awareness sessions for 200+ patients. The event featured expert consultations and educational programs on kidney and heart health.',
      image: 'https://images.unsplash.com/photo-1505751172876-fa186e5a3c60?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
      category: 'Health Camp',
      date: '2023-11-15',
      readTime: '4 min read',
      author: 'Vedanta Medical Team'
    },
    {
      id: 4,
      title: 'Comprehensive Healthcare Services',
      excerpt: 'Discover our wide range of specialized medical services. Our expert team combines advanced technology with compassionate care to provide comprehensive treatment options for all your healthcare needs.',
      image: 'https://images.unsplash.com/photo-1579154204601-01588f351e67?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
      category: 'Transplant',
      date: '2023-11-10',
      readTime: '7 min read',
      author: 'Dr. K. Venkata Rao'
    },
    {
      id: 5,
      title: 'Diabetes and Kidney Health',
      excerpt: 'Understanding the crucial connection between diabetes and kidney disease. Our specialists share insights on prevention, early detection, and management strategies for diabetic kidney disease.',
      image: 'https://images.unsplash.com/photo-1532938914880-cd1dd9e64ccc?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
      category: 'Nephrology',
      date: '2023-11-05',
      readTime: '5 min read',
      author: 'Dr. Chinta Rama Krishna'
    },
    {
      id: 6,
      title: 'Pediatric Nephrology Care',
      excerpt: 'Specialized kidney care for children at Vedanta Hospitals. Our pediatric nephrology department provides comprehensive diagnosis and treatment for all kidney-related conditions in children.',
      image: 'https://images.unsplash.com/photo-1576091160399-112ba8d25af1?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
      category: 'Pediatrics',
      date: '2023-10-30',
      readTime: '4 min read',
      author: 'Dr. Manjula Sri Ram'
    }
  ];

  // Pagination state
  const [currentPage, setCurrentPage] = useState(1);
  const postsPerPage = 8;
  const totalPages = Math.ceil(allBlogPosts.length / postsPerPage);

  // Get current posts
  const indexOfLastPost = currentPage * postsPerPage;
  const indexOfFirstPost = indexOfLastPost - postsPerPage;

  const [selectedCategory, setSelectedCategory] = useState<string>('All');
  const [searchQuery, setSearchQuery] = useState<string>('');

  // Get unique categories
  const categories = ['All', ...new Set(allBlogPosts.map(post => post.category))];

  // Filter blog posts based on selected category and search query
  const filteredPosts = allBlogPosts.filter(post => {
    const matchesCategory = selectedCategory === 'All' || post.category === selectedCategory;
    const matchesSearch = post.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         post.excerpt.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         post.author.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  // Update current posts when filters change
  const currentFilteredPosts = filteredPosts.slice(indexOfFirstPost, indexOfLastPost);

  // Format date to a more readable format
  const formatDate = (dateString: string) => {
    const options: Intl.DateTimeFormatOptions = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
  };

  return (
    <section id="blog-gallery" className="py-20 bg-gradient-to-b from-white to-gray-50">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 max-w-7xl">
        <div className="text-center mb-16">
          <span className="inline-block bg-sky-100 text-sky-700 text-sm font-semibold px-4 py-1.5 rounded-full mb-4">
            Our Blog
          </span>
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-5 font-heading">
            Health Insights & <span className="text-sky-600">Updates</span>
          </h2>
          <div className="w-20 h-1 bg-gradient-to-r from-sky-400 to-emerald-400 mx-auto mb-6"></div>
          <p className="text-lg md:text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Stay informed with our latest articles, research, and health tips from our expert medical team.
          </p>
        </div>

        {/* Search and Filter */}
        <div className="mb-16 flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="w-full md:w-1/3 relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Search className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="text"
              placeholder="Search articles..."
              className="block w-full pl-10 pr-3 py-3 border border-gray-200 rounded-xl bg-white shadow-sm focus:outline-none focus:ring-2 focus:ring-sky-500 focus:border-transparent transition-all duration-200"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
          <div className="flex flex-wrap justify-center gap-3">
            {categories.map((category) => (
              <button
                key={category}
                onClick={() => setSelectedCategory(category)}
                className={`px-5 py-2.5 rounded-xl text-sm font-medium transition-all duration-300 transform hover:-translate-y-0.5 ${
                  selectedCategory === category
                    ? 'bg-gradient-to-r from-sky-500 to-emerald-500 text-white shadow-lg shadow-sky-100'
                    : 'bg-white text-gray-700 hover:bg-gray-50 shadow-md hover:shadow-lg border border-gray-100'
                }`}
              >
                {category}
              </button>
            ))}
          </div>
        </div>

        {/* Blog Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {currentFilteredPosts.length > 0 ? (
            currentFilteredPosts.map((post) => (
              <article 
                key={post.id} 
                className="group bg-white rounded-2xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-1.5 border border-gray-50"
              >
                <div className="relative h-56 overflow-hidden">
                  <img
                    src={post.image}
                    alt={post.title}
                    className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                  <span className="absolute top-4 right-4 bg-gradient-to-r from-sky-500 to-emerald-500 text-white text-xs font-semibold px-3 py-1.5 rounded-full shadow-md">
                    {post.category}
                  </span>
                </div>
                <div className="p-6">
                  <div className="flex items-center text-sm text-gray-500 mb-4">
                    <div className="flex items-center mr-5">
                      <Calendar className="w-4 h-4 mr-1.5 text-sky-500" />
                      <span className="text-gray-600">{formatDate(post.date)}</span>
                    </div>
                    <div className="flex items-center">
                      <Clock className="w-4 h-4 mr-1.5 text-emerald-500" />
                      <span className="text-gray-600">{post.readTime}</span>
                    </div>
                  </div>
                  <h3 className="text-xl font-bold text-gray-900 mb-3 line-clamp-2 leading-tight group-hover:text-sky-600 transition-colors duration-200">
                    {post.title}
                  </h3>
                  <p className="text-gray-600 mb-5 line-clamp-3 leading-relaxed">
                    {post.excerpt}
                  </p>
                  <div className="flex items-center justify-between pt-4 border-t border-gray-100">
                    <div className="flex items-center">
                      <div className="w-8 h-8 rounded-full bg-gradient-to-r from-sky-100 to-emerald-100 flex items-center justify-center mr-3">
                        <User className="w-4 h-4 text-sky-600" />
                      </div>
                      <span className="text-sm font-medium text-gray-700">{post.author}</span>
                    </div>
                    <a
                      href={`/blog/${post.id}`}
                      className="inline-flex items-center text-sky-600 hover:text-sky-700 font-medium text-sm group-hover:translate-x-1 transition-transform duration-200"
                    >
                      Read More 
                      <ArrowRight className="w-4 h-4 ml-1.5 group-hover:translate-x-1 transition-transform duration-200" />
                    </a>
                  </div>
                </div>
              </article>
            ))
          ) : (
            <div className="col-span-full text-center py-16 px-4 bg-white rounded-2xl shadow-sm border border-gray-100">
              <div className="w-20 h-20 mx-auto mb-4 rounded-full bg-sky-50 flex items-center justify-center">
                <Search className="w-8 h-8 text-sky-500" />
              </div>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">No articles found</h3>
              <p className="text-gray-500 max-w-md mx-auto">
                We couldn't find any articles matching your search. Try adjusting your filters or search terms.
              </p>
            </div>
          )}
        </div>

        {/* Pagination */}
        {filteredPosts.length > postsPerPage && (
          <div className="flex justify-center mt-12 space-x-2">
            <button
              onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
              disabled={currentPage === 1}
              className="px-4 py-2 rounded-lg border border-gray-300 bg-white text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Previous
            </button>
            
            {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
              let pageNum;
              if (totalPages <= 5) {
                pageNum = i + 1;
              } else if (currentPage <= 3) {
                pageNum = i + 1;
              } else if (currentPage >= totalPages - 2) {
                pageNum = totalPages - 4 + i;
              } else {
                pageNum = currentPage - 2 + i;
              }
              
              return (
                <button
                  key={pageNum}
                  onClick={() => setCurrentPage(pageNum)}
                  className={`w-10 h-10 rounded-lg ${currentPage === pageNum 
                    ? 'bg-sky-600 text-white' 
                    : 'bg-white text-gray-700 hover:bg-gray-100'} border border-gray-300`}
                >
                  {pageNum}
                </button>
              );
            })}
            
            <button
              onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
              disabled={currentPage === totalPages}
              className="px-4 py-2 rounded-lg border border-gray-300 bg-white text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next
            </button>
          </div>
        )}
      </div>
    </section>
  );
};

export default BlogGallery;
