'''
Matplotlib stuff
'''
import matplotlib.pyplot as plt



# --- ROC --- #
plt.figure(1, figsize=(14, 10))
plt.clf()

x = ''
y = ''
color = ''
label = ''
plt.plot(x, y, label=label, linewidth=2, linestyle='--', alpha=0.7, color=color)

plt.xlim((-0.01, 1.01))
plt.ylim((-0.01, 1.01))
plt.xticks([0.25, 0.5, 0.75, 1.0], fontsize=14)
plt.yticks([0.25, 0.5, 0.75, 1.0], fontsize=14)
plt.xlabel("False Positive Rate", fontsize=18)
plt.ylabel("True Positive Rate", fontsize=18)
plt.grid(alpha=0.25)
leg = plt.legend(loc='lower right', fontsize=20)
leg.get_frame().set_alpha(0.0)
plt.tight_layout()


# --- histogram --- #
plt.figure(1, figsize=(16, 10))
plt.clf()
hist_kwargs = {'align': 'left', 'alpha': 0.25, 'log': True}

data = ''
color = ''
label = ''

plt.hist(data, bins=100, color=color, label=label, **hist_kwargs)
plt.hist(data, bins=100, color=color, linewidth=2, fill=False, histtype='step', **hist_kwargs)

plt.xlabel('Measured Value', fontsize=16)
plt.ylabel('Counts', fontsize=16)
plt.tight_layout()
plt.tight_layout()
