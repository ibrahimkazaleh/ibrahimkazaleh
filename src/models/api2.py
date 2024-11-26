from joblib import dump, load
learner = load('../../models/random_forest_model.joblib')



# هذا التابع يقوم بتحويل البيانات التي نخصل عليها من الحساس الى الشكل الذي يمكن للموديل الذكاء الاستفاده منه 
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from joblib import load
from DataTransformation import LowPassFilter, PrincipalComponentAnalysis

def preprocess_sensor_data(df):
    """
    This function processes raw sensor data and transforms it into the format
    that is compatible with the trained model. The function extracts relevant 
    features, such as basic features, square features, PCA features, time features, 
    frequency features, and clustering features.

    Args:
    df (pd.DataFrame): Raw sensor data DataFrame.

    Returns:
    pd.DataFrame: Processed DataFrame ready for model prediction.
    """
    
    # Step 1: Basic features
    basic_features = ["acc_x", "acc_y", "acc_z", "gyr_x", "gyr_y", "gyr_z"]
    
    # Step 2: Square features (compute the magnitude of acceleration and gyroscope)
    df['acc_r'] = np.sqrt(df['acc_x']**2 + df['acc_y']**2 + df['acc_z']**2)
    df['gyr_r'] = np.sqrt(df['gyr_x']**2 + df['gyr_y']**2 + df['gyr_z']**2)
    
    # Step 3: PCA features (Apply the saved PCA model)
    # Assuming the PCA model was trained and saved earlier
    # pca_model = load('pca_model.joblib')  # Load pre-trained PCA model
    pca_features = ["pca_1", "pca_2", "pca_3"]

    
        
    df_pca=df.copy()

    PCA=PrincipalComponentAnalysis()

    PC_values=PCA.determine_pc_explained_variance(df_pca,predictor_coloumns)

    df_pca=PCA.apply_pca(df_pca,predictor_coloumns,3)

    
    # Apply PCA transformation to the data
    pca_transformed = pca_model.transform(df[basic_features])
    df[pca_features] = pd.DataFrame(pca_transformed, columns=pca_features)
    
    # Step 4: Temporal abstraction features (e.g., mean, standard deviation over time windows)
    df['acc_x_temp_mean'] = df['acc_x'].rolling(window=10).mean()
    df['acc_y_temp_mean'] = df['acc_y'].rolling(window=10).mean()
    df['acc_z_temp_mean'] = df['acc_z'].rolling(window=10).mean()
    df['gyr_x_temp_mean'] = df['gyr_x'].rolling(window=10).mean()
    df['gyr_y_temp_mean'] = df['gyr_y'].rolling(window=10).mean()
    df['gyr_z_temp_mean'] = df['gyr_z'].rolling(window=10).mean()
    
    time_features = [f for f in df.columns if "_temp_" in f]
    
    # Step 5: Frequency domain features (Fourier transformation or similar)
    freq_features = [f for f in df.columns if (("_freq" in f) or ("_pse" in f))]
    
    # Step 6: Clustering feature (assuming clustering has been done and cluster labels are added)
    cluster_model = KMeans(n_clusters=5, random_state=42)
    df['cluster'] = cluster_model.fit_predict(df[basic_features])
    cluster_features = ["cluster"]

    # Combine all features
    final_features = basic_features + ['acc_r', 'gyr_r'] + pca_features + time_features + freq_features + cluster_features
    
    # Return the processed dataframe with selected features
    return df[final_features]


# هنا يتم الوصول الى البيانات التي نحثل عليها من الحساس لينقوم بالتعديل عليها 
# تجربته
import pandas as pd
from glob import glob

single_file_gyr=pd.read_csv('../../data/raw/MetaMotion/A-bench-heavy2-rpe8_MetaWear_2019-01-11T16.10.08.270_C42732BE255C_Gyroscope_25.000Hz_1.4.4.csv')

