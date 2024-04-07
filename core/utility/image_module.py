import os
import nibabel as nib
import numpy as np
import cv2

def save_slice_as_image(scanFilePath, directory, filenames=None, scale=False):
    # Load the scan and extract data using nibabel 
    scan = nib.load(scanFilePath)
    scanArray = scan.get_fdata()

    # Get and print the scan's shape 
    scanArrayShape = scanArray.shape
    print('The scan data array has the shape: ', scanArrayShape)

    # Examine scan's shape and header 
    scanHeader = scan.header
    print('The scan header is as follows: \n', scanHeader)

    # Calculate proper aspect ratios
    pixDim = scanHeader['pixdim'][1:4]
    aspectRatios = [pixDim[1]/pixDim[2], pixDim[0]/pixDim[2], pixDim[0]/pixDim[1]]
    print('The required aspect ratios are: ', aspectRatios)

    if filenames is None:
        base_name = os.path.splitext(os.path.basename(scanFilePath))[0].split(".")[0]
        filenames = [f"{base_name}_{i}" for i in range(1, 4)]

    for i, filename in enumerate(filenames, start=1):
        if i == 1:
            img = scanArray[scanArrayShape[0]//2,:,:]
            shape_str = f"{scanArrayShape[2]}_{scanArrayShape[1]}"
        elif i == 2:
            img = scanArray[:,scanArrayShape[1]//2,:]
            shape_str = f"{scanArrayShape[2]}_{scanArrayShape[0]}"
        elif i == 3:
            img = scanArray[:,:,scanArrayShape[2]//2]
            shape_str = f"{scanArrayShape[1]}_{scanArrayShape[0]}"

        # Normalize pixel values to [0, 255] range
        img = cv2.normalize(img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

        if scale:
            # Upscale the image for improved quality
            img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)

        # Convert to grayscale
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        # Save the image
        # cv2.imwrite(f"{directory}/{filename}_{shape_str}.png", img)
        cv2.imwrite(f"{directory}/{filename}", img)

    print("Images saved to " + directory)
