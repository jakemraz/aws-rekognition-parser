import aws_rekognition_parser as arp
import json

if __name__ == "__main__":


    with open('sample.json') as json_file:
        data = json.load(json_file)

    print('result:',arp.getNearestFaceByKdsRecord(data))

    pass

