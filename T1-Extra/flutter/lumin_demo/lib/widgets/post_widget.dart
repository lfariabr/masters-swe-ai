import 'package:flutter/material.dart';
import 'package:cached_network_image/cached_network_image.dart';
import '../models/post.dart';

class PostWidget extends StatefulWidget {
  final Post post;

  const PostWidget({
    super.key,
    required this.post,
  });

  @override
  State<PostWidget> createState() => _PostWidgetState();
}

class _PostWidgetState extends State<PostWidget> {
  late bool isLiked;
  late int likeCount;

  @override
  void initState() {
    super.initState();
    isLiked = widget.post.isLiked;
    likeCount = widget.post.likes;
  }

  void _toggleLike() {
    setState(() {
      isLiked = !isLiked;
      likeCount = isLiked ? likeCount + 1 : likeCount - 1;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Post Header (User info)
          Padding(
            padding: const EdgeInsets.all(12),
            child: Row(
              children: [
                // User Avatar
                CircleAvatar(
                  radius: 20,
                  backgroundImage: CachedNetworkImageProvider(
                    widget.post.userAvatar,
                  ),
                ),
                const SizedBox(width: 12),
                // Username and time
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        widget.post.username,
                        style: const TextStyle(
                          fontWeight: FontWeight.bold,
                          fontSize: 14,
                        ),
                      ),
                      Text(
                        widget.post.timeAgo,
                        style: const TextStyle(
                          color: Colors.grey,
                          fontSize: 12,
                        ),
                      ),
                    ],
                  ),
                ),
                // More options button
                IconButton(
                  icon: const Icon(Icons.more_vert),
                  onPressed: () {
                    // TODO: Show options menu
                  },
                ),
              ],
            ),
          ),
          
          // Post Image
          CachedNetworkImage(
            imageUrl: widget.post.imageUrl,
            width: double.infinity,
            height: 300,
            fit: BoxFit.cover,
            placeholder: (context, url) => Container(
              height: 300,
              color: Colors.grey[200],
              child: const Center(
                child: CircularProgressIndicator(),
              ),
            ),
            errorWidget: (context, url, error) => Container(
              height: 300,
              color: Colors.grey[200],
              child: const Center(
                child: Icon(Icons.error),
              ),
            ),
          ),
          
          // Action Buttons (Like, Comment, Share)
          Padding(
            padding: const EdgeInsets.all(12),
            child: Row(
              children: [
                // Like button
                GestureDetector(
                  onTap: _toggleLike,
                  child: Icon(
                    isLiked ? Icons.favorite : Icons.favorite_border,
                    color: isLiked ? Colors.red : Colors.black,
                    size: 28,
                  ),
                ),
                const SizedBox(width: 16),
                // Comment button
                GestureDetector(
                  onTap: () {
                    // TODO: Navigate to comments
                  },
                  child: const Icon(
                    Icons.chat_bubble_outline,
                    size: 28,
                  ),
                ),
                const SizedBox(width: 16),
                // Share button
                GestureDetector(
                  onTap: () {
                    // TODO: Share functionality
                  },
                  child: const Icon(
                    Icons.send_outlined,
                    size: 28,
                  ),
                ),
                const Spacer(),
                // Bookmark button
                GestureDetector(
                  onTap: () {
                    // TODO: Bookmark functionality
                  },
                  child: const Icon(
                    Icons.bookmark_border,
                    size: 28,
                  ),
                ),
              ],
            ),
          ),
          
          // Like count
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 12),
            child: Text(
              '$likeCount likes',
              style: const TextStyle(
                fontWeight: FontWeight.bold,
                fontSize: 14,
              ),
            ),
          ),
          
          // Caption
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
            child: RichText(
              text: TextSpan(
                style: const TextStyle(
                  color: Colors.black,
                  fontSize: 14,
                ),
                children: [
                  TextSpan(
                    text: widget.post.username,
                    style: const TextStyle(fontWeight: FontWeight.bold),
                  ),
                  const TextSpan(text: ' '),
                  TextSpan(text: widget.post.caption),
                ],
              ),
            ),
          ),
          
          // Comments preview
          if (widget.post.comments.isNotEmpty)
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 12),
              child: GestureDetector(
                onTap: () {
                  // TODO: Navigate to all comments
                },
                child: Text(
                  'View all ${widget.post.comments.length} comments',
                  style: const TextStyle(
                    color: Colors.grey,
                    fontSize: 14,
                  ),
                ),
              ),
            ),
        ],
      ),
    );
  }
}
