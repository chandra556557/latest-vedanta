import { useState } from 'react';
import { Search, Filter, ChevronRight, User, Calendar, Clock, BookOpen, ArrowRight } from 'lucide-react';
import { motion } from 'framer-motion';

// Animation variants
const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { duration: 0.5 } }
};

const articles = [
    {
      title: 'Introducing HelloKidney.ai: Revolutionizing Kidney Care',
      excerpt: 'We are excited to announce our partnership with HelloKidney.ai, an innovative platform that uses AI to transform kidney disease management and improve patient outcomes worldwide.',
      author: 'HelloKidney Team',
      date: '2024-03-15',
      readTime: '4 min read',
      image: 'https://images.unsplash.com/photo-1576091160550-2173dba999ef?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80',
      category: 'Innovation',
      link: 'https://hellokidney.ai'
    },
    {
      title: 'How AI is Changing Kidney Disease Management',
      excerpt: 'Discover how HelloKidney.ai leverages artificial intelligence to provide personalized treatment plans and early detection of kidney disease, improving patient outcomes.',
      author: 'Dr. Michael Chen',
      date: '2024-03-10',
      readTime: '5 min read',
      image: 'https://images.unsplash.com/photo-1579154204601-01588f351e67?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80',
      category: 'Technology',
      link: 'https://hellokidney.ai/technology'
    },
    {
      title: 'HelloKidney.ai: A Patient\'s Guide to the Platform',
      excerpt: 'Learn how patients can utilize HelloKidney.ai to monitor their kidney health, track lab results, and connect with nephrology specialists from the comfort of their homes.',
      author: 'Health & Wellness',
      date: '2024-03-05',
      readTime: '6 min read',
      image: 'https://images.unsplash.com/photo-1505751172876-fa186e9d30a8?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80',
      category: 'Patient Care',
      link: 'https://hellokidney.ai/patients'
    },
    {
      title: 'The Science Behind HelloKidney.ai',
      excerpt: 'An in-depth look at the cutting-edge AI algorithms and machine learning models that power HelloKidney.ai\'s predictive analytics for kidney disease progression.',
      author: 'Medical Research',
      date: '2024-02-28',
      readTime: '7 min read',
      image: 'https://images.unsplash.com/photo-1578496480159-205e85f51e37?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80',
      category: 'AI Technology',
      link: 'https://hellokidney.ai/technology'
    },
    {
      title: 'HelloKidney.ai: Patient Success Stories',
      excerpt: 'Read inspiring stories from patients whose lives have been transformed by HelloKidney.ai\'s innovative approach to kidney disease management and treatment.',
      author: 'Patient Stories',
      date: '2024-02-20',
      readTime: '5 min read',
      image: 'https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80',
      category: 'Success Stories',
      link: 'https://hellokidney.ai/patient-stories'
    },
    {
      title: 'Join the HelloKidney.ai Early Access Program',
      excerpt: 'Be among the first to experience our AI-powered kidney care platform. Sign up for early access and help shape the future of kidney disease management.',
      author: 'HelloKidney Team',
      date: '2024-03-01',
      readTime: '3 min read',
      image: 'https://images.unsplash.com/photo-1582719471384-894e8d719586?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80',
      category: 'Announcement',
      link: 'https://hellokidney.ai/early-access'
    }
  ];

