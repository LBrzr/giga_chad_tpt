import 'dart:ui';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:ia_front/bloc/message.dart';

import 'package:kimiko/kimiko.dart';
import 'package:lottie/lottie.dart';

import 'models/message.dart';
import 'widgets/bubble.dart';

class App extends StatefulWidget {
  const App({super.key});

  @override
  State<App> createState() => _AppState();
}

class _AppState extends State<App>
    with ThemeAndSizeMixin, SingleTickerProviderStateMixin {
  static const messages = MessageBloc.instance;
  late final controller = AnimationController(
    vsync: this,
    duration: const Duration(milliseconds: 500),
  );
  late final animation = CurvedAnimation(
    parent: controller,
    curve: Curves.easeInOutCubic,
  );
  final TextEditingController textController = TextEditingController();
  bool responding = false;

  @override
  void initState() {
    super.initState();
    messages.respondingStream.listen((status) {
      setState(() => responding = status);
    });
  }

  void onSend() {
    messages.send(textController.text);
    textController.clear();
  }

  CurvedAnimation lateAnimation(int index) => CurvedAnimation(
        curve: Interval(index / 15, 1, curve: Curves.easeOutSine),
        parent: controller,
      );

  border({required Widget child}) => Material(
        elevation: 8,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(5),
          side: BorderSide(
            color: theme.iconTheme.color!,
            width: .75,
          ),
        ),
        child: child,
      );

  action({
    void Function()? onTap,
    required IconData icon,
    padding = const EdgeInsets.symmetric(vertical: 12.5),
  }) =>
      MouseRegion(
        cursor: SystemMouseCursors.click,
        child: Padding(
          padding: padding,
          child: GestureDetector(
            onTap: onTap,
            child: Icon(icon),
          ),
        ),
      );

  lateAnimate(
          {required int index,
          required double height,
          required Widget child}) =>
      AnimatedBuilder(
        animation: animation,
        builder: (context, child) => Transform.translate(
          offset: Offset(0, height * (1 - lateAnimation(index).value)),
          child: Opacity(
            opacity: animation.value,
            child: child,
          ),
        ),
        child: child,
      );

  get divider => const VerticalDivider(
        thickness: .5,
        width: 30,
        endIndent: 7.5,
        indent: 7.5,
      );

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        alignment: Alignment.center,
        children: [
          KimikoScrollingIconBackground(
            randomRate: 0.75,
            icons: KimikoScrollingIconBackground.musik(null).icons,
          ),
          BackdropFilter(
            filter: ImageFilter.blur(sigmaX: 12.5, sigmaY: 12.5),
            child: Material(
              color: Colors.black38,
              child: StreamBuilder<List<Message>>(
                  stream: messages.stream,
                  builder: (context, snapshot) {
                    final messages = snapshot.data ?? [];
                    return ListView.separated(
                      padding: EdgeInsets.only(
                        top: 90,
                        bottom: 150,
                        left: size.width * .15,
                        right: size.width * .15,
                      ),
                      reverse: true,
                      itemCount: messages.length,
                      itemBuilder: (context, index) => lateAnimate(
                        index: index * 2 + 1,
                        height: 40,
                        child: Bubble(
                            message: messages[messages.length - 1 - index]),
                      ),
                      separatorBuilder: (context, index) =>
                          const SizedBox(height: 15),
                    );
                  }),
            ),
          ),
          Positioned(
            bottom: 0,
            width: size.width,
            height: 100,
            child: DecoratedBox(
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  colors: [
                    theme.backgroundColor,
                    theme.backgroundColor.withOpacity(0),
                  ],
                  begin: Alignment.bottomCenter,
                  end: Alignment.topCenter,
                ),
              ),
            ),
          ),
          Positioned(
            bottom: 40,
            width: size.width,
            child: Padding(
              padding: const EdgeInsets.symmetric(
                vertical: 40,
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.end,
                children: [
                  lateAnimate(
                    index: 3,
                    height: 40,
                    child: border(
                      child: IntrinsicHeight(
                        child: Padding(
                          padding: const EdgeInsets.symmetric(
                            horizontal: 15,
                          ),
                          child: Row(
                            children: [
                              action(
                                onTap: () {},
                                icon: CupertinoIcons.music_note,
                              ),
                              divider,
                              action(
                                onTap: () {},
                                icon: CupertinoIcons.double_music_note,
                              ),
                              divider,
                              action(
                                onTap: () {},
                                icon: CupertinoIcons.music_note_list,
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(width: 15),
                  lateAnimate(
                    index: 5,
                    height: 40,
                    child: border(
                      child: SizedBox(
                        width: size.width * 0.65,
                        child: Padding(
                          padding: const EdgeInsets.symmetric(horizontal: 20),
                          child: IntrinsicHeight(
                            child: Row(
                              children: [
                                Expanded(
                                  child: TextField(
                                    enabled: !responding,
                                    controller: textController,
                                    onSubmitted: (value) => onSend(),
                                    decoration: InputDecoration(
                                      border: InputBorder.none,
                                      contentPadding:
                                          const EdgeInsets.symmetric(
                                        vertical: 15,
                                        horizontal: 10,
                                      ),
                                      hintText: "Type your message",
                                      suffixIcon: responding
                                          ? Transform.scale(
                                              scale: 3,
                                              child: Lottie.asset(
                                                "./lotties/loading.json",
                                                repeat: true,
                                                height: 10,
                                              ),
                                            )
                                          : null,
                                    ),
                                  ),
                                ),
                                divider,
                                action(
                                  onTap: onSend,
                                  icon: CupertinoIcons.paperplane_fill,
                                ),
                              ],
                            ),
                          ),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
          Positioned(
            top: 0,
            width: size.width,
            child: lateAnimate(
              index: 10,
              height: 35,
              child: GestureDetector(
                onTap: controller.forward,
                child: Material(
                  color: theme.backgroundColor.withOpacity(.25),
                  child: Stack(
                    alignment: Alignment.center,
                    children: [
                      Row(
                        mainAxisSize: MainAxisSize.max,
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Lottie.asset('./lotties/robot.json', height: 75),
                          Text(
                            "GigaChad Tout - PT",
                            style: theme.textTheme.headline6,
                          ),
                        ],
                      ),
                      Positioned(
                        right: 35,
                        child: GestureDetector(
                          onTap: controller.reverse,
                          child: Material(
                            type: MaterialType.transparency,
                            child: Padding(
                              padding: const EdgeInsets.all(8.0),
                              child: Icon(
                                CupertinoIcons.xmark,
                                color: theme.iconTheme.color,
                              ),
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
          AnimatedBuilder(
            animation: animation,
            builder: (context, child) => Transform.translate(
              offset: Offset(0, -size.height * animation.value),
              child: GestureDetector(
                onTap: controller.forward,
                child: Material(
                  color: theme.backgroundColor,
                  child: Padding(
                    padding: const EdgeInsets.only(bottom: 50),
                    child: Center(
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Text(
                            "GigaChad Tout - PT",
                            style: theme.textTheme.headline4!
                                .copyWith(fontFamily: 'HP'),
                          ),
                          Lottie.asset('./lotties/robot.json', height: 200),
                        ],
                      ),
                    ),
                  ),
                ),
              ),
            ),
          ),
          Positioned(
            bottom: 0,
            child: Center(
              child: Padding(
                padding: const EdgeInsets.symmetric(vertical: 12.5),
                child: RichText(
                  text: TextSpan(
                    text: "Powered by ",
                    style: theme.textTheme.caption,
                    children: [
                      TextSpan(
                        text: "AKA",
                        style: theme.textTheme.caption!.copyWith(
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
