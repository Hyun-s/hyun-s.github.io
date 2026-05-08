import React from 'react';
import './Home.css';

const Home = () => {
  return (
    <div className="home">
      <div className="hero">
        <h1>Welcome to Hyunsoo Han's Personal Site</h1>
        <p>Researcher specializing in AI Diffusion Model Compression</p>
      </div>
      <div className="content">
        <section className="intro">
          <h2>About Me</h2>
          <p>
            Hi, I'm Hyunsoo Han, a researcher focused on AI Diffusion Model Compression.
            My work aims to make diffusion models more efficient and accessible.
          </p>
        </section>

        <section className="features">
          <h2>My Research Areas</h2>
          <div className="features-grid">
            <div className="feature-card">
              <h3>Diffusion Model Compression</h3>
              <p>Techniques for reducing the computational cost of diffusion models.</p>
            </div>
            <div className="feature-card">
              <h3>Efficient Inference</h3>
              <p>Methods to speed up inference while maintaining quality.</p>
            </div>
            <div className="feature-card">
              <h3>Model Optimization</h3>
              <p>Advanced optimization techniques for generative models.</p>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};

export default Home;