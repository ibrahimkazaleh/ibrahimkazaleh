import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from DataTransformation import LowPassFilter, PrincipalComponentAnalysis
from TemporalAbstraction import NumericalAbstraction
from FrequencyAbstracktion import FourierTransformation
from sklearn.cluster import KMeans



# --------------------------------------------------------------
# Load data
# --------------------------------------------------------------
df=pd.read_pickle('../../data/interim/01_data_processed.pkl')

predictor_coloumns=list(df.columns[:6])

# plote setting 
plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize']=(20,5)
plt.rcParams['figure.dpi']=100 
plt.rcParams['lines.linewidth']=2
# plt.style.available

# --------------------------------------------------------------
# Dealing with missing values (imputation)
# --------------------------------------------------------------

df.info()
# in this to undstand the the missing value but we dont have it 
subset=df[df['set']==35]['acc_y'].plot()

for col in predictor_coloumns:
    df[col]=df[col].interpolate()


# --------------------------------------------------------------
# Calculating set duration
# --------------------------------------------------------------

# subset=df[df['set']==25]['acc_y'].plot() 
# subset=df[df['set']==50]['acc_y'].plot() 

# dirent between last and first 
duration =df[df['set']==1].index[-1]-df[df['set']==1].index[0]

# من خلال وجود اندكس يوجد ترتيب دائما فلا فالقيمه دائما اكبر من الصفر 
 
duration.seconds

for s in df['set'].unique():
    start =df[df['set']==s].index[0]
    stop=df[df['set']==s].index[-1]
    duration=stop-start
    df.loc[(df['set']==s),'duration']=duration.seconds

df[df['set']==64]
df['set'].unique()

duration_df=df.groupby(['category'])['duration'].mean()

duration_df.iloc[0]/5
duration_df.iloc[1]/10
# معرفه الوقت الذي استغرقه كل تمرين  

# --------------------------------------------------------------
# Butterworth lowpass filter
# --------------------------------------------------------------
df_lowpass = df.copy()
LowPass = LowPassFilter()

fs = 1000 / 200
cutoff = 1.3

df_lowpass = LowPass.low_pass_filter(df_lowpass, "acc_y", fs, cutoff, order=5)

subset = df_lowpass[df_lowpass["set"] == 45]
print(subset["label"][0])

fig, ax = plt.subplots(nrows=2, sharex=True, figsize=(20, 10))
ax[0].plot(subset["acc_y"].reset_index(drop=True), label="raw data")
ax[1].plot(subset["acc_y_lowpass"].reset_index(drop=True), label="butterworth filter")
ax[0].legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), fancybox=True, shadow=True)
ax[1].legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), fancybox=True, shadow=True)

for col in predictor_coloumns:
    df_lowpass = LowPass.low_pass_filter(df_lowpass,col, fs, cutoff, order=5)
    df_lowpass[col]=df_lowpass[col +'_lowpass']
    del df_lowpass[col +'_lowpass']


    
# --------------------------------------------------------------
# Principal component analysis PCA
# --------------------------------------------------------------

df_pca=df_lowpass.copy()

PCA=PrincipalComponentAnalysis()

PC_values=PCA.determine_pc_explained_variance(df_pca,predictor_coloumns)

plt.figure(figsize=(10,10))
plt.plot(range(1,len(PC_values)+1),PC_values)
plt.xlabel('principal component number ')
plt.ylabel('explained veraince')
plt.show()

df_pca=PCA.apply_pca(df_pca,predictor_coloumns,3)


subset=df_pca[df_pca['set']==35]
subset[['pca_1','pca_2','pca_3']].plot(subplots=True)
# --------------------------------------------------------------
# Sum of squares attributes
# --------------------------------------------------------------

df_squared =df_pca.copy()

acc_r=df_squared['acc_x']**2 + df_squared['acc_x'] **2+df_squared['acc_x']**2
gyr_r=df_squared['gyr_x']**2 + df_squared['gyr_x'] **2+df_squared['gyr_x']**2

df_squared['acc_r']=np.sqrt(acc_r)
df_squared['gyr_r']=np.sqrt(gyr_r)

subset=df_squared[df_pca['set']==17]

subset[['acc_r','gyr_r']].plot(subplots=True)

# --------------------------------------------------------------
# Temporal abstraction
# --------------------------------------------------------------
df_temporal =df_squared.copy()
NumAbs =NumericalAbstraction()

