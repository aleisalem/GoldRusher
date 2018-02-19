CREATE TABLE Executables( 
    exeID		        TEXT, 
    exeName 	   	    TEXT,
    exeRuns		        INTEGER,
    exeStartTimestamp	TEXT,
    exeEndTimestamp     TEXT
);

CREATE TABLE Functions( 
    fName       	TEXT, 
    fExecutable	  	TEXT,
    PRIMARY KEY (fName, fExecutable)
    FOREIGN KEY (fExecutable) REFERENCES parent(exeID)
);

CREATE TABLE Reports( 
    rID		       	INTEGER PRIMARY KEY AUTOINCREMENT, 
    rExecutable 	TEXT, 
    rTimestamp 		TEXT,
    rPath  		TEXT,
    FOREIGN KEY (rExecutable) REFERENCES parent(exeID)
);

CREATE TABLE Testcases( 
    tcID        	INTEGER PRIMARY KEY AUTOINCREMENT, 
    tcExecutable	TEXT,
    tcArgTypes		TEXT,
    tcArgValues		TEXT,
    tcCoverage 		TEXT,
    FOREIGN KEY (tcExecutable) REFERENCES parent(exeID)
);
