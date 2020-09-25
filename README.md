# Darknet Toolkit
A simple script for faster training and testing of dartket based machine learning models.

# Setup
Run the setup script like so:
'''$ ./setup.sh [darknet folder path]'''

# Usage
The default folder structure must follow this criteria:
* Main folder must have the intended model name
* Must have an images folder containing images and its respective text files
* Must contain custom.nammes file

## Training
To train the model using the default folder structure and parameters use this command:
'''$ python3 model.py [-s, --save_path] [folder path]'''

Other flags include:
**-o, --objects** Change default path and file name of custom.names
**-i, --images** Change default path of /images/
**-m, --model** Change default model to be generated; default is YOLOv4
**-w, --weights** Change default weights to be used; when training used the corresponding one to the generated model and when testing uses \_best.weights
**-n, --name** Name given to the yolo.cfg file; defaults to folder name
**--custom_model** Prevend model generation and use a custom config instead
**-d, --distribution** Change the data distribution used for splitting images to training and testing sets; defaults to 0.75 or 75%

## Testing
To test the model using the default parameters:
'''$ python3 model.py [-t, --train] [-v, --video_in] [video]'''
This will output a res.avi file in the model folder.

Other flags include:
**--video_out** Change the default video output
