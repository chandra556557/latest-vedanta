import BlogGallery from '../components/BlogGallery';

const BlogPage = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-blue-700 to-blue-900 text-white py-20">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">Our Blog</h1>
          <p className="text-xl text-blue-100 max-w-3xl mx-auto">
            Stay updated with the latest health news, medical breakthroughs, and wellness tips from our expert doctors.
          </p>
        </div>
      </section>

      {/* Blog Gallery */}
      <div className="py-16">
        <div className="container mx-auto px-4">
          <BlogGallery />
        </div>
      </div>
    </div>
  );
};

export default BlogPage;
