import pickle
import json
import glob
import os


classes = ['person', 'person-fa', 'people']
image_folder_path = 'images'
image_size = (640, 480)
datasets = {
	'train' : open('train.txt', 'w'), 
	'test' : open('test.txt', 'w') 
}
annotations = json.load(open('annotations.json'))
if not os.path.exists('labels'):
    os.makedirs('labels')

def convert_box_format((box_x_left, box_y_top, box_w, box_h)):
	dw = 1./image_size[0]
	dh = 1./image_size[1]
	x = (box_x_left + box_w / 2.0) * dw
	y = (box_y_top + box_h / 2.0) * dh
	w = box_w * dw
	h = box_h * dh
	return (x, y, w, h)

def write_label_file(labels, file_name):
	label_file = open('labels/' + file_name, 'w')
	for label in labels:
		class_index = classes.index(label['lbl'])
		yolo_box_format = convert_box_format((float(n) for n in label['pos']))
		label_file.write(str(class_index) + ' ' + ' '.join([str(n) for n in yolo_box_format]) + '\n')
	label_file.close()

for file_path in sorted(glob.glob(image_folder_path + '/*.png')):
	file_name = file_path.replace(image_folder_path + '/', '').replace('.png', '')
	[dataset_folder_nr, video_nr, frame_nr] = file_name.replace('train', '').replace('test', '').split('_')

	# check if the frame is annotated
	if frame_nr in annotations['set' + dataset_folder_nr][video_nr]['frames']:
		labels = [label for label in annotations['set' + dataset_folder_nr][video_nr]['frames'][frame_nr] 
		if (label['lbl'] in classes # only labels that exist
		# TODO: only big enough pedestrians (>= 50 px)
		# TODO: only pedestrians that are at least 65% visible
		)]
		# if no suitable labels left, continue
		if not labels:
			continue
		write_label_file(labels, file_name + '.txt')

		for dataset_key in datasets.keys():
			if dataset_key in file_path:
				datasets[dataset_key].write(os.getcwd() + '/' + file_path + '\n')
				break

for dataset in datasets.values():
	dataset.close()
