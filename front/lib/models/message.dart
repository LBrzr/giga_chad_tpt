class Message {
  final String id = DateTime.now().millisecondsSinceEpoch.toString();
  final bool isBot;
  Stream<String>? stream;
  String text;

  Message({
    required this.text,
    this.isBot = false,
    this.stream,
  });

  factory Message.fromMap(Map<String, dynamic> map) => Message(
        text: map['text'],
        isBot: map['isBot'] ?? true,
      );

  bool get typing => stream != null;

  Map<String, dynamic> toMap() => {
        'id': id,
        'text': text,
        'isBot': isBot,
      };

  /* static final test = [
    Message(
      id: '1',
      text: 'Hello',
      isBot: true,
    ),
    Message(
      id: '2',
      text: 'Hello. How are you?',
      isBot: false,
    ),
    Message(
      id: '3',
      text: 'I am fine. How are you?',
      isBot: true,
    ),
    Message(
      id: '4',
      text: 'I am fine too. Thank you.',
      isBot: false,
    ),
    Message(
      id: '5',
      text: 'You are welcome.',
      isBot: true,
    ),
    Message(
      id: '6',
      text: 'Bye',
      isBot: false,
    ),
    Message(
      id: '7',
      text: 'Bye',
      isBot: true,
    ),
  ].reversed.toList(); */
}
