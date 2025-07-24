# Instagram-Style Social Network - Step-by-Step Outline
## Phase 1: Foundation & Setup (Weeks 1-2)
Goal: Get familiar with Flutter basics and project structure

### Step 1: Project Structure & Dependencies
- Clean up the default counter app
- Add essential dependencies to pubspec.yaml:
    - provider (state management)
    - dio (HTTP requests)
    - image_picker (camera/gallery access)
    - cached_network_image (image loading)
    - shared_preferences (local storage)

### Step 2: Basic App Structure
- Create folder structure in lib/:
    - models/ (data models)
    - providers/ (state management)
    - screens/ (UI screens)
    - widgets/ (reusable components)
    - services/ (API calls)
    - utils/ (helper functions)

### Step 3: Learn Flutter Basics
- Understand Widgets (StatelessWidget vs StatefulWidget)
- Learn about the Widget tree
- Practice with basic layouts (Column, Row, Container)

## Phase 2: Authentication & User Management (Weeks 3-4)
Goal: Learn state management and user authentication

### Step 4: User Model & Authentication
- Create User model class
- Build login/signup screens
- Implement Provider for authentication state
- Learn about form validation

### Step 5: User Profiles
- Create profile screen layout
- Learn about navigation between screens
- Implement basic profile editing

## Phase 3: Core Social Features (Weeks 5-8)
Goal: Build the main Instagram-like features

### Step 6: Photo Sharing
- Implement image picker functionality
- Create post creation screen
- Learn about file handling in Flutter
- Build image preview and editing

### Step 7: Feed/Timeline
- Create main feed screen
- Build post widget components
- Learn about ListView and scrolling
- Implement pull-to-refresh

### Step 8: Social Interactions
- Add like/unlike functionality
- Implement comments system
- Learn about nested widgets and state updates

## Phase 4: Advanced Features (Weeks 9-12)
Goal: Add sophisticated social features

### Step 9: User Discovery
- Build search functionality
- Create user following system
- Learn about filtering and searching data

### Step 10: Stories Feature
- Implement story creation and viewing
- Learn about timers and animations
- Build story viewer with gestures

### Step 11: Direct Messaging
- Create chat interface
- Learn about real-time updates
- Implement message threading

## Phase 5: Polish & Deployment (Weeks 13-14)
Goal: Finalize and deploy the app

### Step 12: UI/UX Polish
- Implement dark/light themes
- Add loading states and error handling
- Learn about responsive design

### Step 13: Testing & Deployment
- Write basic tests
- Build for different platforms
- Learn about app deployment

---

## Current progress

### Running the app
```bash
cd T1-Extra/flutter/lumin_demoZ
flutter run -d chrome
```

### 🔹 v1.0.0 - `feature/flutter-setup` - Project Structure & Dependencies

#### Step 1 - COMPLETED ✅
**Project Structure & Dependencies**
1. Updated pubspec.yaml with essential dependencies:
- provider - State management (like Redux for Flutter)
- dio - HTTP requests (like Axios for JavaScript)
- image_picker - Camera/gallery access
- cached_network_image - Efficient image loading
- shared_preferences - Local storage
- flutter_staggered_grid_view - Instagram-style grid layouts

2. Created organized folder structure:
lib/
├── models/      # Data structures (User, Post, etc.)
├── providers/   # State management logic
├── screens/     # Full-screen pages
├── widgets/     # Reusable UI components
├── services/    # API calls and external services
└── utils/       # Helper functions

3. Cleaned up the default counter app and created a foundation with:
- SocialNetworkApp: Main app widget
- HomeScreen: Our first screen
- Provider setup ready for state management

**Key Learnings**
1. Widget Tree Structure
```dart
SocialNetworkApp (MaterialApp)
└── HomeScreen (Scaffold)
    ├── AppBar
    └── Body (Center → Column → [Icon, Text, Text])
```

2. StatelessWidget vs StatefulWidget
- StatelessWidget: UI that doesn't change (like our `HomeScreen`)
- StatefulWidget: UI that can change based on user interaction
- Key concept: `build()` method returns the UI