# --------------------------------------------------------------
def read_data_from_files(files):

    acc_df=pd.DataFrame()
    gyr_df=pd.DataFrame()

    acc_set=1
    gyr_set=1


    for f in files:
        participant=f.replace(bath_file,"").split('-')[0]# A
        lable=f.split('-')[1] # banch
        catagory =f.split('-')[2].replace('_MetaWear_2019','').rstrip('123') # heavy

        df=pd.read_csv(f)

        df['participant']=participant
        df['lable']=lable
        df['category']=catagory

        if 'Accelerometer' in f :
            df['set']=acc_set
            acc_set+=1
            acc_df=pd.concat([acc_df,df])


        if 'Gyroscope' in f :
            df['set']=gyr_set
            gyr_set+=1
            gyr_df=pd.concat([gyr_df,df])

        # set the time as index 
    acc_df.index=pd.to_datetime(acc_df['epoch (ms)'],unit= "ms") 
    gyr_df.index=pd.to_datetime(gyr_df['epoch (ms)'],unit= "ms") 


    del acc_df['epoch (ms)']
    del acc_df['time (01:00)']
    del acc_df['elapsed (s)']

    del gyr_df['epoch (ms)']
    del gyr_df['time (01:00)']
    del gyr_df['elapsed (s)']

    return acc_df,gyr_df







# ---------------------------------
# ------ read the single file -----



single_file_acc=pd.read_csv('../../data/raw/MetaMotion/A-bench-heavy2-rpe8_MetaWear_2019-01-11T16.10.08.270_C42732BE255C_Accelerometer_12.500Hz_1.4.4.csv')


single_file_gyr=pd.read_csv('../../data/raw/MetaMotion/A-bench-heavy2-rpe8_MetaWear_2019-01-11T16.10.08.270_C42732BE255C_Gyroscope_25.000Hz_1.4.4.csv')
type(single_file_acc)

# -------------------------------
# --------geat the single Row ---
# -------------------------------

acc_df=single_file_acc
gyr_df=single_file_gyr

# -------------------------------
# set the time is index 
acc_df.index=pd.to_datetime(acc_df['epoch (ms)'],unit= "ms") 
gyr_df.index=pd.to_datetime(gyr_df['epoch (ms)'],unit= "ms")



del acc_df['epoch (ms)']
del acc_df['time (01:00)']
del acc_df['elapsed (s)']

del gyr_df['epoch (ms)']
del gyr_df['time (01:00)']
del gyr_df['elapsed (s)']


# -----------------------------
# --------وضع البيانات في ملف واحد  -------------
# -------------------------------


new_df = pd.DataFrame([single_file_acc.iloc[0], single_file_gyr.iloc[0]])
# del new_df['epoch (ms)']
# del new_df['elapsed (s)']




# --------------------------------------------------------------
# Merging datasets
# --------------------------------------------------------------
# o => row   1 => column 
data_merged=pd.concat([acc_df.iloc[:,:3],gyr_df],axis=1)

# --------------------------------------------------------------
# Resample data (frequency conversion)
# --------------------------------------------------------------

# Accelerometer:    12.500HZ
# Gyroscope:        25.000Hz


# renmae the data 
data_merged.columns = [
    "acc_x",
    "acc_y",
    "acc_z",
    "gyr_x",
    "gyr_y",
    "gyr_z",
   
]



sampling ={
    'acc_x':'mean',
    'acc_y':'mean',
    'acc_z':'mean',
    'gyr_x':'mean',
    'gyr_y':'mean',
    'gyr_z':'mean',
    
}



data_merged[:1000].resample(rule='200ms').apply(sampling)


# split by days
days=[g for n ,g in data_merged.groupby(pd.Grouper(freq='D'))]


data_resampled=pd.concat([df.resample(rule='200ms').apply(sampling).dropna() for df in days])
data_resampled.info()

# ---------------------------------
# ------- column ------------------

predictor_coloumns=list(df.columns[:6])



basic_features = ["acc_x", "acc_y", "acc_z", "gyr_x", "gyr_y", "gyr_z"]
square_features = ["acc_r", "gyr_r"]
pca_features = ["pca_1", "pca_2", "pca_3"]
time_features = [f for f in final_df.columns if "_temp_" in f]
cluster_features = ["cluster"]
freq_features = [f for f in final_df.columns if (("_freq" in f) or ("_pse" in f))]


featuer_set_1 =list(set(basic_features))
featuer_set_2=list(set(basic_features + square_features + pca_features))
featuer_set_3=list(set(featuer_set_2 + time_features))
featuer_set_4=list(set(featuer_set_3 + freq_features + cluster_features))


final_df=preprocess_sensor_data(data_resampled)

# ----------------------------------
# ---- prodected model -----------
# ----------------------------------




# قم بمعالجة البيانات كما فعلت أثناء التدريب (مثل استخراج الميزات، PCA، إلخ.)
new_data_processed = final_df[featuer_set_4]

# التنبؤ
predictions = learner.random_forest.predict(new_data_processed)

# عرض النتائج
print(predictions)