predictor_coloumns=predictor_coloumns + ['acc_r','gyr_r']

ws=int(1000/200)

for col in predictor_coloumns:
    NumAbs.abstract_numerical(df_temporal,[col],ws,'mean')
    NumAbs.abstract_numerical(df_temporal,[col],ws,'std')

# القيم غير دقيقه فعلييا لان الانحراف المعياري يقوم بأخذ 4 قيم سابقه ( حجم النافذه ) لذلك فإنه من الممكن 
# ان يكون الانحراف المعياري غير دقيق في بعض الحالات لذلك سنقوم بالعمل الى المطموعات كل واحده على حدا 

df_temporal_list=[]
for s in df_temporal['set'].unique():
    subset=df_temporal[df_temporal['set']==s].copy()
    for col in predictor_coloumns:
        NumAbs.abstract_numerical(subset,[col],ws,'mean')
        NumAbs.abstract_numerical(subset,[col],ws,'std')
    df_temporal_list.append(subset)

df_temporal=pd.concat(df_temporal_list)


subset[['gyr_x','gyr_x_temp_mean_ws_5','gyr_x_temp_std_ws_5']].plot()
subset[['acc_x','acc_x_temp_mean_ws_5','acc_x_temp_std_ws_5']].plot()
# df_temporal.info()

# --------------------------------------------------------------
# Frequency features
# --------------------------------------------------------------
df_freq = df_temporal.copy().reset_index()

FreqAbs = FourierTransformation()

ws=int(1000/200)
fs=int(2800/200)

df_freq=FreqAbs.abstract_frequency(df_freq,['acc_x'],6,fs)

subset=df_freq[df_freq['set']==17]
subset[['acc_x']].plot()
subset[[
    'acc_x_freq_7.0_Hz_ws_6',
    'acc_x_freq_0.0_Hz_ws_6',
    'acc_x_pse',
    'acc_x_freq_weighted',
    'acc_x_max_freq'
        ]].plot()

df_freq_list=[]
for s in df_freq['set'].unique():
    print(f'apply the Fourier transform to set {s}')
    subset=df_freq[df_freq['set']==s].reset_index(drop=True).copy()
    FreqAbs.abstract_frequency(subset,predictor_coloumns,6,fs)
    df_freq_list.append(subset)

df_freq=pd.concat(df_freq_list).set_index("epoch (ms)",drop=True)
# --------------------------------------------------------------
# Dealing with overlapping windows
# --------------------------------------------------------------
df_freq=df_freq.dropna()
df_freq=df_freq.iloc[::2]

# --------------------------------------------------------------
# Clustering
# --------------------------------------------------------------
df_cluster =df_freq.copy()

cluster_columns=['acc_x','acc_y','acc_z']
K_values=range(2,20)
interias =[]

for k in K_values:
    subset=df_cluster[cluster_columns]
    kmeans=KMeans(n_clusters=k,n_init=20,random_state=0)
    cluster_lable =kmeans.fit_predict(subset)
    interias.append(kmeans.inertia_)


plt.figure(figsize=(10,10))
plt.plot(K_values,interias)
plt.xlabel('k value')
plt.ylabel('sum fo squard distenecs')
plt.show() 
# the 5 is goode cluster 


kmeans=KMeans(n_clusters=5,n_init=20,random_state=0)
subset=df_cluster[cluster_columns]
df_cluster['cluster'] =kmeans.fit_predict(subset)
df_cluster['cluster'].unique()


# Plote cluster 
fig=plt.figure(figsize=(18,18))
ax=fig.add_subplot(projection='3d')
for c in df_cluster['cluster'].unique():
    subset=df_cluster[df_cluster['cluster']==c]
    ax.scatter(subset['acc_x'],subset['acc_y'],subset['acc_z'],label=c)
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')
plt.legend()
plt.show()

# Plote label 
fig=plt.figure(figsize=(18,18))
ax=fig.add_subplot(projection='3d')
for l in df_cluster['label'].unique():
    subset=df_cluster[df_cluster['label']==l]
    ax.scatter(subset['acc_x'],subset['acc_y'],subset['acc_z'],label=l)
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')
plt.legend()
plt.show()
# --------------------------------------------------------------
# Export dataset
# --------------------------------------------------------------

df_cluster.to_pickle('../../data/interim/02_data_featuers.pkl')

df_cluster.columns

