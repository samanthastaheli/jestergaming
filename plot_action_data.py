import pandas as pd
import matplotlib.pyplot as plt

# Load your CSV
# df = pd.read_csv("actions_acc_converted.csv")

# # Compute average value per label
# avg_values = df.groupby("label")["value"].mean().sort_index()

# # Plot
# plt.figure(figsize=(10, 5))
# plt.bar(avg_values.index, avg_values.values)
# plt.xlabel("Action")
# plt.ylabel("Average Accuracy")
# plt.title("Average Accuracy per Label")
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()



action_labels = ['action', 'five', 'four', 'journal', 'map', 'menu', 'three', 'tool', 'toolbar', 'one', 'two']
action_image_counts = [3000,1770,1805,3000,3000,1742,1751,3000,3000,1778,1769]

# Plot
plt.figure(figsize=(10, 5))
plt.bar(action_labels, action_image_counts)
plt.xlabel("Action")
plt.ylabel("Count")
plt.title("Amount Images in Actions Dataset")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
