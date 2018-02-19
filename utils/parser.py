#!/usr/bin/python

from GoldRusher.utils.graphics import *
from GoldRusher.utils.misc import *

def parseCCOutput(output, functionStat, lineStat):
    """
    Parses the output of DynInst's CodeCoverage
    :param output: The output returned from CodeCoverage
    :type output: str
    :param functionStat: Counts of invocations of every function
    :type functionStat: dict
    :param lineStat: Counts about the executions of every line
    :type lineStat: dict
    :return: Two dicts of updated stats for the method invocations and line executions
    """
    # Retrieve the code coverage section
    codeCoverage, blockCoverage = [], []
    allLines = output.split("\n")
    idx = allLines.index(" ************************** Code Coverage ************************* ") + 1
    line = allLines[idx]
    while line.find("************** Code Coverage") == -1:
        codeCoverage.append(line)
        idx += 1
        line = allLines[idx]

    # Parse the functions
    functionStat = _parseCCFunctions(codeCoverage, functionStat)

    # Now retrieve the code lines
    bbIdx = allLines.index(" ************************** Basic Block Coverage ************************* ")
    for line in allLines[bbIdx:]:
        if line.find("************** Basic Block Coverage") == -1:
            blockCoverage.append(line)

    # Parse the basic blocks
    lineStat = _parseCCBlocks(blockCoverage, functionStat, lineStat)

    return functionStat, lineStat


def _parseCCFunctions(codeCoverage, functions):
    """
    Parses CodeCoverage's output to extract counts of method invocations
    :param codeCoverage: The output from code coverage summarizing method coverage
    :type codeCoverage: list
    :param functions: Counts of function invocations
    :type functions: dict
    :return: An updated dict of function invocations
    """
    for line in codeCoverage:
        data = line.split(" : ")
        if len(data) > 1 and line.find("__") == -1:
            if not data[1].startswith("_"):
                if data[1] in functions.keys():
                    functions[data[1]] += int(data[0])
                else:
                    functions[data[1]] = int(data[0])
    return functions

def _parseCCBlocks(blockCoverage, functions, lines):
    """
    Parses CodeCoverage's outut to extract counts of line executions
    :param blockCoverage: The output from code coverage summarizing line executions
    :type blockCoverage: list
    :param functions: Counts of function invocations
    :type functions: dict
    :param lines: Counts of line executions
    :type lines: dict
    :return: An updated dict of line executions
    """
    # Loop on function names and count their lines
    for f in functions:
        fIdx = blockCoverage.index(" (%s)" % (f)) + 1
        l = blockCoverage[fIdx] # Retrieve code lines
        while l.find("(") == -1 and l != '':
            # Clean up the \t and spaces
            l = l.replace("\t", "")
            l = l.replace(" ", "")
            lineAddr = l.split(":")[1]
            lineCount = int(l.split(":")[0])
            # Insert data into dictionary
            if not f in lines.keys():
                lines[f] = {}
            if lineAddr in lines[f].keys():
                lines[f][lineAddr] += lineCount
            else:
                lines[f][lineAddr] = lineCount
            fIdx += 1
            l = blockCoverage[fIdx] # Fetch next line

    return lines

def parseLtraceOutput(ltraceOutput, ltrace):
    """
    Parses the output retruned by "ltrace"
    :param ltraceOutput: The output of ltrace
    :type ltraceOutput: str
    :param ltrace: Counts of function invocations as reported by ltrace
    :type ltrace: dict
    :return: An updated dict of counts of function invocations
    """
    filteredOutput = ltraceOutput[ltraceOutput.find("----"):ltraceOutput.rfind("----")]
    allLines =  filteredOutput.split("\n") 
    data = allLines[1:-1]
    for line in data:
        if len(line) < 1 or line.find("----") != -1:
            continue
        functionData = line.split(" "*8)[-1]
        if len(functionData) > 0:
            # Retrieve function name and count from string
            if functionData[0] == " ":
                functionData = functionData[1:]
            if not functionData.isalpha() and functionData.isdigit():
                # Only numbers, skip
                continue
            idx = 0
            functionCount = functionData[idx]
            idx += 1
            while functionData[idx].isdigit():
                functionCount += functionData[idx]
                idx += 1
            functionName = functionData[idx:].replace(' ', '')
        # Insert them into dictionary    
        if functionName in ltrace.keys():
            ltrace[functionName] += int(functionCount)
        else:
            ltrace[functionName] = int(functionCount)

    return ltrace

def parseLtracePCOutput(ltraceOutput, ltracePC):
    """
    Parses the output of running "ltrace" on the target binary
    :param ltraceOutput: The output returned by "ltrace"
    :type ltraceOutput: str
    :param ltracePC: The functions encountered before in previous runs
    :type ltracePC: dict
    :return: 
    """
    allLines =  ltraceOutput.split("\n")[:-2] # Exclude the +++ exited line
    for line in allLines:
        if line.lower().find("[") == -1 and line.lower().find("[") == -1:
            continue
        callData = line.split(" ")
        lAddress = callData[1].replace("[","")
        lAddress = lAddress.replace("]", "")
        #braceIdx = callData[2].find("(")
        #if callData[2][braceIdx+1] == ")":
        #    braceIdx += 2
        #lName = callData[2][:braceIdx]
        lName = line[line.find("] ")+2:line.rfind(" =")]
        # Add library call to the dictionary
        if not lName.startswith("__") and not lName.startswith("_"):
            ltracePC[lAddress] = lName

    return ltracePC

