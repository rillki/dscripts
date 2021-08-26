#!/usr/bin/env rdmd

import std;

void main(string[] args) {
	if(args.length < 2 || args.canFind("-h")) {
		("\n=====================================================\n" ~
			"incrn  v1.0 -- INCremental file ReNaming.\n" ~
			"-----------------------------------------------------\n" ~
			"USAGE:\n\tincrn.d [path] (prefix) (# of files)\n" ~
			"OPTIONS:\n\t[]\trequired\n\t()\toptional, specify \'-\' to use defaults\n" ~
			"\t-h\tdisplay available options and exit\n" ~
			"\t-v\tverbose output\n" ~
			"DEFAULTS:\n\t(prefix)\t0, 1, ..., N\n\t(# of files)\tall files in a directory\n" ~
			"EXAMPLE:\n\tgoal\t rename 50 files in testdir\n\tcommand\t ./incrn ../testdir - 50\n\n" ~
			"\toutput\t 0.file_extension\n\t\t 1.file_extension\n\t\t ...\n\t\t N.file_extension\n" ~
			"=====================================================\n"
		).writeln;
		return;
	}

	// get directory path
	immutable dir = args[1].absolutePath;
	if(!dir.exists && !dir.isDir) {
		writefln("\n#incrn: directory <%s> does not exist!\n", dir);
		return;
	}

	// list files in dir (remove files that start with '.' e.g. hidden files)
	auto list = dir.listdir.filter!(a => a[0] != '.').array;
	if(list is null) {
		writefln("\n#incrn: directory <%s> is empty!\n", dir);
		return;
	}

	// get prefix
	immutable prefix = ((args.length > 2 && args[2][0] != '-') ? (args[2] ~ "_") : "");
	if(prefix.isNumeric) {
		writefln("\n#incrn: prefix <%s> cannot be numeric (do _%s_ instead)!\n", prefix, prefix);
		return;
	}

	// create a incrn_renamed directory
	immutable rndir = dir.buildPath("incrn_renamed");
	if(!rndir.exists) {
		rndir.mkdirRecurse;
	}

	// count files
	immutable n = (
		(args.length > 3 && args[3].isNumeric) ? 
			((args[3].to!int <= list.length) ? args[3].to!int : 0) : 
			list.length
	);

	// verbose output
	immutable verbose = args.canFind("-v");

	// print status
	if(verbose) {
		"\n#incrn: path\t= %s".writefln(dir);
		"#incrn: prefix\t= %s".writefln(prefix);
		"#incrn: files\t= %s\n".writefln(n);

		"#incrn: RENAMING|\n----------------|".writeln;
	}


	//rename files and save them to rndir
	foreach(i, file; list[0..n]) {
		// retrieve extension, oldName, newName
		immutable extension = (file.canFind(".") ? ("." ~ file.split(".")[$-1]) : "");
		immutable oldName = dir.buildPath(file);
		immutable newName = rndir.buildPath(prefix ~ i.to!string ~ extension);

		if(verbose) {
			"#incrn: %s: %s >> %s".writefln(i, file, prefix ~ i.to!string ~ extension);
		}

		oldName.copy(newName);
	}

	writefln("\n#incrn: %s files have been renamed!", n);
	writefln("#incrn: saved to %s\n", rndir);
}

string[] listdir(string dir) {
    return dirEntries(dir, SpanMode.shallow)
        .filter!(a => a.isFile)
        .map!(a => baseName(a.name))
        .array;
}





















