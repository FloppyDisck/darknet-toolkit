from xml.dom import minidom
import os

def convert_to_yolo(dirs, deleteOld=True):
    xmls = []
    # Get all files in question
    for dir in dirs:
        for file in os.listdir(dir):
            if file.endswith("xml"):
                xmls.append(os.path.join(dir, file))
    
    # Process all files
    #TODO: support for more than one name
    for xml in xmls:
        xmldoc = minidom.parse(xml)
        name = xmldoc.getElementsByTagName('filename')[0].childNodes[0].data.split('.')[0]
        width = int(xmldoc.getElementsByTagName('width')[0].childNodes[0].data.split('.')[0])
        height = int(xmldoc.getElementsByTagName('height')[0].childNodes[0].data.split('.')[0])
        xmin = [int(tag.childNodes[0].data) for tag in xmldoc.getElementsByTagName('xmin')]
        ymin = [int(tag.childNodes[0].data) for tag in xmldoc.getElementsByTagName('ymin')]
        xmax = [int(tag.childNodes[0].data) for tag in xmldoc.getElementsByTagName('xmax')]
        ymax = [int(tag.childNodes[0].data) for tag in xmldoc.getElementsByTagName('ymax')]

        with open(os.path.join(dirs[0], name+".txt"), 'w') as f:
            for i in range(len(xmin)):
                xlen = xmax[i] - xmin[i]
                ylen = ymax[i] - ymin[i]
                f.write(f"{0} {(xlen + xmin[i])/width} {(ylen + ymin[i])/height} {xlen/width} {ylen/height}\n")
        
        if deleteOld:
            os.remove(xml)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Turns XML files into YOLO accepted files.')

    parser.add_argument('-p', '--paths', nargs='+', type=str,
                        help="Folder or multiple folders containing xmls.")

    args = parser.parse_args()

    convert_to_yolo(args.paths)