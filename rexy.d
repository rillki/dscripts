module rexy;

import std.stdio: writefln;
import std.getopt: getopt, defaultGetoptPrinter;

void main(string[] args) {
    bool start = false;
	int framerate = 24;
	
	// get arg options
	auto argInfo = getopt(
		args,
		"start|s", "start recording", &start,
		"framerate|f", "video framerate", &framerate
	);
	
	// print help if needed
	if(argInfo.helpWanted) {
		defaultGetoptPrinter("\nrexy version 1.0 - simple screen recorder with few arguments", argInfo.options);
		writefln("\nEXAMPLE: rexy --start --framerate=10\n");
		return;
	}
}