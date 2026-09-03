print("\nSub-region value counts:")
print(cross_verified['un_subregion'].value_counts())
 
print("\nGender value counts:")
print(cross_verified['gender'].value_counts())

print("SUMMARY")
print(database.groupby('isWestern')['ranking_visib_5criteria'].describe().round(2))
print("\n")

region_counts = cross_verified.groupby(['un_subregion', 'isWestern']).size().reset_index(name='count')
fig, ax = plt.subplots(figsize=(12, 5))
colors = region_counts['isWestern'].map({0:'#009E73', 1: '#CC79A7'})
ax.barh(region_counts['un_subregion'], region_counts['count'], color=colors)
ax.set_xlabel('Count')
ax.set_title('People per Sub-region (Blue = Western, Orange = Non-Western)')
plt.tight_layout()
plt.show()

fig, ax = plt.subplots(figsize=(8, 5))
sns.violinplot(
    x='isWestern', y='ranking_visib_5criteria',
    data=database,
    hue='isWestern',
    palette={0:'#009E73', 1: '#CC79A7'},
    legend=False,
    ax=ax
)
ax.set_xticks([0, 1])
ax.set_xticklabels(['Non-Western', 'Western'])
ax.set_xlabel('')
ax.set_ylabel('Visibility Ranking')
ax.set_yticks([ax.get_ylim()[0], ax.get_ylim()[1]])
ax.set_yticklabels(['Highest Visibility', 'Lowest Visibility'])
ax.set_title('Visibility Ranking by Western Status')
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor="#009E73", label='Western'),
    Patch(facecolor="#CC79A7", label='Non-Western'),
]
ax.legend(handles=legend_elements, loc='upper right')
plt.tight_layout()
plt.savefig("violin.pdf")
plt.show()

occupations = database['level2_main_occ'].dropna().unique()
half = len(occupations) // 2
group1 = occupations[:half]
group2 = occupations[half:]

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))

sns.boxplot(
    x='level2_main_occ', y='ranking_visib_5criteria',
    hue='isWestern',
    data=database[database['level2_main_occ'].isin(group1)],
    palette={0:'#009E73', 1: '#CC79A7'},
    ax=ax1
)
ax1.set_xticks(ax1.get_xticks())
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=40, ha='right')
ax1.set_title('Visibility Ranking by Occupation and Region (1/2)')
ax1.set_xlabel('')
ax1.set_ylabel('Visibility Ranking')
handles, _ = ax1.get_legend_handles_labels()
ax1.legend(handles, ['Non-Western', 'Western'], title='Region')

sns.boxplot(
    x='level2_main_occ', y='ranking_visib_5criteria',
    hue='isWestern',
    data=database[database['level2_main_occ'].isin(group2)],
    palette={0:'#009E73', 1: '#CC79A7'},
    ax=ax2
)
ax2.set_xticks(ax2.get_xticks())
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=40, ha='right')
ax2.set_title('Visibility Ranking by Occupation and Region (2/2)')
ax2.set_xlabel('Main Occupation')
ax2.set_ylabel('Visibility Ranking')
handles, _ = ax2.get_legend_handles_labels()
ax2.legend(handles, ['Non-Western', 'Western'], title='Region')
plt.tight_layout()

plt.savefig("box.pdf")
plt.show()

fig, ax = plt.subplots(figsize=(9, 5))
sns.boxplot(
    x='gender', y='ranking_visib_5criteria',
    hue='isWestern',
    data=database,
    palette={0:'#009E73', 1: '#CC79A7'},
    ax=ax
)
ax.set_title('Visibility Ranking by Gender and Western Status')
ax.set_xlabel('Gender')
ax.set_ylabel('Visibility Ranking')
handles, _ = ax.get_legend_handles_labels()
ax.legend(handles, ['Non-Western', 'Western'], title='Region')
plt.tight_layout()
plt.show()

