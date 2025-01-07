import 'dart:developer';

import 'package:flutter/material.dart';
// import 'views/ExercisePage.dart'; // استيراد صفحة التمرين التي أنشأناها
// import 'views/AnalysisPage.dart';
import 'views/service.dart';
// import 'SensorData.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
        debugShowCheckedModeBanner: false, // لإخفاء شعار "debug" في التطبيق
        theme: ThemeData(
          primarySwatch: Colors.blue, // تخصيص اللون الأساسي للتطبيق
        ),
        home:SensorDataPage(),
        // ExercisePage()
        // AnalysisPage(
        //           userName: 'ibra',
        //           status: 'Good',
        //           day: 'mod',
        //         ), // تحديد ExercisePage كواجهة البداية
        );
  }
}
