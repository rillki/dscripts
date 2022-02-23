import std.stdio;
import std.file;
import std.array;
import std.path;
import std.algorithm;

void main() {
    auto imgs = listdir(".").filter!(a => a.canFind(".png"));
    foreach(i; imgs) {
        auto path = i.split("/");
        auto newpath = path[0].buildPath(path[1], i.baseName);
        i.rename(newpath);

        writeln("DONE: ", newpath);
    }
}


string[] listdir(string pathname)
{
    import std.algorithm;
    import std.array;
    import std.file;
    import std.path;

    return std.file.dirEntries(pathname, SpanMode.depth)
        .filter!(a => a.isFile)
        .map!((return a) => a.name)
        .array;
}



