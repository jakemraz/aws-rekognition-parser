from __future__ import print_function
import json

filename = 'sample.json'

class BoundBox:
    left = 0.0
    top = 0.0
    width = 0.0
    height = 0.0
    def toJson(self):
        return json.dumps(self.__dict__)

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

def getNearestFace(parcel):
    maxArea = 0
    maxIndex = -1
    i = 0
    for face in parcel.faces:
        area = face.boundBox.width * face.boundBox.height
        print('name:',face.externalImageId,' area:',area)
        if area > maxArea:
            maxArea = area
            maxIndex = i
        
    if maxIndex == -1:
        print('face not matched')
        return

    # found person
    face = parcel.faces[maxIndex]    
    print('result:', face.externalImageId)
    return face

def getNearestInformation(jsonObj):

    # Do Nothing if FaceSearchResponse is None
    if jsonObj.get('FaceSearchResponse') is None:
        return
    
    # Parse Rekognition Json Object
    parcel = parseRekognitionJson(jsonObj)

    # Get Event Timestamp
    timestamp = parcel.producerTimeStamp

    # Get Nearest Face Information (Who, Where)
    face = getNearestFace(parcel)
    print('timestamp:', timestamp,',name:', face.externalImageId, ',box:', face.boundBox.toJson())  

    return {
        'timestamp':timestamp,
        'name':face.externalImageId
    }

