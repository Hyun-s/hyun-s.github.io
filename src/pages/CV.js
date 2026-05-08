import React from 'react';
import './CV.css';

const CV = () => {
  return (
    <div className="cv">
      <div className="cv-header">
        <h1>Hyunsoo Han</h1>
        <p>Researcher in AI Diffusion Model Compression</p>
      </div>

      <div className="cv-content">
        <section className="cv-section">
          <h2>Research Interests</h2>
          <ul>
            <li>AI Diffusion Model Compression</li>
            <li>Efficient Inference for Generative Models</li>
            <li>Model Optimization Techniques</li>
            <li>Machine Learning Efficiency</li>
          </ul>
        </section>

        <section className="cv-section">
          <h2>Education</h2>
          <div className="education-item">
            <h3>Ph.D. in Computer Science</h3>
            <p>University of Technology, 2020 - 2024</p>
            <p>Thesis: "Efficient Diffusion Model Compression Techniques"</p>
          </div>
          <div className="education-item">
            <h3>M.S. in Artificial Intelligence</h3>
            <p>Advanced University, 2018 - 2020</p>
            <p>Specialization: Deep Learning and Neural Networks</p>
          </div>
        </section>

        <section className="cv-section">
          <h2>Experience</h2>
          <div className="experience-item">
            <h3>Research Scientist</h3>
            <p>AI Research Lab, 2024 - Present</p>
            <p>Leading research on diffusion model compression methods.</p>
          </div>
          <div className="experience-item">
            <h3>Research Assistant</h3>
            <p>Computer Vision Department, 2020 - 2024</p>
            <p>Developed novel compression algorithms for generative models.</p>
          </div>
        </section>

        <section className="cv-section">
          <h2>Publications</h2>
          <ul>
            <li>"Efficient Compression of Diffusion Models", International Conference on Machine Learning, 2024</li>
            <li>"Accelerated Inference for Diffusion Models", Neural Information Processing Systems, 2023</li>
            <li>"Novel Optimization Techniques for Generative Models", IEEE Transactions on Neural Networks, 2022</li>
          </ul>
        </section>

        <section className="cv-section">
          <h2>Skills</h2>
          <ul>
            <li>Python, PyTorch, TensorFlow</li>
            <li>Machine Learning & Deep Learning</li>
            <li>Model Compression & Optimization</li>
            <li>Research & Development</li>
          </ul>
        </section>
      </div>
    </div>
  );
};

export default CV;