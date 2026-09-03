western_vis    = database2[database2['isWestern'] == 1]['ranking_visib_5criteria']
nonwest_vis    = database2[database2['isWestern'] == 0]['ranking_visib_5criteria']
 
u_stat, p_val  = mannwhitneyu(western_vis, nonwest_vis, alternative='two-sided')
n1, n2         = len(western_vis), len(nonwest_vis)
r_rb           = 1 - (2 * u_stat) / (n1 * n2)
pooled_std     = np.sqrt((western_vis.std()**2 + nonwest_vis.std()**2) / 2)
cohens_d       = (western_vis.mean() - nonwest_vis.mean()) / pooled_std
 
print(f"\nMann-Whitney U = {u_stat:.0f},  p = {p_val:.4e}")
print(f"Rank-biserial correlation r = {r_rb:.3f}")
print(f"Cohen's d = {cohens_d:.3f}")

model = smf.ols(
    'ranking_visib_5criteria ~ isWestern + C(bigperiod_birth)'
    ' + C(gender) + C(level2_main_occ)',
    data=database2
).fit(cov_type='HC3')
print(model.summary())
 
coef = model.params['isWestern']
ci   = model.conf_int().loc['isWestern']
pval = model.pvalues['isWestern']
print(f"\nisWestern coefficient : {coef:.2f}")
print(f"95% CI                : [{ci[0]:.2f}, {ci[1]:.2f}]")
print(f"p-value               : {pval:.4e}")

pfig, ax = plt.subplots(figsize=(7, 3.5))
ax.errorbar(
    x=coef, y=0,
    xerr=[[coef - ci[0]], [ci[1] - coef]],
    fmt='o', color='#CC79A7',
    capsize=7, capthick=1.5, markersize=9, linewidth=1.5
)
ax.axvline(0, color='#009E73', linestyle='--', linewidth=1.2)
ax.set_yticks([])
ax.set_xlabel('Effect on Visibility Ranking\n(negative = western ranks higher)')
ax.set_title(
    f'Western Status Coefficient (HC3 robust SEs)\n'
    f'Controlling for birth period, gender, occupation  |  N = {len(database2):,}'
)
plt.tight_layout()
plt.show()

fig, ax = plt.subplots(figsize=(8, 4.5))
sns.histplot(
    model.resid, kde=True,
    color='#CC79A7',
    edgecolor='white',
    ax=ax
)
ax.axvline(0, color='#009E73', linestyle='--', linewidth=1.2)
ax.set_xlabel('Residual')
ax.set_title('Residual Distribution — OLS Model')
plt.tight_layout()
plt.show()

X   = model.model.exog
vif = pd.DataFrame({
    'Variable': model.model.exog_names,
    'VIF': [variance_inflation_factor(X, i) for i in range(X.shape[1])]
}).sort_values('VIF', ascending=False)
print("\nVariance Inflation Factors:")
print(vif.to_string(index=False))

model_interaction = smf.ols(
    'ranking_visib_5criteria ~ isWestern * C(level2_main_occ) + C(bigperiod_birth) + C(gender)',
    data=database
).fit(cov_type='HC3')
print(model_interaction.summary())

interaction_terms = {
    k.replace('isWestern:C(level2_main_occ)[T.', '').replace(']', ''): v
    for k, v in model_interaction.params.items()
    if 'isWestern:' in k
}
interaction_ci = {
    k.replace('isWestern:C(level2_main_occ)[T.', '').replace(']', ''): v
    for k, v in model_interaction.conf_int().iterrows()
    if 'isWestern:' in k
}

coefs = pd.DataFrame({
    'occupation': list(interaction_terms.keys()),
    'coef': list(interaction_terms.values()),
    'lower': [v[0] for v in interaction_ci.values()],
    'upper': [v[1] for v in interaction_ci.values()]
}).sort_values('coef')

fig, ax = plt.subplots(figsize=(10, 7))
colors = ['red' if (row['lower'] > 0 or row['upper'] < 0) else 'grey' 
          for _, row in coefs.iterrows()]
ax.barh(coefs['occupation'], coefs['coef'], 
        xerr=[coefs['coef'] - coefs['lower'], coefs['upper'] - coefs['coef']],
        color=colors, capsize=4, edgecolor='black', linewidth=0.5)
ax.axvline(0, color='black', linewidth=1)
ax.set_xlabel('Interaction Coefficient\n(positive = western ranks higher number = less visible)')
ax.set_title('Western × Occupation Interaction Effects\n(Red = statistically significant)')
plt.tight_layout()
plt.savefig("interaction.pdf")
plt.show()

model_gender = smf.ols(
    'ranking_visib_5criteria ~ isWestern * C(gender) + C(level2_main_occ) + C(bigperiod_birth)',
    data=database2
).fit(cov_type='HC3')

gender_interactions = model_gender.params.filter(like='isWestern:')
gender_ci = model_gender.conf_int().filter(like='isWestern:', axis=0)
gender_pvals = model_gender.pvalues.filter(like='isWestern:')

print(pd.DataFrame({
    'coef': gender_interactions,
    'lower': gender_ci[0],
    'upper': gender_ci[1],
    'p': gender_pvals
}).round(2))

print(model_gender.summary())

