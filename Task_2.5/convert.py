import os
import subprocess


def create_result_directory(result_directory):
	if os.path.exists(result_directory) is True:
		result_files = [os.path.join(result_directory, file) for file in os.listdir(result_directory)]
		[os.remove(file) for file in result_files]
	else:
		os.mkdir(result_directory)

def convert_pictures_size(size, external_prog, source_dir, result_dir):
	size = str(size)
	convert = os.path.join(os.getcwd(), external_prog)
	create_result_directory(result_dir)
	source_directory = os.path.join(os.getcwd(), source_dir)
	result_directory = os.path.join(os.getcwd(), result_dir)
	source_files = os.listdir(source_directory)
	result_files = ["{0}-{1}".format(size, file) for file in source_files]
	source_files = [os.path.join(source_directory, file) for file in os.listdir(source_directory)]
	result_files = [os.path.join(result_directory, file) for file in result_files]
	for source_file, result_file in zip(source_files, result_files):
		subprocess.call("{0} {1} -resize {2} {3}".format(convert, source_file, size, result_file))


convert_pictures_size(200, "convert.exe", "Source", "Result")

