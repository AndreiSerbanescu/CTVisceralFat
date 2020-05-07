import SimpleITK as sitk
import numpy as np
import os

class Splitter():

    def __init__(self, base_dir):
        self.base_dir = base_dir

    def split(self, volume_filepath, split_no):

        image = sitk.ReadImage(volume_filepath)
        array = sitk.GetArrayFromImage(image)
        arrays = np.array_split(array, split_no, axis=0)

        filepaths = []
        for i in range(len(arrays)):
            sub_array = arrays[i]
            sub_image = sitk.GetImageFromArray(sub_array)

            filepath = os.path.join(self.base_dir, "subvol-" + str(i) + ".nii.gz")

            print("Writing volume", filepath)
            sitk.WriteImage(sub_image, filepath)

            filepaths.append(filepath)

        return filepaths