import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import 'package:kimiko/kimiko.dart';
import 'package:lottie/lottie.dart';

import '../models/message.dart';

class Bubble extends StatefulWidget {
  const Bubble({super.key, required this.message});

  final Message message;

  @override
  State<Bubble> createState() => _BubbleState();
}

class _BubbleState extends State<Bubble> with ThemeAndSizeMixin {
  @override
  Widget build(BuildContext context) {
    return Material(
      color: widget.message.isBot ? Colors.black12 : Colors.white10,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(8),
        side: BorderSide(
          color: theme.iconTheme.color!,
          width: .75,
        ),
      ),
      child: Padding(
        padding: const EdgeInsets.symmetric(
          horizontal: 50,
          vertical: 35,
        ),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            AnimatedSwitcher(
              duration: const Duration(milliseconds: 300),
              child: widget.message.typing
                  ? Transform.translate(
                      offset: const Offset(-10, -5),
                      child: Transform.scale(
                        scale: 3,
                        child: Lottie.asset(
                          './lotties/responding.json',
                          repeat: true,
                          width: 27.5,
                          height: 27.5,
                        ),
                      ),
                    )
                  : Transform.translate(
                      offset: const Offset(0, -3),
                      child: widget.message.isBot
                          ? const Icon(CupertinoIcons.macwindow)
                          : const Icon(CupertinoIcons.person_alt),
                    ),
            ),
            const SizedBox(width: 20),
            Expanded(
              child: widget.message.typing
                  ? StreamBuilder<String>(
                      stream: widget.message.stream!,
                      builder: (context, snapshot) =>
                          Text('${snapshot.data ?? ''}...'),
                    )
                  : Text(widget.message.text),
            ),
          ],
        ),
      ),
    );
  }
}
