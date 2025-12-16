import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './styles.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">Bridging Digital AI with Embodied Intelligence</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/chapters/chapter1">
            Start Learning Chapter 1
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();

  return (
    <div>
      <HomepageHeader />
      <main>
        <div className="container">
          <div className="row">
            <div className="col col--4">
              <div className="card">
                <div className="card__header">
                  <h3>Chapter 1: Foundations of Physical AI</h3>
                </div>
                <div className="card__body">
                  <p>Explore the fundamental concepts of Physical AI and embodied intelligence. Understand how artificial intelligence moves from abstract algorithms to tangible, physical manifestations.</p>
                </div>
                <div className="card__footer">
                  <Link to="/docs/chapters/chapter1" className="button button--secondary">
                    Read Chapter 1
                  </Link>
                </div>
              </div>
            </div>
            <div className="col col--4">
              <div className="card">
                <div className="card__header">
                  <h3>Chapter 2: The Robotic Nervous System (ROS 2)</h3>
                </div>
                <div className="card__body">
                  <p>Dive into the Robot Operating System 2 (ROS 2) - the foundational infrastructure that enables communication between robot components and AI algorithms.</p>
                </div>
                <div className="card__footer">
                  <Link to="/docs/chapters/chapter2" className="button button--secondary">
                    Read Chapter 2
                  </Link>
                </div>
              </div>
            </div>
            <div className="col col--4">
              <div className="card">
                <div className="card__header">
                  <h3>Book Overview</h3>
                </div>
                <div className="card__body">
                  <p>This textbook explores the intersection of artificial intelligence and robotics, focusing on embodied intelligence and the practical implementation of AI in physical systems.</p>
                </div>
                <div className="card__footer">
                  <Link to="/docs/chapters/chapter1" className="button button--secondary">
                    View All Chapters
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}