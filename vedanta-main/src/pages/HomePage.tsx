import Hero from '../components/Hero';
import Services from '../components/Services';
import About from '../components/About';
import Doctors from '../components/Doctors';
import Testimonials from '../components/Testimonials';
import News from '../components/News';

const HomePage = () => {
  return (
    <div>
      <Hero />
      <About />
      <Services />
      <Doctors />
      <Testimonials />
      <News />
    </div>
  );
};

export default HomePage;