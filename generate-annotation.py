# adapted from
# - https://github.com/mitmul/caltech-pedestrian-dataset-converter/blob/master/scripts/convert_annotations.py
# - https://pjreddie.com/media/files/voc_label.py

import os
import glob
from scipy.io import loadmat


classes = ['person', 'people'] # others are 'person-fa' and 'person?'
squared = True
frame_size = (640, 640) if squared else (640, 480)
number_of_truth_boxes = 0
datasets = {
	'train' : open('train' + ('_squared' if squared else '')  + '.txt', 'w'),
	'test' : open('test' + ('_squared' if squared else '')  + '.txt', 'w')
}
if not os.path.exists('labels'):
	os.makedirs('labels')

def convertBoxFormat(box):
	(box_x_left, box_y_top, box_w, box_h) = box
	(image_w, image_h) = frame_size
	dw = 1./image_w
	dh = 1./image_h
	x = (box_x_left + box_w / 2.0) * dw
	y = (box_y_top + box_h / 2.0) * dh
	w = box_w * dw
	h = box_h * dh
	return (x, y, w, h)

# traverse sets
for caltech_set in sorted(glob.glob('../caltech/annotations/set*')):
	set_nr = os.path.basename(caltech_set).replace('set', '')
	dataset = 'train' if int(set_nr) < 6 else 'test'
	set_id = dataset + set_nr

	# traverse videos
	for caltech_annotation in sorted(glob.glob(caltech_set + '/*.vbb')):
		vbb = loadmat(caltech_annotation)
		obj_lists = vbb['A'][0][0][1][0]
		obj_lbl = [str(v[0]) for v in vbb['A'][0][0][4][0]]
		video_id = os.path.splitext(os.path.basename(caltech_annotation))[0]

		# traverse frames
		for frame_id, obj in enumerate(obj_lists):
			if len(obj) > 0:

				# traverse labels
				labels = ''
				for pedestrian_id, pedestrian_pos in zip(obj['id'][0], obj['pos'][0]):
					pedestrian_id = int(pedestrian_id[0][0]) - 1
					pedestrian_pos = pedestrian_pos[0].tolist()
					# class filter and height filter: here example for medium distance
					if obj_lbl[pedestrian_id] in classes and pedestrian_pos[3] > 30 and pedestrian_pos[3] <= 80:
						class_index = classes.index(obj_lbl[pedestrian_id])
						yolo_box_format = convertBoxFormat(pedestrian_pos)
						labels += str(class_index) + ' ' + ' '.join([str(n) for n in yolo_box_format]) + '\n'
						number_of_truth_boxes += 1

				# if no suitable labels left after filtering, continue
				if not labels:
					continue

				image_id = set_id + '_' + video_id + '_' + str(frame_id)
				datasets[dataset].write(os.getcwd() + '/images/' + image_id + ('_squared' if squared else '') + '.png\n')
				label_file = open('labels/' + image_id + ('_squared' if squared else '') + '.txt', 'w')
				label_file.write(labels)
				label_file.close()

				print('finished ' + image_id)

for dataset in datasets.values():
	dataset.close()
print(number_of_truth_boxes) # useful for statistics
