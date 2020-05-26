#!/usr/bin/python3
# -*- coding: utf-8 -*-
# File  : load_data.py
# Author: LU Chongkai
# Date  : 23/5/2019




def load_trimmed_images(train_ground_truth_path, test_ground_truth_path , train_directory , test_directory, *y_range):
    """
    This function is used for load trimmed images. In case of buffer cannot store too much images, only the path of images will be output instead of loading true image.
    In addition, this function will also output completeness labels of each frame.
    :param train_ground_truth_path:
        String. Path where the temporal annotation file (csv) for training locates.
    :param test_ground_truth_path:
        String. Path where the temporal annotation file (csv) for test locates.
    :param train_directory:
        String. Path where train images locate.
    :param train_directory:
        String. Path where test images locate.
    :param y_range:
        Tuple. Consists of 2 int number. Show the range of completeness: [for_start, for_end].
    :return:
        List. Four numpy arrays. [Traim images paths, Train labels, Test images paths, Test labels].
    Example arguments:
    train_directory = "/mnt/louis-consistent/Datasets/THUMOS14/Validation"
    test_directory = "/mnt/louis-consistent/Datasets/THUMOS14/Test"
    train_ground_truth_path = "/mnt/louis-consistent/Datasets/THUMOS14/TH14_Temporal_annotations_validation/annotationF/BaseballPitch_valF.csv"
    test_ground_truth_path = "/mnt/louis-consistent/Datasets/THUMOS14/TH14_Temporal_annotations_test/annotationF/BaseballPitch_testF.csv"
    y_range = [0, 100]
    """
    import pandas as pd
    import numpy as np

    train_ground_truth = pd.read_csv(train_ground_truth_path, header=None)
    test_ground_truth = pd.read_csv(test_ground_truth_path, header=None)

    train_pathlist, train_labellist = [], []
    for i_r, row in train_ground_truth.iterrows():
        action_length = row.values[2] + 1 - row.values[1]
        train_pathlist.extend(["{}/{}/{}.jpg".format(train_directory, row.values[0], str(num).zfill(5)) for num in
                               np.arange(row.values[1], row.values[2] + 1)])
        train_labellist.extend(np.linspace(*y_range, num=action_length, dtype=np.float32))
    test_pathlist, test_labellist = [], []
    for i_r, row in test_ground_truth.iterrows():
        action_length = row.values[2] + 1 - row.values[1]
        test_pathlist.extend(["{}/{}/{}.jpg".format(test_directory, row.values[0], str(num).zfill(5)) for num in
                              np.arange(row.values[1], row.values[2] + 1)])
        test_labellist.extend(np.linspace(*y_range, num=action_length, dtype=np.float32))
    return np.array(train_pathlist), np.array(train_labellist), np.array(test_pathlist), np.array(test_labellist)


def get_video(location='C:\WorkSpace\TAL\gd', name='task1'):
    import pandas as pd
    from tensorflow.keras.applications.resnet50 import preprocess_input
    from keras_preprocessing.image import ImageDataGenerator
    gd = pd.read_csv('{}/{}/{}_gd'.format(location, name, name), index_col=['Useful', 'Data_Index']).droplevel(0, 0)[
        'Task_End']
    datagen = ImageDataGenerator(preprocessing_function=preprocess_input)
    video_generators = []
    for index, item in gd.items():
        video_df = pd.DataFrame({'paths': ['{}/{}/{}/{}.jpg'.format(location, name, index, str(num).zfill(4)) for num in
                                           list((range(item + 1)))]})

        video_generators.append(datagen.flow_from_dataframe(video_df, x_col='paths', target_size=(224, 224),
                                                            class_mode=None, batch_size=256, shuffle=False))
    return video_generators


def get_untrimmed_video(video_path):
    """
    To creat a datagenerator (Keras) instance which contains all images, unshuffled, of a given untrimmed video file folder.
    This function may cost some time to read files. While if you need do this multiple times, you can save a file which stores all images paths to aviod repeating loading.
    :param video_path:
        String. The path of untrimmed video folder which consists of images. Name of images should can be sorted with
        "sorted" function
    :return:
        DataFrameIterator(Keras).
    """
    import pandas as pd
    from pathlib import Path
    from tensorflow.keras.applications.resnet50 import preprocess_input
    from keras_preprocessing.image import ImageDataGenerator

    video_PathObject = Path(video_path)
    image_paths = [str(p) for p in sorted(video_PathObject.iterdir())]
    datagen = ImageDataGenerator(preprocessing_function=preprocess_input)
    video_df = pd.DataFrame({'paths': image_paths})
    video_generator = datagen.flow_from_dataframe(video_df, x_col='paths', target_size=(224, 224), class_mode=None,
                                                  batch_size=32, shuffle=False)
    return video_generator
