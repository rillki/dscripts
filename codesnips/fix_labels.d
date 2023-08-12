import std;

void main(string[] args) 
{
    if (args.length < 3)
    {
        writeln("USAGE: ./fix_labels.d [INPUT] [OUTPUT]");
        return;
    }

	auto folder = args[1];
	auto savefolder = args[2];
    if (!savefolder.exists) 
    {
        savefolder.mkdirRecurse;
    }

	auto files = folder.listdir;
    if (files.empty)
    {
        writeln("No files found!");
        return;
    }

	foreach (file; files) 
    {
        auto data = folder
            .buildPath(file)
            .readText
            .splitter("\n")
            .filter!(a => !a.empty)
            .map!(a => a.split)
            .array;
    	
        File saveFile = File(savefolder.buildPath(file), "w");
		scope(exit) { saveFile.close(); }

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

string[] listdir(string dir) 
{
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


