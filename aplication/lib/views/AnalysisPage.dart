import 'package:flutter/material.dart';

import 'ExercisePage.dart';

class AnalysisPage extends StatelessWidget {
  final String userName; // اسم المستخدم
  final String status; // الحالة (مثل "Good")
  final String day; // اليوم أو التاريخ
  // final Widget exercisePage;
  // final Widget analysisPage;

  AnalysisPage({
    required this.userName,
    required this.status,
    required this.day,
    // required this.exercisePage,
    // required this.analysisPage,
  });

  Widget _buildTopButton(
      BuildContext context, String text, Widget destinationPage) {
    return ElevatedButton(
      style: ElevatedButton.styleFrom(
        backgroundColor: Colors.white,
        foregroundColor: Colors.black,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(20),
        ),
      ),
      onPressed: () {
        Navigator.push(
          context,
          MaterialPageRoute(builder: (context) => destinationPage),
        );
      },
      child: Text(text),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black87,
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                CircleAvatar(
                  radius: 30,
                  backgroundColor: Colors.grey, // صورة المستخدم
                ),
                SizedBox(width: 10),
                Text(
                  userName,
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
            SizedBox(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                _buildTopButton(context, "EXERCISE", ExercisePage()),
                // _buildTopButton(context, "ANALYSIS", AnalysisPage()),
              ],
            ),
            SizedBox(
              height: 60,
              width: 200,
            ),
            buildStatusContainer(status, day),
            Spacer(),
            Container(
              padding: EdgeInsets.symmetric(vertical: 15),
              decoration: BoxDecoration(
                color: Colors.grey[800],
                borderRadius: BorderRadius.circular(10),
              ),
              child: Center(
                child: Text(
                  "MY ACCOUNT",
                  style: TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

buildStatusContainer(String status, String day) {
  return Container(
    width: 500,
    height: 200,
    padding: EdgeInsets.all(20),
    decoration: BoxDecoration(
      color: Colors.grey[700],
      borderRadius: BorderRadius.circular(10),
    ),
    child: Column(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(
          status, // الحالة (مثل "Good")
          style: TextStyle(
            color: Colors.white,
            fontWeight: FontWeight.bold,
          ),
        ),
        Text(
          day, // اليوم أو التاريخ
          style: TextStyle(
            color: Colors.white,
            fontWeight: FontWeight.bold,
          ),
        ),
      ],
    ),
  );
}
