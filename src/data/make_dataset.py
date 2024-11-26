import pandas as pd
from glob import glob

# --------------------------------------------------------------
# Read single CSV file
# --------------------------------------------------------------
# there are a MetaMotion
single_file_acc=pd.read_csv('../../data/raw/MetaMotion/A-bench-heavy2-rpe8_MetaWear_2019-01-11T16.10.08.270_C42732BE255C_Accelerometer_12.500Hz_1.4.4.csv')


single_file_gyr=pd.read_csv('../../data/raw/MetaMotion/A-bench-heavy2-rpe8_MetaWear_2019-01-11T16.10.08.270_C42732BE255C_Gyroscope_25.000Hz_1.4.4.csv')

# --------------------------------------------------------------
# List all data in data/raw/MetaMotion
# --------------------------------------------------------------
files=glob('../../data/raw/MetaMotion/*.csv')
len(files)
type(files)


# --------------------------------------------------------------
# Extract features from filename
# --------------------------------------------------------------
bath_file='../../data/raw/MetaMotion\\'

f=files[3]
# there are a problem whene i write => participant=f[0].split('-')[0].replace(bath_file,"") 

participant=f.replace(bath_file,"").split('-')[0] # A
lable=f.split('-')[1] # banch
catagory =f.split('-')[2].replace('_MetaWear_2019','').rstrip('123') # heavy

df=pd.read_csv(f)

df['participant']=participant
df['lable']=lable
df['category']=catagory


# --------------------------------------------------------------
# Read all files
# --------------------------------------------------------------
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
    

acc_df[acc_df['set']==2]



# --------------------------------------------------------------
# Working with datetimes
# --------------------------------------------------------------


df['epoch (ms)']
df['time (01:00)']
df.info()

# the diffrence between UTC and CET winter time 
pd.to_datetime(df['epoch (ms)'],unit= "ms") 

# df['time (01:00)'].dt.month # error
# ----
pd.to_datetime(df["time (01:00)"]).dt.month

# -----------------------
# set the time as index 
acc_df.index=pd.to_datetime(acc_df['epoch (ms)'],unit= "ms") 
gyr_df.index=pd.to_datetime(gyr_df['epoch (ms)'],unit= "ms") 


del acc_df['epoch (ms)']
del acc_df['time (01:00)']
del acc_df['elapsed (s)']

del gyr_df['epoch (ms)']
del gyr_df['time (01:00)']
del gyr_df['elapsed (s)']


# --------------------------------------------------------------
# Turn into function
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


acc_df,gyr_df=read_data_from_files(files)


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
    "participant",
    "label",
    "category",
    "set",
]



sampling ={
    'acc_x':'mean',
    'acc_y':'mean',
    'acc_z':'mean',
    'gyr_x':'mean',
    'gyr_y':'mean',
    'gyr_z':'mean',
    'participant':'last',
    'label':'last',
    'category':'last',
    'set':'last'
}



data_merged[:1000].resample(rule='200ms').apply(sampling)


# split by days
days=[g for n ,g in data_merged.groupby(pd.Grouper(freq='D'))]


data_resampled=pd.concat([df.resample(rule='200ms').apply(sampling).dropna() for df in days])
data_resampled.info()

data_resampled['set']=data_resampled['set'].astype('int')

# --------------------------------------------------------------
# Export dataset
# --------------------------------------------------------------

data_resampled.to_pickle('../../data/interim/01_data_processed.pkl')


# 2019-01-20 17:35:13.622
# 2019-01-11 15:08:04	S
# 2019-01-11 15:08:05.000   , 2019-01-11 15:08:05.200	   ms