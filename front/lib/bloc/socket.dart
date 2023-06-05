import 'package:flutter/cupertino.dart' show debugPrint;

import 'package:socket_io_client/socket_io_client.dart' as IO;

import '../resources/strings.dart';

class SocketBloc {
  static const instance = SocketBloc._();

  const SocketBloc._();

  static final IO.Socket _socket = IO.io(Strings.socketUrl);

  static Future<void> init() async {
    debugPrint('Initializing socket');
    _socket.onConnect((data) {
      debugPrint('Connected to socket');
    });
  }

  Future<void> emit(String event, Map data) async {
    _socket.emit(event, data);
  }

  void on(String event, void Function(dynamic) callback) {
    _socket.on(event, callback);
  }

  void dispose() async {
    _socket.disconnect();
    _socket.dispose();
  }
}
