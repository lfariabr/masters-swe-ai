import 'package:flutter/material.dart';
// import 'package:provider/provider.dart'; // We'll uncomment this when we add providers
import 'screens/main_screen.dart';

void main() {
  runApp(const SocialNetworkApp());
}

class SocialNetworkApp extends StatelessWidget {
  const SocialNetworkApp({super.key});

  @override
  Widget build(BuildContext context) {
    // We'll wrap this with MultiProvider later when we have actual providers
    return MaterialApp(
      title: 'Social Network',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: const MainScreen(),
    );
  }
}
