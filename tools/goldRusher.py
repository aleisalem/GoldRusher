#!/usr/bin/python

from GoldRusher.utils.misc import *
from GoldRusher.utils.graphics import *
from GoldRusher.utils.parser import *
from GoldRusher.utils.db import *
from GoldRusher.conf.config import *

from datetime import datetime
import time, sys, os, subprocess
import pickledb, hashlib, json
import argparse
import random

def defineArguments():
    parser = argparse.ArgumentParser(prog="goldRusher.py", description="Extracts hidden code segments from binaries and identifies their trigger conditions.")
    parser.add_argument("-t", "--target", type=str, help="The binaries file to examine.", required=True)
    parser.add_argument("-c", "--codecoverage", type=str, help="The directory under which codeCoverage resides.", default=".", required=False)
    parser.add_argument("-x", "--hiddenthreshold", type=int, help="The percentage of coverage under which a method/line is considered hidden", default=5, required=False)
    parser.add_argument("-p", "--opt", action="append", help="The options to invoke the binary with, if applicable", required=False, default=[])
    parser.add_argument("-e", "--connector", help="The operator that connects options and actions (e.g., '=')", required=False, default=' ')
    parser.add_argument("-a", "--arg", action="append", help="The type/value of arguments to invoke the program with. Supported types are \"int\", \"float\", \"str\", \"char\", \"hash\", or \"none\"", required=False)
    parser.add_argument("-i", "--stdinput", help="Whether the program needs inputs via stdin", required=False, default="none")
    parser.add_argument("-n", "--numruns", type=int, help="The number of times random inputs is fed to the target program.", default=30, required=False)
    parser.add_argument("-o", "--outdir", help="The path to the output directory. Defaults to entry in config file. Files generated if logging is on", default="", required=False)
    return parser

    
