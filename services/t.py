import pandas as pd

path="data/02_data_featuers.pkl"
# قراءة ملف pkl
df = pd.read_pickle(path)

# معرفة الأعمدة
print("الأعمدة:", df.columns)

# تغيير الأعمدة (مثلاً تغيير أسماء الأعمدة)
df_ = df[['acc_x', 'acc_y', 'acc_z', 'gyr_x', 'gyr_y', 'gyr_z']] # استبدل بأسماء الأعمدة الجديدة

# إعادة تخزين البيانات بعد التغيير
df_.to_pickle('data/data.pkl')
