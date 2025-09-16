#Chatbot Frontend

A modern React-based frontend for the AI-powered venue booking chatbot system.

## 🚀 Features

- **Real-time Chat Interface**: Interactive chat with AI assistant for venue booking
- **Conversation Management**: Save, load, and manage chat sessions
- **Responsive Design**: Mobile-first design with responsive sidebar
- **Modern UI/UX**: Clean, intuitive interface with smooth animations
- **TypeScript**: Full type safety and better development experience
- **Tailwind CSS**: Utility-first CSS framework for rapid styling

## 🛠️ Tech Stack

- **React 18** - Modern React with hooks and concurrent features
- **TypeScript** - Type-safe JavaScript
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **React Router** - Client-side routing
- **Axios** - HTTP client for API calls
- **Lucide React** - Beautiful icon library

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   └── chatbot/
│   │       ├── ChatInterface.tsx      # Main chat UI
│   │       ├── MessageBubble.tsx      # Individual message display
│   │       ├── ConversationList.tsx   # Chat session sidebar
│   │       └── index.ts               # Component exports
│   ├── hooks/
│   │   └── useChat.ts                 # Custom chat hook
│   ├── pages/
│   │   └── chat/
│   │       ├── ChatPage.tsx           # Main chat page
│   │       └── index.ts               # Page exports
│   ├── routes/
│   │   └── AppRoutes.tsx              # Application routing
│   ├── services/
│   │   ├── chatService.ts             # Chat API service
│   │   └── bookingService.ts          # Booking API service
│   ├── types/
│   │   └── chat.ts                    # TypeScript type definitions
│   ├── utils/
│   │   └── constants.ts               # App constants
│   ├── App.tsx                        # Main app component
│   ├── main.tsx                       # App entry point
│   ├── App.css                        # App-specific styles
│   └── index.css                      # Global styles
├── public/
│   └── favicon.ico                    # App icon
├── package.json                       # Dependencies and scripts
├── vite.config.ts                     # Vite configuration
├── tsconfig.json                      # TypeScript configuration
├── tailwind.config.js                 # Tailwind CSS configuration
├── postcss.config.js                  # PostCSS configuration
└── README.md                          # This file
```

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Backend Django server running on port 8000

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Set up environment variables**
   Create a `.env` file in the frontend directory:
   ```bash
   VITE_API_BASE_URL=http://localhost:8000/api
   VITE_CHATBOT_API_URL=http://localhost:8000/api/chatbot
   VITE_BOOKING_API_URL=http://localhost:8000/api/booking
   VITE_APP_NAME=Venue Booking Chatbot
   VITE_DEBUG=true
   ```

4. **Start the development server**
   ```bash
   npm run dev
   # or
   yarn dev
   ```

5. **Open your browser**
   Navigate to `http://localhost:3000`

## 📱 Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_BASE_URL` | Base API URL | `http://localhost:8000/api` |
| `VITE_CHATBOT_API_URL` | Chatbot API endpoint | `http://localhost:8000/api/chatbot` |
| `VITE_BOOKING_API_URL` | Booking API endpoint | `http://localhost:8000/api/booking` |
| `VITE_APP_NAME` | Application name | `Venue Booking Chatbot` |
| `VITE_DEBUG` | Enable debug mode | `false` |

### API Configuration

The frontend communicates with the Django backend through REST APIs:

- **Chatbot API**: `/api/chatbot/` - Chat functionality
- **Booking API**: `/api/booking/` - Venue and booking management

## 🎨 UI Components

### ChatInterface
Main chat component with message input, send button, and message display.

### MessageBubble
Individual message component with user/assistant styling and timestamps.

### ConversationList
Sidebar component for managing chat sessions and history.

### ChatPage
Main page component that combines sidebar and chat interface.

## 🔌 Custom Hooks

### useChat
Custom hook for managing chat state, messages, and API calls.

**Features:**
- Message sending and receiving
- Session management
- Error handling
- Loading states
- Request cancellation

## 🌐 API Services

### chatService
Handles all chatbot-related API calls:
- Send messages
- Get chat sessions
- Delete sessions
- Get venue recommendations

### bookingService
Manages venue and booking operations:
- CRUD operations for venues
- Booking management
- Availability checking
- User bookings

## 📱 Responsive Design

The application is fully responsive with:
- Mobile-first design approach
- Collapsible sidebar on mobile
- Touch-friendly interface
- Adaptive layouts for different screen sizes

## 🎯 Key Features

1. **Real-time Chat**: Instant messaging with AI assistant
2. **Session Management**: Save and restore conversations
3. **Venue Information**: Get details about available venues
4. **Booking Assistance**: Help with venue reservations
5. **Mobile Optimized**: Great experience on all devices
6. **Accessibility**: Keyboard navigation and screen reader support

## 🚀 Deployment

### Build for Production
```bash
npm run build
```

### Preview Production Build
```bash
npm run preview
```

### Deploy to Static Hosting
The built files in the `dist/` directory can be deployed to any static hosting service like:
- Vercel
- Netlify
- GitHub Pages
- AWS S3
- Firebase Hosting

## 🔍 Development

### Code Style
- Use TypeScript for all new code
- Follow React best practices
- Use functional components with hooks
- Implement proper error boundaries
- Write meaningful component names

### Testing
```bash
# Run tests (when implemented)
npm test

# Run tests in watch mode
npm run test:watch
```

### Linting
```bash
# Run ESLint
npm run lint

# Fix auto-fixable issues
npm run lint:fix
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Check the documentation
- Review existing issues
- Create a new issue with detailed description

## 🔮 Future Enhancements

- [ ] Voice input support
- [ ] File attachment handling
- [ ] Real-time notifications
- [ ] Advanced venue filtering
- [ ] Calendar integration
- [ ] Payment processing
- [ ] Multi-language support
- [ ] Dark mode theme
- [ ] Offline support
- [ ] Progressive Web App (PWA)