def main():

    try:    
        # Check for required number of command-line arguments
        prettyPrint("Greetings and welcome to the \"GoldRusher\"")
        prettyPrint("Parsing arguments")
        params_parser = defineArguments()
        arguments = params_parser.parse_args()
        
        # Sanity checks and initializations
        if not os.path.exists(arguments.target):
            prettyPrint("Unable to locate the executable \"%s\". Exiting" % arguments.target, "error")
            return False

        # Retrieve the hash of the binary
        targetHash = hashlib.sha256(open(arguments.target).read()).hexdigest()
        targetBinary = arguments.target[arguments.target.rfind('/')+1:]
        # Open database
        goldDB = DB()
        # Insert information about the target binary
        goldDB.insert("Executables", ["exeID", "exeName", "exeRuns", "exeStartTimestamp"], [targetHash, targetBinary, arguments.numruns, str(time.time())]) 
        # Output directory
        outDir = GOLDRUSHER_OUT if arguments.outdir == "" else arguments.outdir
        if not os.path.exists("%s/%s_%s_out" % (outDir, targetBinary, targetHash)):
            os.mkdir("%s/%s_%s_out/" % (outDir, targetBinary, targetHash))
        outDir += "%s_%s_out/" % (targetBinary, targetHash)

        # Step 1 - Calling code coverage
        prettyPrint("Calling \"codeCoverage\"")
        prettyPrint("Make sure \"LD_LIBRARY_PATH\" and \"DYNINSTAPI_RT_LIB\" are set properly in the environment variables", "warning")
        # Attempt to run the program
        ccCmd = ["%s/codeCoverage" % arguments.codecoverage, "-bpa", arguments.target, "%s.inst" % arguments.target]
        if VERBOSE:
            prettyPrint("Command: %s" % " ".join(ccCmd), "debug", False)
        status = subprocess.Popen(ccCmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE).communicate()[0]
        if status.lower().find("rtlib.size()") != -1:
           prettyPrint("The variables \"LD_LIBRARY_PATH\" and \"DYNINSTAPI_RT_LIB\" are not properly configured. Exiting", "error")
           return False
        if status.lower().find("libinst.so") == -1:
            prettyPrint("Unable to invoke \"codeCoverage\"")

        # Step 2 - Run the newly-generated binary
        run = 0
        args, stdArgs = [], []
        functions, lines, ltrace, ltracePC = {}, {}, {}, {}
        binaryArgs = [ba.replace(' ', '') for ba in arguments.arg] if len(arguments.arg) > 0 else [] # Retrieve the number and types of program arguments
        binaryOpts = [bo.lstrip() for bo in arguments.opt] if len(arguments.opt) > 0 else []
        if len(binaryArgs) != len(binaryOpts):
             prettyPrint("The number of options (%s) and that of arguments (%s) are not equal" % (len(binaryOpts), len(binaryArgs)), "error")
             return False
        # Run the binary <numruns> number of times and record output
        while run < arguments.numruns:
            run += 1
            if len(binaryArgs) > 0 and len(binaryOpts) > 0:
                randomArgs = []
                for index in range(len(binaryArgs)):
                    bOpt = "" if binaryOpts[index] == "none" else binaryOpts[index]
                    connector = arguments.connector if binaryOpts[index] != "none" else ""
                    if binaryArgs[index] == "int":
                        randomArgs.append("%s%s%s" % (bOpt, connector, getRandomNumber()))
                    elif binaryArgs[index] == "float":
                        randomArgs.append("%s%s%s.%s" % (bOpt, connector, getRandomNumber(), getRandomNumber()))
                    elif binaryArgs[index] == "str":
                        randomArgs.append("%s%s%s" % (bOpt, connector, getRandomAlphaNumeric()))
                    elif binaryArgs[index] == "char":
                        randomArgs.append("%s%s%s" % (bOpt, connector, getRandomAlphaNumeric(length=1)))
                    elif str.isalnum(binaryArgs[index]):
                        # Probably a fixed value
                        randomArgs.append("%s%s%s" % (bOpt, connector, binaryArgs[index]))
                    elif binaryArgs[index] == "hash":
                        randomArgs.append("%s%s%s" % (bOpt, connector, getRandomHash("sha1")))
                    elif binaryArgs[index] == "none":
                        # An empty value
                        randomArgs.append(bOpt)    

                args.append(randomArgs) # Keep track of used inputs for later use
                
                # Call the binary
                prettyPrint("Calling the binary \"%s.inst\", run # %s" % (arguments.target, run))
                curDir = os.getcwd() # Save the current directory
                argsList = ["%s/%s.inst" % (curDir, arguments.target)] + randomArgs
                os.chdir(arguments.codecoverage)
                if VERBOSE:
                    prettyPrint("Command: %s" % " ".join(argsList), "debug", False)
                # Run the instrumented binary
                p = subprocess.Popen(argsList, stderr=subprocess.STDOUT, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                # Does the program need inputs during execution
                stdinput = arguments.stdinput
                if stdinput == "int":
                    x = getRandomNumber()
                    binaryOutput = p.communicate(input=b'%s\n' % x)[0]
                elif stdinput == "float":
                    x = "%s.%s" % (getRandomNumber() , getRandomNumber())
                    binaryOutput = p.communicate(input=b'%s\n' % x)[0]
                elif stdinput == "str":
                    x = getRandomAlphaNumeric()
                    binaryOutput = p.communicate(input=b'%s\n' % x)[0]
                elif stdinput == "char":
                    x = getRandomAlphaNumeric(length=1)
                    binaryOutput = p.communicate(input=b'%s\n' % x)[0]
                elif stdinput == "hash":
                    x = getRandomHash("sha1")
                    binaryOutput = p.communicate(input=b'%s\n' % x)[0]
                else:
                    x = "none"
                    binaryOutput = p.communicate()[0]
                # Add stdinput to be used with ltrace
                stdArgs.append(x)
              
                if binaryOutput.lower().find("code coverage") == -1:
                    prettyPrint("No output received from codeCoverage. Skipping", "warning")
                    os.chdir(curDir)
                    continue
                # Insert info about the testcase
                testCaseFile = open("%s/%s_testcase%s_%s.txt" % (outDir, targetBinary, run, str(int(time.time()))), "w")
                testCaseFile.write(binaryOutput)
                testCaseFile.close()
                goldDB.insert("Testcases", ["tcExecutable", "tcArgTypes", "tcArgValues", "tcCoverage"], [targetHash, ",".join(binaryArgs), ",".join(randomArgs), testCaseFile.name])
                prettyPrint("Parsing the output")
                functions, lines = parseCCOutput(binaryOutput, functions, lines)
                # Update app functions
                for f in functions.keys():
                    # Check whether function exists
                    fx, fl = (f.split(", ")[0], f.split(", ")[1]) if len(f.split(", ")) > 1 else (f, "")
                    results = goldDB.select([], "Functions", [("fName", fx), ("fExecutable", targetHash)])
                    if len(results.fetchall()) < 1:
                        goldDB.insert("Functions", ["fName", "fExecutable"], [fx, targetHash])
                os.chdir(curDir)

        # Step 3 - Call "ltrace" to find locations of libraries
        prettyPrint("Running \"ltrace\" with previous inputs")
        for index in range(len(args)):
            argsList = ["ltrace", "-itttC", "./%s" % arguments.target] + args[index]
            p = subprocess.Popen(argsList, stderr=subprocess.STDOUT, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            ltraceOutput = p.communicate(input=b'%s\n' % stdArgs[index])[0]
            if len(ltraceOutput) < 1:
                prettyPrint("ltrace did not generate any outputs", "warning")
            else:
                ltracePC = parseLtracePCOutput(ltraceOutput, ltracePC)
    
        # Step 4 - Retrieve least called functions/blocks and plot them
        reportString, reportFile = "", open("%s/report_%s_%sruns_%s.txt" % (outDir, targetBinary, arguments.numruns, str(int(time.time()))), "w")
        prettyPrint("Plotting results after %s runs" % run)
        reportString += "Plotting results after %s runs\n\n" % run
        prettyPrint("\tFunction Coverage\n\t-----------------\n", "output", False)
        reportString += "\tFunction Coverage\n\t-----------------\n"
        reportString += printCalls(functions, run, threshold=arguments.hiddenthreshold)
        prettyPrint("\n", "output", False)
        reportString += "\n\tLine Coverage\n\t-------------\n"
        prettyPrint("\tLine Coverage\n\t-------------\n", "output", False)
        for f in lines:
            if len(f.split(", ")) > 1:
                fx, fl = f.split(", ")[0], f.split(", ")[1]
                prettyPrint("\tFunction: \"%s\" in file \"%s\"\n" % (fx, fl), "output", False)               
                reportString += "\tFunction: \"%s\" in file \"%s\"\n" % (fx, fl)
            else:
                prettyPrint("\tFunction: \"%s\"\n" % f, "output", False)
                reportString += "\tFunction: \"%s\"\n" % f
            reportString += printLines(lines[f], run, ltracePC, orderby="key")
            prettyPrint("\n", "output", False)
            reportString += "\nRunning \"ltrace\" with previous inputs"

        if len(functions) < 1 and len(lines) < 1:
            prettyPrint("Nothing to display. Exiting", "error")
            return False
        
        # Step 5 - Call "ltrace" and rank library calls
        prettyPrint("Running \"ltrace\" with previous inputs")
        for index in range(len(args)):
            argsList = ["ltrace", "-cC", "./%s" % arguments.target] + args[index]
            if VERBOSE:
                prettyPrint("Command: %s" % " ".join(argsList), "debug", False)
                reportString += "Command: %s" % " ".join(argsList)
                p =  subprocess.Popen(argsList, stderr=subprocess.STDOUT, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                ltraceOutput = p.communicate(input=b'%s\n' % stdArgs[index])[0]
            if len(ltraceOutput) < 1:
                prettyPrint("ltrace did not generate any output", "warning")
            else:
                ltrace = parseLtraceOutput(ltraceOutput, ltrace)
        # Plot the frequency of library/system calls
        reportString += printCalls(ltrace, run, threshold=arguments.hiddenthreshold)
        # Update executable details to include end timestamp
        goldDB.update("Executables", [("exeEndTimestamp", str(time.time()))], [("exeID", targetHash)])

                       
        # Write final report to file and add to database
        if VERBOSE:
            prettyPrint("Writing final report to file", "debug")
        reportFile.write(reportString)
        reportFile.close()
        if VERBOSE:
            prettyPrint("Adding report info to database", "debug")
        goldDB.insert("Reports", ["rExecutable", "rTimestamp", "rPath"], [targetHash, getTimestamp(includeDate=True), reportFile.name])
        goldDB.close()

    except Exception as e:
        prettyPrintError("Error encountered: %s" % e)
        return 
    
if __name__ == "__main__":
    main()
