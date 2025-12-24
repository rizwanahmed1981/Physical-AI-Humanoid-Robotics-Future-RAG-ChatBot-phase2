# ChatWidget Usage Instructions

## Adding ChatWidget to Docusaurus Layout (Global Persistence)

To make the ChatWidget appear on every page of your Docusaurus site, you need to integrate it into the global Layout component. Here's how to do it:

### Method 1: Swizzle the Layout Component

1. **Swizzle the Layout component**:
   ```bash
   cd /home/ecomw/Physical-AI-Humanoid-Robotics-Future-RAG-ChatBot/Physical-AI-Humanoid-Robotics-Future-phase-2
   npm run swizzle @docusaurus/theme-classic Layout
   ```

2. **Modify the Layout component** (`src/theme/Layout/index.js`):
   ```jsx
   import React from 'react';
   import Layout from '@theme-original/Layout';
   import ChatWidget from '../components/ChatWidget';

   export default function LayoutWrapper(props) {
     return (
       <>
         <Layout {...props} />
         <ChatWidget />
       </>
     );
   }
   ```

### Method 2: Direct Page Integration (Current Implementation)

The ChatWidget is already integrated into the main index page (`src/pages/index.jsx`) and will appear on the homepage. For full page coverage, use the swizzling method above.

## Component Features Implemented

### Modern Design
- **Primary Color**: #25c2a0 (consistent with Panaversity brand)
- **Floating Action Button**: Circular, with smooth hover and focus states
- **Card Layout**: Subtle shadows, rounded corners, distinct header
- **Responsive Design**: Adapts to mobile screens (full width on small screens)

### Enhanced UX Features
- **Auto-scroll**: Automatically scrolls to latest messages
- **Focus Management**: Input field automatically focuses when chat opens
- **Loading States**: Visual feedback during "thinking" simulation
- **Keyboard Support**: Send messages with Enter key
- **Accessibility**: Full ARIA labeling and semantic HTML

### Accessibility Compliance
- **WCAG Contrast**: Proper color contrast for text readability
- **Screen Reader Support**: Hidden text for assistive technologies
- **Focus Management**: Clear focus indicators
- **ARIA Attributes**: Proper labeling and state management

## Usage in Individual Pages

For pages where you want the ChatWidget to appear, simply import and render it:

```jsx
import ChatWidget from '../components/ChatWidget';

// In your component JSX
<ChatWidget />
```

## Component Props

The ChatWidget accepts no props and manages its own state internally.

## Styling

All styling is contained within `src/components/ChatWidget/styles.module.css` using CSS Modules for scoped styling.