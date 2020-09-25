import os
import random

yolo_conv_files = {
    "YOLOv4": "yolov4.conv.137",
    "YOLOv4TINY": "yolov4-tiny.conv.29"
}


cur_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(cur_dir, "darknet_path.txt")) as f:
    darknet = os.path.join(f.readline(), "darknet")

def check4file(conv_layers, download):
    """Checks if file exists, if not, downloads it."""
    if not os.path.exists(os.path.join(cur_dir, "weights", conv_layers)):
        os.system(f"wget -P {os.path.join(cur_dir, 'weights')} {download}")

def generate_detector(dir, classes, train, valid, names, backup):
    """Generates detector.data file"""
    with open(os.path.join(dir, "detector.data"), 'w') as detector:
        detector.write(f"classes={classes}\n")
        detector.write(f"train={train}\n")
        detector.write(f"valid={valid}\n")
        detector.write(f"names={names}\n")
        detector.write(f"backup={backup}")

def list2file(file, arr):
    with open(file, 'w') as oFile:
        for item in arr:
            oFile.write(f"{item}\n")

def distribute(arr, distribution):
    """Returns two list from the original in a random distribution"""
    random.shuffle(arr)
    distributed = []
    dist = int(len(arr) * distribution)
    distributed.append(arr[0:dist])
    distributed.append(arr[dist:])
    return distributed

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='YOLO model trainer and tester.\nRecommended structure is items in save path and images in save_path/images/\nusage: model.py -s path/model/.')
    parser.add_argument('-t', '--test', dest='test', action='store_false',
                        help="Test the model.")
    parser.add_argument('-o', '--objects', type=str,
                        help="Text file containing the objects in appropriate order.")
    parser.add_argument('-i', '--images', nargs='+', type=str,
                        help="Folder or multiple folders containing images.")
    parser.add_argument('-m', '--model', type=str, default='YOLOv4',
                        help="The yolo model to use. Included models are YOLOv4 & YOLOv4TINY")
    parser.add_argument('-w', '--weights', type=str,
                        help="Assign custom weights instead of the training ones.")
    parser.add_argument('-s', '--save_path', type=str,
                        help="The save path for the model.")
    parser.add_argument('-n', '--name', type=str,
                        help="The name of the model.")
    parser.add_argument('--custom_model', type=str,
                        help="If used no model will be generated and will use the provided one.")
    parser.add_argument('-d', '--distribution', type=int, default=0.75,
                        help="Percentage of data distribution. Default is 0.75")
    parser.add_argument('-v', '--video_in', type=str,
                        help="Video to test the model. Default is save_path")
    parser.add_argument('--video_out', type=str,
                        help="Output of the tested video.")

    args = parser.parse_args()




    # -- DIRECTORY HANDLING --

    # Get current working model directory path
    save_path = args.save_path
    if save_path is None:
        save_path = os.path.join(cur_dir, "trained_models", model_name)
    else:
        save_path = os.path.abspath(save_path)

    # If no model name is given use the folder name its currently on
    model_name = args.name
    if model_name is None:
        model_name = save_path.split("/")[-1]

    # Create dir if it doesnt exist
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # Create weights folder if it doesnt exist
    weights_path = os.path.join(save_path, "weights")
    if not os.path.exists(weights_path):
        os.makedirs(weights_path)

    # If no object path is given assume its in save_path/
    object_path = args.objects
    if object_path is None:
        object_path = os.path.join(save_path, "custom.names")
    else:
        object_path = os.path.abspath(object_path)
    



    # -- IMAGE HANDLING --

    # If no image path is given assume its in save_path/images
    image_path = args.images
    if image_path is None:
        image_path = [os.path.join(save_path, "images")]
    else:
        image_path = os.path.abspath(image_path)

    # Distribute images and write a file with their paths
    # NOTE: files will always be randomized when run
    imgs=[]
    for path in image_path:
        for file in os.listdir(path):
            if file.endswith("jpg") or file.endswith("png") or file.endswith("jpeg") or file.endswith("gif"):
                imgs.append(os.path.join(path, file))

    dist_imgs = distribute(imgs, args.distribution)
    train_path = os.path.join(save_path, "train.txt")
    test_path = os.path.join(save_path, "test.txt")
    list2file(train_path, dist_imgs[0])
    list2file(test_path, dist_imgs[1])





    # Get object count
    oCount = 0
    with open(object_path) as file:
        for line in file:
            if line:
                oCount += 1

    # Generate the required detector file
    generate_detector(save_path, oCount, train_path, test_path, object_path, weights_path)




    # -- YOLO MODEL and WEIGHTS --

    # If no custom CFG is given, generate one
    yolocfg = args.custom_model
    if yolocfg is None:
        # Generate yolo file
        from tools import yolov4
        cfg = yolov4.yolov4(oCount, len(imgs), subdivisions=32)
        yolocfg = os.path.join(save_path, model_name+".cfg")
        with open(yolocfg, 'w') as file:
            file.write(cfg)
    else:
        yolocfg = os.path.abspath(yolocfg)

    # Runs a predefined weight if given, if not check and download standard weights.
    conv_file = args.weights
    if conv_file is None:
        if args.model == "YOLOv4":
            check4file(yolo_conv_files[args.model], "https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.conv.137")
            conv_file = os.path.join(cur_dir, "weights", yolo_conv_files[args.model])
    else:
        conv_file = os.path.abspath(conv_file)




    # -- RUN DARKNET --

    isTrain = True
    if args.test is not None:
        isTrain = args.test
    
    if isTrain:
        os.system(f"{darknet} detector train {os.path.join(save_path, 'detector.data')} {yolocfg} {conv_file} -gpus 0 -map > {os.path.join(save_path, 'train.log')}")\
    
    else:
        # TODO: search for multiple images or videos in a testing folder
        video_in = args.video_in
        if video_in is None:
            video_in = os.path.join(save_path, 'test.avi')
        else:
            video_in = os.path.abspath(video_in)

        video_out = args.video_out
        if video_out is None:
            video_out = os.path.join(save_path, 'res.avi')
        else:
            video_in = os.path.abspath(video_in)

        os.system(f"{darknet} detector demo {os.path.join(save_path, 'detector.data')} {yolocfg} {os.path.join(save_path, 'weights/', model_name+'_best.weights')} {video_in} -out_filename {video_out}")

    # NOTE: the TINY still needs a partial
    # check4file(yolo_conv_files[args.model], "https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.conv.29")