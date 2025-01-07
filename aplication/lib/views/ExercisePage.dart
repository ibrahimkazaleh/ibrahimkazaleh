import 'package:flutter/material.dart';
import 'AnalysisPage.dart';
// import 'SensorData.dart';

class ExercisePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black, // خلفية داكنة حسب تصميمك
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        title: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // _buildTopButton(context, "EXERCISE", ExercisePage()),
            _buildTopButton(
                context,
                "ANALYSIS",
                AnalysisPage(
                  userName: 'ibra',
                  status: 'Good',
                  day: 'mod',
                )),
          ],
        ),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // الدائرة التي تعرض صورة التمرين
            Container(
              width: 200,
              height: 200,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: Colors.blue, // لون الدائرة
              ),
              child: Center(
                child: Icon(
                  Icons.fitness_center, // أيقونة أو صورة للتمرين
                  color: Colors.white,
                  size: 100,
                ),
              ),
            ),
            SizedBox(height: 20),
            // عداد العدات
            Text(
              'Reps: 0', // سيكون متغير حسب العدد المكتشف
              style: TextStyle(color: Colors.white, fontSize: 24),
            ),
          ],
        ),
      ),
      bottomNavigationBar: BottomAppBar(
        color: Colors.transparent,
        elevation: 0,
        child: Padding(
          padding: const EdgeInsets.all(8.0),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              IconButton(
                icon: Icon(Icons.home, color: Colors.blue),
                onPressed: () {
                  // فعالية زر الصفحة الرئيسية
                },
              ),
              TextButton(
                onPressed: () {
                  // فعالية زر "MY ACCOUNT"
                },
                child: Text(
                  "MY ACCOUNT",
                  style: TextStyle(color: Colors.white),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  // دالة لإنشاء الأزرار العلوية
  Widget _buildTopButton(
      BuildContext context, String text, Widget destinationPage) {
    return ElevatedButton(
      style: ElevatedButton.styleFrom(
        backgroundColor: Colors.white, // بدلاً من primary
        foregroundColor: Colors.black, // بدلاً من onPrimary
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(20),
        ),
      ),
      onPressed: () {
        // التنقل إلى الصفحة الوجهة
        Navigator.push(
          context,
          MaterialPageRoute(builder: (context) => destinationPage),
        );
      },
      child: Text(text),
    );
  }
}