const News = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [activeCategory, setActiveCategory] = useState('All');

  // Get unique categories
  const categories = ['All', ...new Set(articles.map(article => article.category))];

  // Filter articles based on search and active category
  const filteredArticles = articles.filter(article => {
    const matchesSearch = article.title.toLowerCase().includes(searchQuery.toLowerCase()) || 
                         article.excerpt.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = activeCategory === 'All' || article.category === activeCategory;
    return matchesSearch && matchesCategory;
  });

  // Get featured article (first in the array)
  const featuredArticle = articles[0];
  // Get remaining articles
  const otherArticles = filteredArticles.filter((_, index) => index !== 0);

  return (
    <section id="news" className="bg-gradient-to-b from-blue-50 to-white py-16">
      {/* Hero Section */}
      <div className="relative overflow-hidden bg-gradient-to-r from-blue-600 to-purple-700 text-white py-20 mb-16">
        <div className="absolute inset-0 bg-grid-white/10 [mask-image:linear-gradient(to_bottom,transparent,white,transparent)]"></div>
        <div className="container mx-auto px-4 relative z-10">
          <div className="max-w-4xl mx-auto text-center">
            <motion.h2 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="text-4xl md:text-5xl font-bold mb-6 leading-tight"
            >
              HelloKidney.ai <span className="text-blue-200">Updates</span>
            </motion.h2>
            <motion.p 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.1 }}
              className="text-lg md:text-xl text-blue-100 mb-8 max-w-3xl mx-auto"
            >
              Stay informed about the latest in AI-powered kidney care, treatment innovations, and patient success stories.
            </motion.p>
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="flex flex-col sm:flex-row gap-4 justify-center items-center"
            >
              <motion.div 
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.2 }}
                className="mt-8"
              >
                <a
                  href="#latest-updates"
                  className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 transition-colors duration-200"
                >
                  Explore Latest Updates
                  <ChevronRight className="ml-2 h-5 w-5" />
                </a>
              </motion.div>
            </motion.div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-12">
        {/* Search and Filter */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="bg-white rounded-2xl shadow-lg p-6 mb-12"
        >
          <div className="flex flex-col md:flex-row gap-4">
            <div className="relative flex-1">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Search className="h-5 w-5 text-gray-400" />
              </div>
              <input
                type="text"
                placeholder="Search articles..."
                className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Filter className="h-5 w-5 text-gray-400" />
              </div>
              <select
                className="appearance-none block w-full pl-10 pr-10 py-2 border border-gray-300 rounded-lg bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                value={activeCategory}
                onChange={(e) => setActiveCategory(e.target.value)}
              >
                {categories.map((category) => (
                  <option key={category} value={category}>
                    {category}
                  </option>
                ))}
              </select>
              <div className="absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none">
                <ChevronRight className="h-5 w-5 text-gray-400 transform rotate-90" />
              </div>
            </div>
          </div>
        </motion.div>

        {/* Featured Article */}
        {featuredArticle && (
          <motion.div 
            className="bg-white rounded-2xl shadow-lg overflow-hidden mb-12"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
          >
            <div className="md:flex">
              <div className="md:flex-shrink-0 md:w-1/2">
                <img 
                  className="w-full h-64 md:h-full object-cover" 
                  src={featuredArticle.image} 
                  alt={featuredArticle.title} 
                />
              </div>
              <div className="p-8">
                <div className="uppercase tracking-wide text-sm text-blue-600 font-semibold mb-1">
                  {featuredArticle.category}
                </div>
                <h2 className="text-2xl font-bold text-gray-900 mb-3">
                  {featuredArticle.title}
                </h2>
                <p className="mt-2 text-gray-600 mb-4">
                  {featuredArticle.excerpt}
                </p>
                <div className="flex items-center text-sm text-gray-500 mb-4">
                  <span className="flex items-center mr-4">
                    <User className="h-4 w-4 mr-1" />
                    {featuredArticle.author}
                  </span>
                  <span className="flex items-center">
                    <Calendar className="h-4 w-4 mr-1" />
                    {new Date(featuredArticle.date).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}
                  </span>
                </div>
                <a 
                  href={featuredArticle.link} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="inline-flex items-center text-blue-600 hover:text-blue-800 font-medium"
                >
                  Read full article
                  <ArrowRight className="h-4 w-4 ml-1" />
                </a>
              </div>
            </div>
          </motion.div>
        )}

        {/* Other Articles */}
        <motion.div 
          id="latest-updates"
          className="mb-12"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.4 }}
        >
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">Latest Updates</h2>
            <motion.div
              variants={container}
              initial="hidden"
              animate="show"
              className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
            >
              {otherArticles.map((article) => (
                <motion.article
                  key={article.title}
                  variants={item}
                  className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300 flex flex-col h-full"
                >
                  <img 
                    className="w-full h-48 object-cover" 
                    src={article.image} 
                    alt={article.title} 
                  />
                  <div className="p-6 flex-1 flex flex-col">
                    <div className="uppercase tracking-wide text-xs text-blue-600 font-semibold mb-1">
                      {article.category}
                    </div>
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">
                      {article.title}
                    </h3>
                    <p className="text-gray-600 text-sm mb-4 line-clamp-2 flex-1">
                      {article.excerpt}
                    </p>
                    <div className="flex items-center text-xs text-gray-500 mb-4">
                      <span className="flex items-center mr-3">
                        <User className="h-3 w-3 mr-1" />
                        {article.author}
                      </span>
                      <span className="flex items-center">
                        <Calendar className="h-3 w-3 mr-1" />
                        {new Date(article.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                      </span>
                      <span className="flex items-center ml-3">
                        <BookOpen className="h-3 w-3 mr-1" />
                        {article.readTime}
                      </span>
                    </div>
                    <a 
                      href={article.link} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:text-blue-800 text-sm font-medium inline-flex items-center mt-auto"
                    >
                      Read more
                      <ArrowRight className="h-4 w-4 ml-1" />
                    </a>
                  </div>
                </motion.article>
              ))}
            </motion.div>
          </div>
        </motion.div>

        {/* Newsletter Subscription */}
        <div className="mt-16 bg-gradient-to-br from-blue-600 to-purple-600 rounded-2xl p-8 text-center text-white">
          <h3 className="text-2xl font-bold mb-4">Join the HelloKidney.ai Community</h3>
          <p className="mb-6 opacity-90 max-w-2xl mx-auto">
            Subscribe to our newsletter for the latest updates on AI-powered kidney care, 
            treatment innovations, and early access to new features.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 max-w-md mx-auto">
            <input
              type="email"
              placeholder="Enter your email"
              className="flex-1 px-4 py-3 rounded-lg text-gray-900 focus:outline-none focus:ring-2 focus:ring-white/50"
            />
            <button className="bg-white text-blue-600 px-6 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors">
              Subscribe
            </button>
          </div>
          <p className="text-sm opacity-80 mt-4">
            By subscribing, you agree to our <a href="https://hellokidnet.ai/privacy" target="_blank" rel="noopener noreferrer" className="underline hover:no-underline">Privacy Policy</a>.
          </p>
        </div>
      </div>
    </section>
  );
};

export default News;