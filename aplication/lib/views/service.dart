import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class SensorDataPage extends StatefulWidget {
  @override
  _SensorDataPageState createState() => _SensorDataPageState();
}

class _SensorDataPageState extends State<SensorDataPage> {
  String _responseMessage = "";

  // Function to send data and receive response
  Future<void> sendDataAndReceiveResponse() async {
    final url =
        Uri.parse('http://127.0.0.1:8000/predict'); // تعديل العنوان حسب الحاجة

    // بيانات ثابتة لإرسالها
    final data = {
      "gyr": {"time": "2024-01-01T12:00:00", "x": 1.23, "y": 4.56, "z": 7.89},
      "acc": {"time": "2024-01-01T12:00:01", "x": 9.87, "y": 6.54, "z": 3.21}
    };

    try {
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(data),
      );

      if (response.statusCode == 200) {
        // تحليل الاستجابة
        final responseData = jsonDecode(response.body);
        setState(() {
          _responseMessage = responseData['prediction']; // عرض النص المستلم
        });
      } else {
        setState(() {
          _responseMessage = "Error: ${response.statusCode} ${response.body}";
        });
      }
    } catch (error) {
      setState(() {
        _responseMessage = "Failed to connect: $error";
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Sensor Data Response")),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: sendDataAndReceiveResponse,
              child: Text("Send Data"),
            ),
            SizedBox(height: 20),
            Text(
              _responseMessage, // عرض الاستجابة هنا
              style: TextStyle(color: Colors.blue, fontWeight: FontWeight.bold),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }
}
