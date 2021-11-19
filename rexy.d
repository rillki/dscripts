#!/usr/bin/env rdmd
module rexy;

import std.stdio: writefln;
import std.array: empty;
import std.getopt: getopt, defaultGetoptPrinter;

import std.string: toStringz;
import core.stdc.stdlib: system;

void main(string[] args) {
	if(args.length < 2) {
		writefln("\n#rexy: no commands provided! See \'rexy -h\' for more info.\n");
		return;
	}

	// variables
	string 
		framerate = "24", 
		preset = "fast", 
		video = "", 
		output = "output.mkv";
	bool 
		audio = false,
		verbose = false;

	// parse command line arguments
	try {
		auto argInfo = getopt(
			args,
			"framerate|f", "video framerate", &framerate,
			"preset|p", "encoding process", &preset,
			"audio|a", "audio recording", &audio,
			"size|s", "video size", &video,
			"output|o", "output file name", &output,
			"verbose|v", "verbose output", &verbose
		);

		if(argInfo.helpWanted) {
			defaultGetoptPrinter("\nrexy version 1.0 - Screen Recorder Utility", argInfo.options);
			writefln("\nEXAMPLE: rexy --framerate=10 --size=640x480 --preset=ultrafast --audio --output=outputFile.mkv\n");
			return;
		}
	} catch(Exception e) { // catch unknown options
		writefln("\n#rexy: error! %s\n", e.msg);
		return;
	}

	// combine ffmpeg options
	string cmd = "ffmpeg -f avfoundation -i \"1:";

	// record audio
	cmd ~= ((audio) ? ("0\"") : ("\""));

	// framerate
	cmd ~= " -framerate " ~ framerate;

	// video size
	if(!video.empty) {
		cmd ~= " -s " ~ video;
	}

	// presets
	cmd ~= " -preset " ~ preset ~ " " ~ output;

	// verbose output
	if(verbose) {
		writefln("\n#rexy: RUNNING %s\n", cmd);
	}

	// run ffmpeg command
	system(cmd.toStringz);
}









