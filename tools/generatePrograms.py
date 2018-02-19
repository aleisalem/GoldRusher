#!/usr/bin/python

from GoldRusher.utils.misc import *
from GoldRusher.utils.graphics import *
from GoldRusher.utils.parser import *
from GoldRusher.utils.db import *
from GoldRusher.conf.config import *

from datetime import datetime
import time, sys, os, subprocess, random, glob
import argparse

tigressCmds = {"virt": ["tigress", "--Transform=Virtualize", "--Functions=main", "--Transform=Virtualize", "--Functions=SECRET"], "jit": ["tigress", "--Transform=Jit", "--Functions=main", "--Transform=Jit", "--Functions=SECRET"], "flatten": ["tigress", "--Transform=Flatten", "--Functions=main", "--Transform=Flatten", "--Functions=SECRET"], "split": ["tigress", "--Transform=Split", "--Functions=main", "--Functions=SECRET"]}
tigressRandomCmds = {"password": ["tigress", "--Environment=x86_64:Linux:Gcc:4.6", "--Verbosity=1", "--Transform=RandomFuns", "--RandomFunsName=SECRET", "--RandomFunsType=long", "--RandomFunsInputSize=1", "--RandomFunsStateSize=1", "--RandomFunsOutputSize=1", "--RandomFunsCodeSize=10", "--RandomFunsPasswordCheckCount=1", "--RandomFunsFailureKind=message", "--RandomFunsPassword=%s"], "time": ["tigress", "--Environment=x86_64:Linux:Gcc:4.6", "--Verbosity=1", "--Transform=RandomFuns", "--RandomFunsName=SECRET", "--RandomFunsType=long", "--RandomFunsInputSize=1", "--RandomFunsStateSize=1", "--RandomFunsOutputSize=1", "--RandomFunsCodeSize=10", "--RandomFunsTimeCheckCount=1", "--RandomFunsFailureKind=message"], "activation": ["tigress", "--Environment=x86_64:Linux:Gcc:4.6", "--Verbosity=1", "--Transform=RandomFuns", "--RandomFunsName=SECRET", "--RandomFunsType=long", "--RandomFunsInputSize=1", "--RandomFunsStateSize=1", "--RandomFunsOutputSize=1", "--RandomFunsCodeSize=10", "--RandomFunsActivationCodeCheckCount=1", "--RandomFunsFailureKind=message"]}

def defineArguments():
    parser = argparse.ArgumentParser(prog="generatePrograms.py", description="Generates obfuscated and hidden code versions of programs.")
    parser.add_argument("-n", "--num", type=str, help="The number of random programs to generate.", required=True)
    parser.add_argument("-o", "--outdir", type=str, help="The directory to write generated programs to", required=False, default=".")
    parser.add_argument("-f", "--obfuscate", type=str, help="Whether to obfuscate generated programs", choices=["yes", "no"], required=False, default="no")
    return parser

    
def main():
    try:    
        # Check for required number of command-line arguments
        params_parser = defineArguments()
        arguments = params_parser.parse_args()

        generated = 0
        while generated < int(arguments.num):
            # 1. Random program name
            programName = getRandomAlphaNumeric()
            # 2. Random check
            #checkType = ["password", "activation", "time"][random.randint(0,2)]
            checkType = ["password", "time"][random.randint(0,1)]
            # 3. Random obfuscation
            obfuscationType = ["virt", "jit", "flatten", "split"][random.randint(0,3)]
            outFile = "%s/%s_%s_%s" % (arguments.outdir, programName, checkType, obfuscationType) if arguments.obfuscate == "yes" else "%s/%s_%s" % (arguments.outdir, programName, checkType)
            
            # 4. Run commands
            if arguments.obfuscate == "yes":
                prettyPrint("Generating a program of check type: \"%s\" and obfuscation \"%s\"" % (checkType, obfuscationType))
            else:
                prettyPrint("Generating a program of check type: \"%s\"" % checkType)
            # 4.a. Build command
            if checkType == "password":
                cmd = tigressRandomCmds["password"] + ["--RandomFunsPassword=%s" % getRandomAlphaNumeric()]
            elif checkType == "activation":
                cmd = tigressRandomCmds["activation"] + ["--RandomFunsActivationCode=%s" % getRandomNumber()]
            else:
                cmd = [] + tigressRandomCmds["time"]
            # 4.b. Generate program
            cmd += ["--out=%s.c" % outFile, "empty.c"]
            prettyPrint("Running command: %s" % " ".join(cmd), "debug")
            result = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE).communicate()[0]
            if result.lower().find("error") != -1:
                prettyPrint("Error encountered: %s" % result, "error")
                return False
            if arguments.obfuscate == "yes":
                # 4.c. Obfuscate program
                cmd = tigressCmds[obfuscationType] + ["--out=%s.c" % outFile, "%s.c" % outFile]
                prettyPrint("Running command: %s" % " ".join(cmd), "debug")
                result = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE).communicate()[0]
                if result.lower().find("error") != -1:
                    prettyPrint("Error encountered: %s" % result, "error")
                    return False
            if arguments.obfuscate == "no":
                # 5. Compile
                cmd = ["gcc", "%s.c" % outFile, "-o", "%s" % outFile]
                prettyPrint("Running command: %s" % " ".join(cmd), "debug")
                result = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE).communicate()[0]
                if result.lower().find("error") != -1:
                    prettyPrint("Error encountered: %s" % result, "error")
                    return False
           
            generated += 1
    
    except Exception as e:
        prettyPrintError("Error encountered: %s" % e)
        return False

    return True
    
if __name__ == "__main__":
    main()
