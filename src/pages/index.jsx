import React, { useState, useEffect } from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './cinematic-homepage.module.css';

import useBaseUrl from '@docusaurus/useBaseUrl';


// Simple particle animation component
function ParticleBackground() {
  const [particles, setParticles] = useState([]);

  useEffect(() => {
    // Generate random particles
    const generateParticles = () => {
      const newParticles = [];
      for (let i = 0; i < 50; i++) {
        newParticles.push({
          id: i,
          x: Math.random() * 100,
          y: Math.random() * 100,
          size: Math.random() * 3 + 1,
          speed: Math.random() * 0.5 + 0.1,
        });
      }
      setParticles(newParticles);
    };

    generateParticles();
  }, []);

  return (
    <div className={styles.particlesContainer}>
      {particles.map((particle) => (
        <div
          key={particle.id}
          className={styles.particle}
          style={{
            left: `${particle.x}%`,
            top: `${particle.y}%`,
            width: `${particle.size}px`,
            height: `${particle.size}px`,
            opacity: Math.random() * 0.5 + 0.1,
          }}
        />
      ))}
    </div>
  );
}

// Scroll indicator component
function ScrollIndicator() {
  return (
    <div className={styles.scrollIndicator}>
      <div className={styles.scrollArrow}></div>
    </div>
  );
}

// Chapter module component
function ChapterModule({ number, title, to }) {
  return (
    <Link to={to} className={styles.chapterLink}>
      <div className={styles.chapterModule}>
        <div className={styles.chapterNumber}>{number}</div>
        <div className={styles.chapterTitle}>{title}</div>
      </div>
    </Link>
  );
}

export default function Home() {
  const { siteConfig } = useDocusaurusContext();

  // Define chapters as system modules
  const chapters = [
    { number: '01', title: 'Foundations of Physical AI', to: '/docs/chapters/chapter1' },
    { number: '02', title: 'The Robotic Nervous System (ROS 2)', to: '/docs/chapters/chapter2' },
    { number: '03', title: 'Digital Twins and Simulation', to: '/docs/chapters/chapter3' },
    { number: '04', title: 'The AI Brain with NVIDIA Isaac', to: '/docs/chapters/chapter4' },
    { number: '05', title: 'Vision–Language–Action Systems', to: '/docs/chapters/chapter5' },
    { number: '06', title: 'Capstone Project - Simulated Autonomous Humanoid Robot', to: '/docs/chapters/chapter6' },
  ];

  return (
    <div className={styles.homepage}>
      {/* Particle Background */}
      <ParticleBackground />

      {/* Hero Section */}
      <div className={styles.heroSection}>
        <div className={styles.heroContent}>
          <div className={styles.heroText}>
            <h1 className={styles.heroTitle}>Physical AI & Humanoid Robotics</h1>
            <p className={styles.heroSubtitle}>Bridging Digital AI with Embodied Intelligence</p>
            <Link to="/docs/chapters/chapter1" className={styles.ctaButton}>
              Enter the Physical AI World
            </Link>
          </div>
          <div className={styles.heroImagePlaceholder}>
            <img
              src={useBaseUrl('/img/home-page-image.png')}
              alt="Human transforming into humanoid robot"
              className={styles.heroImage}
            />
          </div>
        </div>
      </div>

      {/* Scroll Indicator */}
      <ScrollIndicator />

      {/* System Modules Section */}
      <div className={styles.modulesSection}>
        <div className={styles.modulesContainer}>
          <h2 className={styles.modulesTitle}>Chapters</h2>
          <div className={styles.modulesGrid}>
            {chapters.map((chapter, index) => (
              <ChapterModule
                key={index}
                number={chapter.number}
                title={chapter.title}
                to={chapter.to}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}