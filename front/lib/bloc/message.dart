import 'package:flutter/cupertino.dart' show debugPrint;

import 'package:rxdart/subjects.dart';

import '../bloc/socket.dart';
import '../models/message.dart';

class MessageBloc {
  static const instance = MessageBloc._();
  const MessageBloc._();

  static const _socket = SocketBloc.instance;

  static void init() {
    _socket.on('responding', _respondingCallback);
    _socket.on('next_char', _nextCharCallback);
  }

  static Message? respondingMsg;

  static final _messageSubject = BehaviorSubject<List<Message>>.seeded([]);
  static final _nextCharSubject = BehaviorSubject<String>.seeded('');
  static final _respondingSubject = BehaviorSubject<bool>.seeded(false)
    ..listen((status) {
      if (status) {
        _messageSubject.add(_messageSubject.value
          ..add(respondingMsg = Message(
            text: '',
            isBot: true,
            stream: _nextCharSubject,
          )));
      } else {
        respondingMsg!.text = _nextCharSubject.value;
        respondingMsg!.stream = null;
        _messageSubject.add(_messageSubject.value);
        _nextCharSubject.add('');
      }
    });

  Stream<List<Message>> get stream => _messageSubject.stream;
  Stream<String> get nextCharStream => _nextCharSubject.stream;
  Stream<bool> get respondingStream => _respondingSubject.stream;

  static void _nextCharCallback(data) {
    debugPrint('next_char: ${data['next_char']}');
    _nextCharSubject.add(_nextCharSubject.value + data['next_char']);
  }

  static void _respondingCallback(data) {
    debugPrint('responding: ${data['status']}');
    _respondingSubject.add(data['status']);
  }

  void send(String message) {
    _messageSubject.add(_messageSubject.value..add(Message(text: message)));
    _socket.emit('message', {'message': message});
  }

  static void dispose() {
    _socket.dispose();
  }
}
