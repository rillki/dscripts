module rk.core.asol;

/*
 * Asol - simple auxiliary lib for my D projects.
 *
 * The name Asol is a female name from the novel "Scarlet Sails" by Alexander Grin in 1922.
 * It symbolizes purity, dreams, and the hope for a better future.
 */

import std.file : dirEntries, SpanMode, DirEntry;
import std.path : baseName;
import std.array : array;
import std.stdio : write, writef;
import std.algorithm : map, filter, startsWith;

/++
 + Python-like print function
 +/
void logPrint(string sep = " ", string end = "\n", string header = null, Args...)(Args args)
{
    if (header) write(header);
    foreach (i, arg; args) write(arg, i + 1 < args.length ? sep: "");
    write(end);
}

/++
 + C printf-like log function
 +/
void logPrintf(string header = null, Args...)(in string format, Args args)
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