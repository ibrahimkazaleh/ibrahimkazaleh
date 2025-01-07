// import 'dart:async';
// import 'package:flutter/material.dart';
// import 'package:sensors_plus/sensors_plus.dart';
// import 'package:http/http.dart' as http;
// import 'dart:convert';

// void main() {
//   runApp(MyApp());
// }

// class MyApp extends StatelessWidget {
//   @override
//   Widget build(BuildContext context) {
//     return MaterialApp(
//       title: 'Exercise Detection App',
//       theme: ThemeData(
//         primarySwatch: Colors.blue,
//       ),
//       home: SensorDataScreen(),
//     );
//   }
// }

// class SensorDataScreen extends StatefulWidget {
//   @override
//   _SensorDataScreenState createState() => _SensorDataScreenState();
// }

// class _SensorDataScreenState extends State<SensorDataScreen> {
//   StreamSubscription? _accelerometerSubscription;

//   @override
//   void initState() {
//     super.initState();
//     startListeningToSensors();
//   }

//   @override
//   void dispose() {
//     stopListeningToSensors();
//     super.dispose();
//   }

//   void startListeningToSensors() {
//     _accelerometerSubscription =
//         accelerometerEvents.listen((AccelerometerEvent event) {
//       double x = event.x;
//       double y = event.y;
//       double z = event.z;

//       // إرسال البيانات إلى الـ backend
//       sendSensorDataToBackend(x, y, z);
//     });
//   }

//   void stopListeningToSensors() {
//     _accelerometerSubscription?.cancel();
//   }

//   void sendSensorDataToBackend(double x, double y, double z) async {
//     var url = Uri.parse('http://your-backend-url/api/sensor-data');

//     var response = await http.post(
//       url,
//       headers: {"Content-Type": "application/json"},
//       body: jsonEncode({
//         'x': x,
//         'y': y,
//         'z': z,
//         'timestamp': DateTime.now().toIso8601String(),
//       }),
//     );

//     if (response.statusCode == 200) {
//       print("Data sent successfully!");
//     } else {
//       print("Failed to send data: ${response.statusCode}");
//     }
//   }

//   @override
//   Widget build(BuildContext context) {
//     return Scaffold(
//       appBar: AppBar(
//         title: Text('Sensor Data Screen'),
//       ),
//       body: Center(
//         child: Text('Collecting sensor data...'),
//       ),
//     );
//   }
// }
