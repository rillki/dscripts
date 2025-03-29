module assol;

/*
 * Assol - simple auxiliary lib for my D projects.
 *
 * The name Assol is a female name from the novel "Scarlet Sails" by Alexander Grin in 1922.
 * It symbolizes purity, dreams, and the hope for a better future.
 */

import std.file : dirEntries, SpanMode, DirEntry;
import std.path : baseName;
import std.array : array;
import std.stdio : write, writef;
import std.algorithm : map, filter, startsWith;


/++
 + Python-like print function
 + Params:
 +   args = arguments
 +/
void logPrint(string sep = " ", string end = "\n", string header = "", Args...)(Args args)
{
    write(header);
    foreach (i, arg; args) write(arg, i < args.length ? sep: "");
    write(end);
}

/++
 + C printf-like log function
 + Params:
 +   format = formatted output
 +   args = arguments
 +/
void logPrintf(string header = "", Args...)(in string format, Args args)
{
    if (header) write(header);
    writef(format, args);
}

/++
 + List all files found in a directory
 + Params:
 +   dir = directory to inspect
 +   ignoreDotFiles = exclude dot files
 +   mode = inspection span mode
 + Returns: an array of file names with absolute path
 +/
string[] listdir(in string dir, in bool ignoreDotFiles = false, in SpanMode mode = SpanMode.depth)
{
    return ignoreDotFiles
        ? dirEntries(dir, mode).filter!(a => !baseName(a.name).startsWith(".")).map!(a => a.name).array
        : dirEntries(dir, mode).map!(a => a.name).array;
}
