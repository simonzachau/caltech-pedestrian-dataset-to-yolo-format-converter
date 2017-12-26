#!/usr/bin/env python
# -*- coding: utf-8 -*-

# adapted from
# - https://github.com/mitmul/caltech-pedestrian-dataset-converter/blob/master/scripts/convert_annotations.py
# - https://pjreddie.com/media/files/voc_label.py

import os
import glob
from scipy.io import loadmat


classes = ['person', 'person-fa', 'people']
image_size = (640, 480)
datasets = {
	'train' : open('train.txt', 'w'),
	'test' : open('test.txt', 'w')
}
if not os.path.exists('labels'):
	os.makedirs('labels')

def convert_box_format(box):
	(box_x_left, box_y_top, box_w, box_h) = box
	(image_w, image_h) = image_size
	dw = 1./image_w
	dh = 1./image_h
	x = (box_x_left + box_w / 2.0) * dw
	y = (box_y_top + box_h / 2.0) * dh
	w = box_w * dw
	h = box_h * dh
	return (x, y, w, h)

for caltech_set in sorted(glob.glob('../caltech/annotations/set*')):
	set_nr = os.path.basename(caltech_set).replace('set', '')
	dataset = 'train' if int(set_r) < 6 else 'test' # dataset convention by Caltech: 0-5 are train, 6-10 are test
	set_id = dataset + set_nr

	for caltech_annotation in sorted(glob.glob(caltech_set + '/*.vbb')):
		vbb = loadmat(caltech_annotation)
		obj_lists = vbb['A'][0][0][1][0]
		obj_lbl = [str(v[0]) for v in vbb['A'][0][0][4][0]]
		video_id = os.path.splitext(os.path.basename(caltech_annotation))[0]

		for frame_id, obj in enumerate(obj_lists):
			if len(obj) > 0:
				labels = ''
				for pedestrian_id,  pedestrian_pos,  pedestrian_posv in zip(obj['id'][0], obj['pos'][0], obj['posv'][0$
					pedestrian_id = int(pedestrian_id[0][0]) - 1  # MATLAB is 1-origin
					pedestrian_pos = pedestrian_pos[0].tolist()
					pedestrian_posv = pedestrian_posv[0].tolist()
					# filter:
					if obj_lbl[pedestrian_id] in classes:
						class_index = classes.index(obj_lbl[pedestrian_id])
						yolo_box_format = convert_box_format(pedestrian_pos)
						labels += str(class_index) + ' ' + ' '.join([str(n) for n in yolo_box_format]) + '\n'
				# if no suitable labels left after filtering, continue
				if not labels:
					continue

				image_id = set_id + '_' + video_id + '_' + str(frame_id)
				datasets[dataset].write(os.getcwd() + '/images/' + image_id + '.png\n')
				label_file = open('labels/' + image_id + '.txt', 'w')
				label_file.write(labels)
				label_file.close()

				print('finished ' + image_id)

for dataset in datasets.values():
	dataset.close()