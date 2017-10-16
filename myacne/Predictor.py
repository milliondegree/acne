from keras.models import model_from_json
from keras import applications
import matplotlib.image as mpimg
import numpy as np


class Predictor():
	
	def __init__(self, model_file_binary, weight_file_binary, model_file_seven, weight_file_seven):
		
		# load the binary-classification model
		json_file_binary = open(model_file_binary, 'r')
		model_json_binary = json_file_binary.read()
		json_file_binary.close()
		self.model_binary = model_from_json(model_json_binary)
		self.model_binary.load_weights(weight_file_binary)
		
		# load the seven-classfication model
		json_file_seven = open(model_file_seven, 'r')
		model_json_seven = json_file_seven.read()
		json_file_seven.close()
		self.model_seven = model_from_json(model_json_seven)
		self.model_seven.load_weights(weight_file_seven)

		self.model_VGG16 = applications.VGG16(include_top=False, weights='imagenet')
		
	# cut the image into pieces then return the array
	def cut_image(self, directory, cut_size = (50, 50), step = (40, 40)):
		
		img = mpimg.imread(directory)
		img = img[:,:,0:3]
		img_size = img.shape
		row_num = np.round((img_size[0]-cut_size[0])/step[0])+1
		colomn_num = np.round((img_size[1]-cut_size[1])/step[1])+1
		num_imgs = row_num * colomn_num
		cut_imgs=np.empty((num_imgs,cut_size[0],cut_size[1],img_size[2]),dtype='uint8')
		
		k = 0
		for i in range(0,row_num):
			for j in range(0,colomn_num):
				cut_imgs[k,:,:,:] = img[i*step[0]:i*step[0]+cut_size[0],j*step[1]:j*step[1]+cut_size[1],:]
				k = k + 1
		
		print cut_imgs.shape
		return cut_imgs
	
	# process the binary classification
	def binary_classify(self, cut_imgs):
		print "This is binary classification"
		cut_temp = cut_imgs * 1.0 / 255
		transimages = np.transpose(cut_temp, (0, 3, 1, 2))
		print "Start VGG16"
		bottleneck_features = self.model_VGG16.predict(transimages)
		binary_classes = self.model_binary.predict(bottleneck_features, batch_size = 1, verbose = True)
		print "Binary classification over"
		
		#find the skin indexs
		index = np.where(binary_classes[:,0] < binary_classes[:,1])[0]
		skin_imgs = bottleneck_features[index,:,:,:]
		return skin_imgs
		
	# process the seven classfication
	def seven_classify(self, skin_imgs):
		print "This is seven classification"
		
		normal_label = 3

		# predict method three
		seven_classes = self.model_seven.predict_classes(skin_imgs, batch_size = 1, verbose = True)
		nums = np.bincount(seven_classes, minlength = 7)
		print nums
		abnormal_num = skin_imgs.shape[0] - nums[normal_label]
		abnormal_ratio = int((abnormal_num * 1.0 / skin_imgs.shape[0])*10000)/10000.0
		bt_ratio = int((nums[5] * 1.0 / abnormal_num)*10000)/10000.0
		ht_ratio = int((nums[2] * 1.0 / abnormal_num)*10000)/10000.0
		qz_ratio = int((nums[0] * 1.0 / abnormal_num)*10000)/10000.0
		nb_ratio = int((nums[4] * 1.0 / abnormal_num)*10000)/10000.0
		nz_ratio = int((nums[1] * 1.0 / abnormal_num)*10000)/10000.0
		jj_ratio = int((nums[6] * 1.0 / abnormal_num)*10000)/10000.0
		return bt_ratio, ht_ratio, qz_ratio, nb_ratio, nz_ratio, jj_ratio, abnormal_ratio

		# predict method two
		# seven_classes = self.model_seven.predict(skin_imgs, verbose = True)
		# raw_ratio = np.sum(seven_classes, axis = 0)
		# sum_ratio = np.sum(raw_ratio)
		# abnormal = sum_ratio - raw_ratio[normal_label]
		# abnormal_ratio = int(abnormal*10000 / sum_ratio)/10000.0
		# bt_ratio = int((raw_ratio[5] / abnormal)*10000)/10000.0
		# ht_ratio = int((raw_ratio[2] / abnormal)*10000)/10000.0
		# qz_ratio = int((raw_ratio[0] / abnormal)*10000)/10000.0
		# nb_ratio = int((raw_ratio[4] / abnormal)*10000)/10000.0
		# nz_ratio = int((raw_ratio[1] / abnormal)*10000)/10000.0
		# jj_ratio = int((raw_ratio[6] / abnormal)*10000)/10000.0
		# print bt_ratio
		# print ht_ratio
		# print qz_ratio
		# print nb_ratio
		# print nz_ratio
		# print jj_ratio
		# return bt_ratio, ht_ratio, qz_ratio, nb_ratio, nz_ratio, jj_ratio, abnormal_ratio
		

		# predict method one
		# seven_classes = self.model_seven.predict_classes(skin_imgs, batch_size = 1, verbose = False)

		# nums = np.bincount(seven_classes)
		# normal_num = nums[normal_label]
		# abnormal_num = skin_num - normal_num
		# abnormal_ratio = abnormal_num * 1.0 / skin_num
		# if nums.shape[0] == 4:
		# 	class0 = nums[0] * 1.0 / abnormal_num
		# 	class1 = nums[1] * 1.0 / abnormal_num
		# 	class3 = nums[3] * 1.0 / abnormal_num
		# else:
		# 	class0 = nums[0] * 1.0 / abnormal_num
		# 	class1 = nums[1] * 1.0 / abnormal_num
		# 	class3 = 0 * 1.0
			
		# return class0, class1, class3, abnormal_ratio