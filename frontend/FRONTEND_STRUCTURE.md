# Frontend Structure - EVENTAURA

This document outlines the frontend project structure for EVENTAURA, following a feature-driven development approach.

## Directory Structure

```
frontend/
├── public/                 # Static assets served directly
├── src/
│   ├── app/               # Main application logic and core files
│   │   ├── App.tsx        # Main application component
│   │   ├── App.css        # Main application styles
│   │   └── services/      # API services and external integrations
│   │       ├── bookingService.ts
│   │       └── chatService.ts
│   ├── features/          # Feature-driven modules
│   │   ├── chat/          # Chat feature
│   │   │   ├── ChatPage.tsx
│   │   │   └── index.ts
│   │   └── chatbot/       # Chatbot feature
│   │       ├── ChatInterface.tsx
│   │       ├── ConversationList.tsx
│   │       ├── MessageBubble.tsx
│   │       └── index.ts
│   ├── shared/            # Shared utilities and components
│   │   ├── hooks/         # Custom React hooks
│   │   │   └── useChat.ts
│   │   ├── types/         # TypeScript type definitions
│   │   │   └── chat.ts
│   │   └── utils/         # Utility functions
│   │       └── constants.ts
│   ├── store/             # State management
│   ├── assets/            # Static assets (images, fonts, etc.)
│   ├── _tests_/           # Test files
│   ├── index.css          # Global styles
│   ├── main.tsx           # Application entry point
│   └── vite-env.d.ts      # Vite type definitions
├── components.json        # UI components configuration
├── eslint.config.js       # ESLint configuration
├── index.html             # HTML entry point
├── package.json           # Dependencies and scripts
├── tailwind.config.js     # Tailwind CSS configuration
├── tsconfig.json          # TypeScript configuration
└── vite.config.ts         # Vite build configuration
```

## Architecture Principles

### 1. Feature-Driven Development
- Each feature is self-contained in its own folder
- Features can be developed independently
- Clear separation of concerns

### 2. Shared Resources
- Common utilities, hooks, and types in `shared/`
- Reusable components and UI elements
- Consistent patterns across features

### 3. State Management
- Centralized state in `store/` folder
- Feature-specific state can be co-located with features

### 4. Asset Organization
- Static assets in `assets/` folder
- Public assets in `public/` folder
- Organized by type and usage

## Development Guidelines

### Adding New Features
1. Create a new folder in `features/`
2. Include all feature-specific components, hooks, and types
3. Export public API through `index.ts`
4. Add feature-specific services to `app/services/` if needed

### Shared Components
- Place reusable components in `shared/components/`
- Create UI component library in `shared/components/ui/`
- Document component usage and props

### State Management
- Use `store/` for global application state
- Consider feature-specific state management
- Keep state logic close to where it's used

### Testing
- Place test files in `_tests_/` folder
- Mirror the source structure in tests
- Use descriptive test file names

## File Naming Conventions

- Components: PascalCase (e.g., `ChatInterface.tsx`)
- Hooks: camelCase starting with 'use' (e.g., `useChat.ts`)
- Utilities: camelCase (e.g., `constants.ts`)
- Types: camelCase (e.g., `chat.ts`)
- Services: camelCase ending with 'Service' (e.g., `chatService.ts`)

## Import Paths

Use absolute imports from `src/` for better maintainability:

```typescript
// Good
import { useChat } from '@/shared/hooks/useChat'
import { ChatInterface } from '@/features/chatbot/ChatInterface'

// Avoid
import { useChat } from '../../../shared/hooks/useChat'
```

