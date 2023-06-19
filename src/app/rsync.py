# Note: This file does not implement the full rsync algorithm. I stopped working on it as I think it's overkill for my needs. Keeping the work here in case I change my mind in the future.


# Import general packages
from __future__ import absolute_import
import numpy

# Import project files
import comms.file

class Rsync():
    def __init__(self):
        self.rootPath = ""
        self.allFiles = []

    def getRootPath(self):
        return self.rootPath

    def setRootPath(self, path):
        self.rootPath = path
        self.allFiles = []

    def areFilesPresent(self):
        return len(self.allFiles) > 0

    def discoverFiles(self):
        print("Rsync Manager " + str(self.rootPath) + "Collecting files")
        rawFiles = comms.file.getFilesInDirectory(self.rootPath)
        for file in rawFiles:
            self.allFiles.append(RsyncFile(file))
            print(file)

    def loadFilesIntoMemory(self):
        for file in self.allFiles:
            file.loadFile()

    def prepareAllFiles(self):
        for file in self.allFiles:
            file.calculateBlocks()
            file.calculateFixedChecksum()


class RsyncFile():
    def __init__(self, path):
        self.absolutePath = path
        self.rawBytes = bytes
        self.fileBlocks = []
        self.rollingChecksums = []
        self.strongChecksums = []

        # Settings
        self.bytesPerBlock = 1000
        self.modulusValue = 2^16

    def loadFile(self):
        raw_bytes = comms.file.extractRawData(self.absolutePath)
        if raw_bytes is not None:
            self.raw_bytes = raw_bytes

    def calculateBlocks(self):
        print("Calculating blocks for file " + self.absolutePath)
        for blockIdx in range(0, len(self.raw_bytes), self.bytesPerBlock):
            block = self.raw_bytes[blockIdx: blockIdx + self.bytesPerBlock]
            self.fileBlocks.append(block)

    def calculateFixedChecksum(self):
        print("Calculating rolling checksums for file " + self.absolutePath)
        for blockIdx in range(0, len(self.raw_bytes), self.bytesPerBlock):
            byteVector = numpy.frombuffer(self.fileBlocks[blockIdx], dtype=numpy.uint8)

            alpha = numpy.sum(byteVector) % self.modulusValue

            beta = self.rollingChecksumBeta(byteVector)

            self.rollingChecksums.append(alpha + (beta % self.modulusValue))

    def rollingChecksumBeta(self, byteVector):
        # Helper function
        runningResult = 0
        for byteIdx in range(len(byteVector)):
            runningResult += (self.bytesPerBlock - byteIdx +1) * byteVector[byteIdx]
        return runningResult * self.modulusValue
