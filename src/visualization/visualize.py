import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl # to use in loop or function 

# --------------------------------------------------------------
# Load data
# --------------------------------------------------------------
df=pd.read_pickle('../../data/interim/01_data_processed.pkl')

# --------------------------------------------------------------
# Plot single columns
# --------------------------------------------------------------
set_df=df[df['set']==1]
plt.plot(set_df['acc_y'].reset_index(drop=True))


# --------------------------------------------------------------
# Plot all exercises
# --------------------------------------------------------------
for label in df['label'].unique():
    subset =df[df['label']==label]
    fig,ax=plt.subplots()
    plt.plot(subset['acc_y'].reset_index(drop=True),label=label)
    plt.legend()
    plt.show()

for label in df['label'].unique():
    subset =df[df['label']==label]
    fig,ax=plt.subplots()
    plt.plot(subset['acc_y'][:100].reset_index(drop=True),label=label)
    plt.legend()
    plt.show()
    


# --------------------------------------------------------------
# Adjust plot settings
# --------------------------------------------------------------
# mpl.style.use("seaborn-darkgrid")
mpl.style.use('seaborn-v0_8-deep')
mpl.rcParams['figure.figsize']=(20,5)
mpl.rcParams['figure.dpi']=100 
# plt.style.available


# --------------------------------------------------------------
# Compare medium vs. heavy sets
# --------------------------------------------------------------
# ------ in this case i chose the paticipant A only -----------

fig,ax=plt.subplots()
category_df=df.query("label=='squat'").query("participant=='A'").reset_index()
category_df.groupby(['category'])['acc_y'].plot() # there are sort to caregory  column 
ax.set_ylabel('acc_y')
ax.set_xlabel('sample')
plt.legend()

# --------------------------------------------------------------
# Compare participants
# --------------------------------------------------------------
# --------------- all the participant A B ... ------------------

participant_df=df.query("label=='bench'" ).sort_values("participant").reset_index()

fig,ax=plt.subplots()
participant_df.groupby(['participant'])['acc_y'].plot()
ax.set_ylabel('acc_y')
ax.set_xlabel('sample')
plt.legend()

# --------------------------------------------------------------
# Plot multiple axis
# --------------------------------------------------------------

df['label'].unique()

label='squat'
participant='E'

all_axis_df=df.query(f"label=='{label}'").reset_index()

fig,ax=plt.subplots()
all_axis_df[['acc_x','acc_y','acc_z']].plot(ax=ax)
ax.set_ylabel('acc_y')
ax.set_xlabel('sample')
plt.legend()
plt.show()

# --------------------------------------------------------------
# Create a loop to plot all combinations per sensor
# --------------------------------------------------------------

labels=df['label'].unique()
participants=df['participant'].unique()

for label in labels:
    for participant in participants:
        all_axis_df=(df.query(f"label=='{label}'")
                     .query(f"participant=='{participant}'")
                     .reset_index())
        
        if len(all_axis_df) > 0:
            fig,ax=plt.subplots()
            all_axis_df[['acc_x','acc_y','acc_z']].plot(ax=ax)
            ax.set_ylabel('acc_y')
            ax.set_xlabel('sample')
            plt.title(f"{label} ({participant})".title())
            plt.legend()
            



for label in labels:
    for participant in participants:
        all_axis_df=(df.query(f"label=='{label}'")
                     .query(f"participant=='{participant}'")
                     .reset_index())
        
        if len(all_axis_df) > 0:
            fig,ax=plt.subplots()
            all_axis_df[['gyr_x','gyr_y','gyr_z']].plot(ax=ax)
            ax.set_ylabel('gyr_y')
            ax.set_xlabel('sample')
            plt.title(f"{label} ({participant})".title())
            plt.legend()
# --------------------------------------------------------------
# Combine plots in one figure
# --------------------------------------------------------------
label ='row'
participant='A'
combined_plot_df=(
    df.query(f"label =='{label}' ")
    .query(f"participant=='{participant}'")
    .reset_index(drop=True)
)

fig, ax = plt.subplots(nrows=2,sharex=True,figsize=(20,10))
combined_plot_df[['acc_x','acc_y','acc_z']].plot(ax=ax[0])
combined_plot_df[['gyr_x','gyr_y','gyr_z']].plot(ax=ax[1])

ax[0].legend(loc='upper center',bbox_to_anchor=(0.5,1.15),ncol=3,fancybox=True,shadow=True)
ax[1].legend(loc='upper center',bbox_to_anchor=(0.5,1.15),ncol=3,fancybox=True,shadow=True)
ax[1].set_xlabel("Sample")


# --------------------------------------------------------------
# Loop over all combinations and export for both sensors
# --------------------------------------------------------------

for label in labels:
    for participant in participants:
        combined_plot_df=(df.query(f"label=='{label}'")
                     .query(f"participant=='{participant}'")
                     .reset_index())
        
        if len(combined_plot_df) > 0:

            fig, ax = plt.subplots(nrows=2,sharex=True,figsize=(20,10))
            combined_plot_df[['acc_x','acc_y','acc_z']].plot(ax=ax[0])
            combined_plot_df[['gyr_x','gyr_y','gyr_z']].plot(ax=ax[1])     
            ax[0].legend(loc='upper center',bbox_to_anchor=(0.5,1.15),ncol=3,fancybox=True,shadow=True)
            ax[1].legend(loc='upper center',bbox_to_anchor=(0.5,1.15),ncol=3,fancybox=True,shadow=True)
            ax[1].set_xlabel("Sample")

            plt.savefig(f'../../reports/figures/{label.title()} ({participant}).png')
            plt.show()