module asol;

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


/**
 * UTILITY
 */

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


/**
 * PROCESS
 */

/++
 + Kill process by PID.
 + Params:
 +   pid = process pid
 + Returns: `true` if process was successfully killed.
 +/
bool killProcess(in int pid)
{
    import std.datetime.stopwatch : StopWatch, AutoStart;
    import std.datetime : msecs, seconds;
    auto timeout = 5.seconds;

    version (Windows)
    {
        import core.sys.windows.windows :
            OpenProcess, TerminateProcess, CloseHandle,
            WaitForSingleObject, PROCESS_TERMINATE, PROCESS_QUERY_INFORMATION,
            SYNCHRONIZE, INFINITE, WAIT_OBJECT_0;

        // create process handle
        enum PROCESS_ACCESS = PROCESS_TERMINATE | PROCESS_QUERY_INFORMATION | SYNCHRONIZE;
        auto handle = OpenProcess(PROCESS_ACCESS, false, cast(uint)pid);
        if (handle is null) return false;
        scope (exit) CloseHandle(handle);

        // try graceful termination (Windows doesn't support SIGTERM)
        if (!TerminateProcess(handle, 1)) return false;

        // wait for process to actually exit
        auto result = WaitForSingleObject(handle, cast(uint)timeout.total!"msecs");
        return result == WAIT_OBJECT_0;
    }
    else version (Posix)
    {
        import core.sys.posix.signal : kill, SIGTERM, SIGKILL;
        import core.sys.posix.sys.wait : waitpid, WNOHANG, WIFEXITED, WIFSIGNALED;

        // try graceful kill
        if (kill(pid, SIGTERM) != 0) 
        {
            return false;
        }

        // check for status
        int status = 0;
        waitpid(pid, &status, WNOHANG);
        if (WIFEXITED(status) || WIFSIGNALED(status)) 
        {
            return true;
        }

        return kill(pid, SIGKILL) != 0;
    }
    else
    {
        static assert(false, "Unsupported platform");
    }
}

/++
 + Check if process is running by PID.
 + Params:
 +   pid = process pid
 + Returns: `true` if process was successfully killed.
 +/
bool processIsRunning(in int pid)
{
    version(Posix)
    {
        import core.sys.posix.signal : kill;
        
        // send signal 0 (null signal) to test if process exists
        // this doesn't actually send a signal, just checks if we can
        int result = kill(pid, 0);
        return result == 0;
    }
    else version(Windows)
    {
        import core.sys.windows.windows : 
            OpenProcess, CloseHandle, GetExitCodeProcess, 
            PROCESS_QUERY_INFORMATION, STILL_ACTIVE;
        
        // try to open the process handle
        auto handle = OpenProcess(PROCESS_QUERY_INFORMATION, false, cast(uint)pid);
        if (handle is null)
        {
            return false; // process doesn't exist or no permission
        }
        scope(exit) CloseHandle(handle);
        
        // check if the process is still running
        uint exitCode;
        if (GetExitCodeProcess(handle, &exitCode))
        {
            return exitCode == STILL_ACTIVE;
        }
        
        return false; // failed to get exit code
    }
    else
    {
        static assert(false, "Unsupported platform");
    }
}

