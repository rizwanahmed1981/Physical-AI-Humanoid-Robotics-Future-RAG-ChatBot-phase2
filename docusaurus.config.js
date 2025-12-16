// @ts-check
// `@type` JSDoc annotations allow IDEs and type checkers to infer types
import { themes as prismThemes } from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical-AI-Humanoid-Robotics-Future',
  tagline: 'Bridging Digital AI with Embodied Intelligence',
  favicon: '/img/favicon.ico',

  // Set the production url of your site here
  url: 'https://rizwanahmed1981.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/Physical-AI-Humanoid-Robotics-Future/',

  // GitHub pages deployment config.
  organizationName: 'rizwanahmed1981', // Usually your GitHub org/user name.
  projectName: 'Physical-AI-Humanoid-Robotics-Future', // Usually your repo name.

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          editUrl:
            'https://github.com/rizwanahmed1981/Physical-AI-Humanoid-Robotics-Future/edit/main/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/docusaurus-social-card.jpg',
      navbar: {
        title: 'Physical AI Textbook',
        logo: {
          alt: 'Physical AI Logo',
          src: '/img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Textbook',
          },
          {
            href: 'https://github.com/rizwanahmed1981/Physical-AI-Humanoid-Robotics-Future',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Chapters',
            items: [
              {
                label: 'Chapter 1: Foundations of Physical AI',
                to: '/docs/chapters/chapter1',
              },
              {
                label: 'Chapter 2: The Robotic Nervous System (ROS 2)',
                to: '/docs/chapters/chapter2',
              },
              {
                label: 'Chapter 3: Digital Twins and Simulation',
                to: '/docs/chapters/chapter3',
              },
              {
                label: 'Chapter 4: The AI Brain with NVIDIA Isaac',
                to: '/docs/chapters/chapter4',
              },
              {
                label: 'Chapter 5: Vision–Language–Action Systems',
                to: '/docs/chapters/chapter5',
              },
              {
                label: 'Chapter 6: Capstone Project - Simulated Autonomous Humanoid Robot',
                to: '/docs/chapters/chapter6',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'Stack Overflow',
                href: 'https://stackoverflow.com/questions/tagged/docusaurus',
              },
              {
                label: 'Discord',
                href: 'https://discordapp.com/invite/docusaurus',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/rizwanahmed1981/Physical-AI-Humanoid-Robotics-Future',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Physical AI Textbook. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),
};

export default config;