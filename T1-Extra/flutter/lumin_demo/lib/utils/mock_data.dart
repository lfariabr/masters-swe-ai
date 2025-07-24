import '../models/post.dart';

class MockData {
  static List<Post> getPosts() {
    return [
      Post(
        id: '1',
        username: 'john_doe',
        userAvatar: 'https://i.pravatar.cc/150?img=1',
        imageUrl: 'https://picsum.photos/400/400?random=1',
        caption: 'Beautiful sunset at the beach! 🌅 #sunset #beach #nature',
        likes: 142,
        comments: ['Amazing shot!', 'Love this view!', 'Where is this?'],
        createdAt: DateTime.now().subtract(const Duration(hours: 2)),
      ),
      Post(
        id: '2',
        username: 'sarah_wilson',
        userAvatar: 'https://i.pravatar.cc/150?img=2',
        imageUrl: 'https://picsum.photos/400/400?random=2',
        caption: 'Coffee time ☕ Starting the day right!',
        likes: 89,
        comments: ['Need coffee too!', 'Perfect morning'],
        createdAt: DateTime.now().subtract(const Duration(hours: 5)),
      ),
      Post(
        id: '3',
        username: 'mike_adventures',
        userAvatar: 'https://i.pravatar.cc/150?img=3',
        imageUrl: 'https://picsum.photos/400/400?random=3',
        caption: 'Hiking in the mountains 🏔️ The view from the top is incredible!',
        likes: 256,
        comments: ['Epic adventure!', 'Wish I was there', 'Great photo!', 'How long was the hike?'],
        createdAt: DateTime.now().subtract(const Duration(hours: 8)),
      ),
      Post(
        id: '4',
        username: 'foodie_emma',
        userAvatar: 'https://i.pravatar.cc/150?img=4',
        imageUrl: 'https://picsum.photos/400/400?random=4',
        caption: 'Homemade pasta night! 🍝 Recipe in my bio',
        likes: 78,
        comments: ['Looks delicious!', 'Recipe please!'],
        createdAt: DateTime.now().subtract(const Duration(hours: 12)),
      ),
      Post(
        id: '5',
        username: 'travel_alex',
        userAvatar: 'https://i.pravatar.cc/150?img=5',
        imageUrl: 'https://picsum.photos/400/400?random=5',
        caption: 'Exploring ancient architecture 🏛️ History comes alive here!',
        likes: 195,
        comments: ['Beautiful architecture!', 'Where is this located?', 'Love historical places'],
        createdAt: DateTime.now().subtract(const Duration(days: 1)),
      ),
      Post(
        id: '6',
        username: 'pet_lover_lisa',
        userAvatar: 'https://i.pravatar.cc/150?img=6',
        imageUrl: 'https://picsum.photos/400/400?random=6',
        caption: 'My furry friend enjoying the sunshine 🐕☀️',
        likes: 312,
        comments: ['So cute!', 'What breed?', 'Adorable pup!', 'Give pets from me!'],
        createdAt: DateTime.now().subtract(const Duration(days: 1, hours: 3)),
      ),
    ];
  }
}
