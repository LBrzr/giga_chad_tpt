import 'package:flutter/material.dart';

import 'app.dart';

class Wrapper extends StatefulWidget {
  const Wrapper({super.key});

  @override
  State<Wrapper> createState() => _WrapperState();
}

class _WrapperState extends State<Wrapper> {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'IA Chatbot',
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark().copyWith(
        canvasColor: const Color(0xFF55576D),
        backgroundColor: const Color(0xFF202123),
        dividerColor: Colors.white,
        colorScheme: ColorScheme.light(
          primary: Colors.pinkAccent,
          secondary: Colors.pinkAccent.shade200,
        ),
      ),
      routes: {
        '/': (context) => const App(),
      },
    );
  }
}