def printCalls(data, total, orderby="value", threshold=5.0):
    """ 
    Pretty-prints the number of calls for functions
    :param data: The called methods/functions along with their number of invocations
    :type data: dict
    :param total: The total number of method invocations
    :type total: int
    :param orderby: Whether to order prints by the method names (key) or method invocations (value)
    :type orderby: str
    :param threshold: The percentage under which a method is deemed hidden
    :type threshold: float
    :return: A str of the output to be stored as a report
    """
    outString = ""
    if orderby == "value":
        for key, value in sorted(data.iteritems(), key=lambda (k,v): (v,k)):
            value, total, threshold = float(value), float(total), float(threshold)
            if len(key.split(", ")) > 1:
                fx, fl = key.split(", ")[0], key.split(", ")[1]
                coverage = str(value/total * 100.0) if value/total * 100.0 <= 100.0 else 100.0
                printLine = "\t > Function \"%s\" in file \"%s\" was called %s time(s) = %s%%" % (fx, fl, value, coverage)
            else:
                coverage = str(value/total * 100.0) if value/total * 100.0 <= 100.0 else 100.0
                printLine = "\t > Function \"%s\" was called %s time(s) = %s%%" % (key, value, coverage)
            if value == 0 or value/total <= (threshold/100.0):
                printLine += "\t"
                mode = "error"
            elif value/total < 0.5:
                mode = "warning"
            elif value/total > 1.0:
                mode = "info2"
            else:
                mode = "info"
            outString += "%s\n" % printLine
            prettyPrint(printLine, mode, False)
    elif orderby == "key":
        for key, value in sorted(data.iteritems(), key=lambda (k,v): (k,v)):
            value, total, threshold = float(value), float(total), float(threshold)
            coverage = str(value/total * 100.0) if value/total * 100.0 <= 100.0 else 100.0
            printLine = "\t %s: %s time(s) = %s%%" % (key, value, coverage) 
            if value == 0 or value/total <= (threshold/100.0):
                printLine += "\t"
                mode = "error"
            elif value/total < 0.5:
                mode = "warning"
            elif value/total > 1.0:
                mode = "info2"
            else:
                mode = "info"
            outString += "%s\n" % printLine
            prettyPrint(printLine, mode, False)

    return outString


def printLines(data, total, libraryCalls, orderby="value", threshold=5.0):
    """ 
    Pretty-prints the number of calls for blocks lines and the possible trigger conditions
    :param data: The executed lines  along with their number of executions
    :type data: dict
    :param total: The total number of line executions
    :type total: int
    :param libraryCalls: The calls made to system API which may be the triggers for hidden code
    :type libraryCalls: dict
    :param orderby: Whether to order prints by the method names (key) or method invocations (value)
    :type orderby: str
    :param threshold: The percentage under which a line is deemed hidden
    :type threshold: float
    :return: A str of the output to be stored as a report
    """ 
    outString = ""
    if orderby == "value": 
        for key, value in sorted(data.iteritems(), key=lambda (k,v): (v,k)): 
            value, total, threshold = float(value), float(total), float(threshold)
            coverage = str(value/total * 100.0) if value/total * 100.0 <= 100.0 else 100.0
            printLine = "\t %s: %s time(s) = %s%%" % (key, value, coverage) 
            if value == 0 or value/total <= (threshold/100.0): 
                printLine += "\t"
                mode = "error"
            elif value/total < 0.5:
                mode = "warning"
            elif value/total > 1.0:
                mode = "info2"
            else:
                mode = "info"
            for call in libraryCalls: 
                if key == call: 
                    printLine += "\t>> %s" % libraryCalls[call] 

            outString += "%s\n" % printLine
            prettyPrint(printLine, mode, False)
    elif orderby == "key": 
        for key, value in sorted(data.iteritems(), key=lambda (k,v): (k,v)): 
            value, total, threshold = float(value), float(total), float(threshold)
            coverage = str(value/total * 100.0) if value/total * 100.0 <= 100.0 else 100.0
            printLine = "\t %s: %s time(s) = %s%%" % (key, value, coverage) 
            if value == 0 or value/total <= (threshold/100.0): 
                printLine += "\t" 
                mode = "error"
            elif value/total < 0.5:
                mode = "warning"
            elif value/total > 1.0:
                mode = "info2"
            else:
                mode = "info"
            for call in libraryCalls: 
                if key == call: 
                    printLine += "\t>> %s" % libraryCalls[call] 
            outString += "%s\n" % printLine
            prettyPrint(printLine, mode, False)

    return outString