3. Provider Pattern Setup
```dart
MultiProvider(
  providers: [
    // Future state providers go here
  ],
  child: MaterialApp(...)
)
```

4. Import Organization
- Flutter material design: import `package:flutter/material.dart`;
- Third-party packages: import `package:provider/provider.dart`;
- Local files: import `screens/home_screen.dart`;

### 🔹 v1.1.0 - `feature/flutter-structure` - Basic App Structure

#### Step 2 - COMPLETED ✅
**Basic App Structure**
1. MainScreen - The core navigation controller with:
    - StatefulWidget with navigation state management
    - Bottom navigation bar with 5 Instagram-style tabs
    - Screen switching logic using setState()

2. Navigation Screens:
    - Home 🏠 - Feed/Timeline
    - Search 🔍 - Discover content
    - Add Post ➕ - Create posts
    - Activity ❤️ - Notifications
    - Profile 👤 - User profile

**Key Learnings**
1. StatefulWidget Pattern

2. BottomNavigationBar
- `type: BottomNavigationBarType.fixed` - Shows all tabs
- `currentIndex` - Tracks active tab
- `onTap` - Handles tab switching
- Icon states: `icon` (unselected) vs `activeIcon` (selected)

3. List-Based Screen Management
```dart
final List<Widget> _screens = [
  const HomeScreen(),
  const SearchScreen(),
  // ...
];

body: _screens[_currentIndex], // Dynamic screen switching
```

4. Scaffold Structure
Each screen follows the pattern:
- AppBar - Top navigation
- body - Main content
- Consistent styling across screens

### 🔹 v1.3.0 - `feature/flutter-basics-and-widgets` - Learn Flutter Basics and Widgets

#### Step 3 - COMPLETED ✅
**Learn Flutter Basics and Widgets**

1.Post Model (`models/post.dart`):
- Data structure with all post properties
- `timeAgo` helper method for relative timestamps
- `copyWith` method for immutable updates

2. Mock Data (`utils/mock_data.dart`):
- Sample posts with realistic content
- Different users, images, and timestamps
- Varied engagement (likes, comments)

3. Custom Post Widget (`widgets/post_widget.dart`):
- Complete Instagram-style post layout
- Interactive like button with state management
- Image loading with placeholders and error handling
- User avatars, captions, and comment previews

4. Updated Home Screen:
- `ListView.builder` for efficient scrolling
- App bar with action buttons
- Integration of all components

**Key Learnings**
1. Data Modeling
```dart
class Post {
  final String id;
  final String username;
  // ... other properties
  
  // Helper methods
  String get timeAgo { /* logic */ }
  Post copyWith({...}) { /* immutable updates */ }
}
```

2. ListView.builder Pattern
```dart
ListView.builder(
  itemCount: posts.length,
  itemBuilder: (context, index) {
    return PostWidget(post: posts[index]);
  },
)
```
- Efficient: Only builds visible items
- Scrollable: Handles large lists automatically
- Dynamic: Updates when data changes

3. Custom Widget Creation 
```dart
class PostWidget extends StatefulWidget {
  final Post post; // Data passed from parent
  
  @override
  State<PostWidget> createState() => _PostWidgetState();
}
```

4. State Management in Widgets
```dart
void _toggleLike() {
  setState(() {
    isLiked = !isLiked;
    likeCount = isLiked ? likeCount + 1 : likeCount - 1;
  });
}
```

5. Image Handling
```dart
CachedNetworkImage(
  imageUrl: widget.post.imageUrl,
  placeholder: (context, url) => CircularProgressIndicator(),
  errorWidget: (context, url, error) => Icon(Icons.error),
)
```

6. Widget Composition
- Breaking complex UI into smaller, reusable pieces
- Passing data between parent and child widgets
- Combining multiple widgets to create rich layouts

### 🔹 v1.4.0 - `feature/flutter-tbd` - TBD

#### Step 4 - NOT STARTED 🕐
**TBDs**
