import std;

void main() {
	auto folder = "templabels";
	auto savefolder = folder.buildPath("save");
	auto files = folder.listdir;
	foreach(file; files) {
		File saveFile = File(savefolder.buildPath(file), "w");
		scope(exit) { saveFile.close(); }

		auto data = folder
					.buildPath(file)
					.readText
					.splitter("\n")
					.filter!(a => !a.empty)
					.map!(a => a.split)
					.array;

		foreach(line; data) {
			if(line[0] == "0") {
				line[0] = "1";
			} else if(line[0] == "1") {
				line[0] = "0";
			}

			line.writeln;
			saveFile.writeln(line.join(" "));
		}

		writeln("fixed: ", file);
	}
}

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
