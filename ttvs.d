#!/usr/bin/env rdmd
module ttvs;

import std.stdio: writefln;
import std.array: empty;
import std.path: buildPath;
import std.file: getcwd, exists, mkdirRecurse, copy;
import std.getopt: getopt, defaultGetoptPrinter;
import std.random: uniform;
import std.algorithm: remove;
import std.parallelism: parallel;

void main(string[] args) {
    string path = "";
    size_t test = 20;
    size_t val = 20;
    bool verbose = false;
    
    // get arg options
    auto argInfo = getopt(
        args,
        "path|p", "path to data", &path,
        "test", "test percentage ratio", &test,
        "val", "validation percentage ratio", &val,
        "verbose|v", "verbose output (true by default)", &verbose,
    );
    
    // print help if needed
    if(argInfo.helpWanted) {
        defaultGetoptPrinter("\nttvs version 1.0 - train, test, validation data splitter", argInfo.options);
        writefln("\nEXAMPLE: ttsv --path=data/folder --test=20 --val=10 --verbose\n");
        return;
    }
    
    trainTestValSplit(path, test, val, verbose);
}

void trainTestValSplit(const string path, size_t test, size_t val, const bool verbose) {
    // check if path exists
    if(!path.exists) {
        writefln("\n#ttvs: <%s> does not exist!\n", path);
        return;
    }

    // get all train files
    string[] trainFiles = path.listdir;
    if(trainFiles.empty) {
        writefln("\n#ttvs: no files found in <%s>\n", path);
        return;
    }

    if(verbose) { writefln("\n#ttsv: splitting..."); }
    
    // update values to number of files
    test = trainFiles.length * test / 100;
    val = trainFiles.length * val / 100;

    // get all test files
    string[] testFiles = new string[test];
    foreach(i; 0..test) {
        // get random element
        auto element = uniform(0, trainFiles.length);
        
        // add element to testFiles
        testFiles[i] = trainFiles[element];
        
        // update trainFiles
        trainFiles = trainFiles.remove(element);
    }

    // get all val files
    string[] valFiles = new string[val];
    foreach(i; 0..val) {
        // get random element
        auto element = uniform(0, trainFiles.length);
        
        // add element to testFiles
        valFiles[i] = trainFiles[element];
        
        // update trainFiles
        trainFiles = trainFiles.remove(element);
    }

    // create output directories
    string trainPath = path.buildPath("ttsv").buildPath("train");
    string testPath = path.buildPath("ttsv").buildPath("test");
    string valPath = path.buildPath("ttsv").buildPath("val");
    mkdirRecurse(trainPath);
    mkdirRecurse(testPath);
    mkdirRecurse(valPath);
    
    // copy train files to train directory
    foreach(file; trainFiles.parallel) {
        path.buildPath(file).copy(trainPath.buildPath(file));
    }

    if(verbose) { writefln("#ttsv: <%s> train files added.", trainFiles.length); }

    // copy test files to test directory
    foreach(file; testFiles.parallel) {
        path.buildPath(file).copy(testPath.buildPath(file));
    }

    if(verbose) { writefln("#ttsv: <%s> test files added.", testFiles.length); }

    // copy val files to validation directory
    foreach(file; valFiles.parallel) {
        path.buildPath(file).copy(valPath.buildPath(file));
    }

    if(verbose) { writefln("#ttsv: <%s> val files added.\n#ttsv: done.\n", valFiles.length); }
}

/++ 
Lists files in a specified directory

Params:
    dir = path to files

Returns: string[]
+/
string[] listdir(const string dir) {
    import std.file: dirEntries, SpanMode, isFile;
    import std.path: baseName;
    import std.algorithm: filter, map;
    import std.array: array;

    return dirEntries(dir, SpanMode.shallow)
        .filter!(a => a.isFile)
        .map!(a => baseName(a.name))
        .filter!(a => a[0] != '.')
        .array;
}
 













