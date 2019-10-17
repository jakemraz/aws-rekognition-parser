from __future__ import print_function
import json

filename = 'sample.json'

class BoundBox:
    left = 0.0
    top = 0.0
    width = 0.0
    height = 0.0

class Face:
    externalImageId = ""

    def addBoundBox(self, boundBox):
        self.boundBox = boundBox
        pass

class RekognitionParcel:
    producerTimeStamp = 0.0
    faces = list()
    def __init__(self, *args, **kwargs):
        pass
    def addFace(self, face):
        self.faces.append(face)
        pass


def init():
    pass

def readFile(filename):
    f = open(filename, 'r')
    obj = f.readline()
    f.close()
    return obj

def parseRekognitionJson(obj):
    parcel = RekognitionParcel()
    
    inputInformation = obj['InputInformation']
    parcel.producerTimeStamp = inputInformation['KinesisVideo']['ProducerTimestamp']

    for response in obj['FaceSearchResponse']:
        face = Face()
        box = BoundBox()
        
        maxSimilarity = 0
        maxIndex = -1
        i = 0
        for matchedFace in response['MatchedFaces']:
            if matchedFace['Similarity'] > maxSimilarity:
                maxIndex = i
                maxSimilarity = matchedFace['Similarity']
            i += 1
        
        if maxIndex < 0:
            continue

        matchedFace = response['MatchedFaces'][maxIndex]
        face.externalImageId = matchedFace['Face']['ExternalImageId']

        detectedFace = response['DetectedFace']
        box.height = detectedFace['BoundingBox']['Height']
        box.width = detectedFace['BoundingBox']['Width']
        box.left = detectedFace['BoundingBox']['Left']
        box.top = detectedFace['BoundingBox']['Top']
        
        face.addBoundBox(box)

        

        parcel.addFace(face)

    return parcel


if __name__ == "__main__":

    init()   
    
    with open(filename) as json_file:
        data = json.load(json_file)
    

    # Do Nothing if FaceSearchResponse is None
    if data.get('FaceSearchResponse') is None:
        pass
    
    parcel = parseRekognitionJson(data)

    
    # print(type(parcel))
    # print(parcel.producerTimeStamp)
    
    for face in parcel.faces:
        print(face.externalImageId)



    pass

