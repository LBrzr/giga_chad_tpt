import 'package:flutter/material.dart';

import 'bloc/message.dart';
import 'bloc/socket.dart';
import 'wrapper.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  SocketBloc.init();
  MessageBloc.init();

  runApp(const Wrapper());
}
