import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/__docusaurus/debug',
    component: ComponentCreator('/__docusaurus/debug', '65e'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/config',
    component: ComponentCreator('/__docusaurus/debug/config', 'bea'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/content',
    component: ComponentCreator('/__docusaurus/debug/content', '915'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/globalData',
    component: ComponentCreator('/__docusaurus/debug/globalData', 'c05'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/metadata',
    component: ComponentCreator('/__docusaurus/debug/metadata', '846'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/registry',
    component: ComponentCreator('/__docusaurus/debug/registry', '3a4'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/routes',
    component: ComponentCreator('/__docusaurus/debug/routes', 'c6f'),
    exact: true
  },
  {
    path: '/docs',
    component: ComponentCreator('/docs', '959'),
    routes: [
      {
        path: '/docs',
        component: ComponentCreator('/docs', 'f3f'),
        routes: [
          {
            path: '/docs',
            component: ComponentCreator('/docs', '6cd'),
            routes: [
              {
                path: '/docs/chapters/chapter1',
                component: ComponentCreator('/docs/chapters/chapter1', '274'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/chapters/template',
                component: ComponentCreator('/docs/chapters/template', '673'),
                exact: true
              },
              {
                path: '/docs/intro',
                component: ComponentCreator('/docs/intro', 'aed'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/quizzes/chapter1-section1',
                component: ComponentCreator('/docs/quizzes/chapter1-section1', 'd26'),
                exact: true
              },
              {
                path: '/docs/quizzes/chapter1-section2',
                component: ComponentCreator('/docs/quizzes/chapter1-section2', '4d9'),
                exact: true
              },
              {
                path: '/docs/quizzes/chapter1-section3',
                component: ComponentCreator('/docs/quizzes/chapter1-section3', '98b'),
                exact: true
              },
              {
                path: '/docs/quizzes/chapter1-section4',
                component: ComponentCreator('/docs/quizzes/chapter1-section4', '4f9'),
                exact: true
              },
              {
                path: '/docs/quizzes/chapter1-section5',
                component: ComponentCreator('/docs/quizzes/chapter1-section5', '04c'),
                exact: true
              },
              {
                path: '/docs/quizzes/chapter1-sections',
                component: ComponentCreator('/docs/quizzes/chapter1-sections', '968'),
                exact: true
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
