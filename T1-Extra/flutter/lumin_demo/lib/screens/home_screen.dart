import 'package:flutter/material.dart';
import '../models/post.dart';
import '../utils/mock_data.dart';
import '../widgets/post_widget.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final List<Post> posts = MockData.getPosts();

    return Scaffold(
      appBar: AppBar(
        title: const Text('Lumin.gg'),
        backgroundColor: Colors.white,
        foregroundColor: Colors.black,
        elevation: 0,
        centerTitle: false,
        actions: [
          IconButton(
            icon: const Icon(Icons.favorite_border),
            onPressed: () {
              // TODO: Navigate to activity/notifications
            },
          ),
          IconButton(
            icon: const Icon(Icons.send_outlined),
            onPressed: () {
              // TODO: Navigate to direct messages
            },
          ),
        ],
      ),
      body: ListView.builder(
        itemCount: posts.length,
        itemBuilder: (context, index) {
          return PostWidget(post: posts[index]);
        },
      ),
    );
  }
}
