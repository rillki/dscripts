#!/usr/bin/env rdmd
module incrn;

import std.stdio: writefln;
import std.conv: to;
import std.file: mkdirRecurse, exists, copy;
import std.path: buildPath;
import std.array: empty;
import std.string: split;
import std.getopt: getopt, GetoptResult, defaultGetoptPrinter;
import std.algorithm: canFind;

void main(string[] args) {
	string path = "";
	string prefix = "";
	size_t startFromNum = 0;
	bool verbose = false;

	if(args.length < 2) {
		writefln("\n#incrn: no commands provided! See \'incrn -h\' for more info.\n");
		return;
	}

	// get arg options
	GetoptResult argInfo;
	try {
		argInfo = getopt(
			args, 
			"path|p", "path to files", &path, 
			"prefix|x", "prefix to be added to file name", &prefix,
			"startFrom", "start from index/number, which is appended to prefix", &startFromNum,
			"verbose|v", "verbose output", &verbose
		);
	} catch(Exception e) {
		writefln("\n#incrn: error! %s\n", e.msg);
		return;
	}

	// print help if needed
	if(argInfo.helpWanted) {
		defaultGetoptPrinter("\nincrn version 1.0 - INCremental file ReNaming", argInfo.options);
		writefln("\nEXAMPLE: incrn --path=data/filder --prefix=projectName --startFrom=121\n");
		return;
	}

	// find all files
	auto files = path.listdir;
	if(files.empty) {
		writefln("\n#incrn: directory <%s> is empty!\n", path);
		return;
	} else {
		startFromNum = ((startFromNum == 0) ? (files.length) : (startFromNum));
	}

	// create a incrn directory
	immutable rndir = path.buildPath("incrn");
	if(!rndir.exists) {
		rndir.mkdirRecurse;
	}

	if(verbose) { writefln("\n#incrn: renaming..."); }


	//rename files and save them to rndir
	foreach(i, file; files) {
		// retrieve extension, oldName, newName
		immutable index = (i + startFromNum).to!string;
		immutable extension = (file.canFind(".") ? ("." ~ file.split(".")[$-1]) : "");
		immutable oldName = path.buildPath(file);
		immutable newName = rndir.buildPath(prefix ~ index ~ extension);

		if(verbose) {
			"#incrn: %s: %s => %s".writefln(i, file, prefix ~ index ~ extension);
		}

		oldName.copy(newName);
	}

	if(verbose) {
		writefln("#incrn: %s files were renamed!", files.length);
		writefln("#incrn: saved to <%s>", rndir);
		writefln("#incrn: done.\n");
	}
}

/++ 
filess files in a specified directory

Params:
	path = path to files

Returns: string[]
+/
string[] listdir(const string path) {
	import std.file: dirEntries, SpanMode, isFile;
	import std.path: baseName;
	import std.algorithm: filter, map;
	import std.array: array;

	return dirEntries(path, SpanMode.shallow)
		.filter!(a => a.isFile)
		.map!(a => baseName(a.name))
		.filter!(a => a[0] != '.')
		.array;
}





















