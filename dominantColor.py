# dominantColor.py

# Dominant color code taken from: https://code.likeagirl.io/finding-dominant-colour-on-an-image-b4e075f98097
# Rectangle drawing code taken from: https://stackoverflow.com/questions/37435369/matplotlib-how-to-draw-a-rectangle-on-image


import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from sklearn.cluster import KMeans

def find_histogram(clt):
	"""
	create a histogram with k clusters
	:param: clt
	:return:hist
	"""
	numLabels = np.arange(0,len(np.unique(clt.labels_)) + 1)
	(hist, _) = np.histogram(clt.labels_, bins = numLabels)

	hist = hist.astype("float")
	hist /= hist.sum()

	return hist

# Modified to print the primary color
def plot_colors2(hist, centroids):
	bar = np.zeros((50, 300, 3), dtype = "uint8")
	startX = 0

	for(percent, color) in zip(hist,centroids):
		# plot the relative percentage of each cluster
		endX = startX + (percent * 300)
		cv2.rectangle(bar, (int(startX), 0), (int(endX), 50), color.astype("uint8").tolist(), -1)
		startX = endX
		break

	# return the bar chart
	return bar


cap = cv2.VideoCapture(0)

while(True):
	# Capture the frame
	ret, frame = cap.read()
	img = frame[200:400, 200:400]

	if ret:
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

		img = img.reshape((img.shape[0] * img.shape[1],3)) #represent as row*column,channel number
		clt = KMeans(n_clusters = 3) #cluster number
		clt.fit(img)

		hist = find_histogram(clt)
		bar = plot_colors2(hist, clt.cluster_centers_)

		image = cv2.rectangle(frame, (200, 200), (400, 400), (0,0,255), 2)

		cv2.imshow("stream", image)
		cv2.imshow("majority color", bar)

		#plt.axis("off")
		#plt.imshow(bar)
		#plt.show()

	# Quit if 'q' key pressed
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()