#!/usr/bin/env python3
# bu22: writes tests/cases/touch.toml. A generator only so that the cases
# stay legible; the TOML it writes is what is committed.
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "bu21", "gen"))
from lib import Cases

c = Cases()
OLD = "1000000000.000000000"
F = {"scratch": {"f": "x\n"}, "scratch_times": {"f": OLD}, "times": True}
UTC = {"TZ": "UTC0"}
NY = "/usr/share/zoneinfo/America/New_York"

c.note("Usage.")
c.case("no operand", [])
c.case("-d with no argument", ["-d"])
c.case("-t with no argument", ["-t"])
c.case("-r with no argument", ["-r"])
c.case("an invalid option", ["-Q", "f"], **F)
c.case("--help", ["--help"], compare=["exit"])
c.case("--version", ["--version"], compare=["exit"])
c.case("-d and -t together", ["-d", "@1", "-t", "202001020304", "f"], **F)
c.case("-t and -d together", ["-t", "202001020304", "-d", "@1", "f"], **F)
c.case("-t and -r together", ["-t", "202001020304", "-r", "f", "f"], **F)
c.case("-f does nothing", ["-f", "-d", "@5", "f"], **F)

c.note("Now: an old file's times move to now; a new file is made.")
c.case("an existing file", ["f"], **F)
c.case("a new file", ["g"], **F)
c.case("a new file under the mask 077", ["g"], umask=0o077, **F)
c.case("a new file under the mask 777", ["g"], umask=0o777, **F)
c.case("two files, one new", ["f", "g"], **F)
c.case("-c on a new name", ["-c", "g"], **F)
c.case("-c on an existing file", ["-c", "f"], **F)
c.case("--no-create", ["--no-create", "g", "f"], **F)
c.case("-a", ["-a", "f"], **F)
c.case("-m", ["-m", "f"], **F)
c.case("-a -m", ["-a", "-m", "f"], **F)
c.case("a directory", ["d"], scratch_dirs=["d"], scratch_times={"d": OLD}, times=True)
c.case("a directory with a slash", ["d/"], scratch_dirs=["d"], scratch_times={"d": OLD}, times=True)
c.case("an unwritable file of one's own", ["f"], scratch={"f": "x\n"}, scratch_times={"f": OLD}, scratch_modes={"f": 0o444}, times=True)
c.case("--time=atime", ["--time=atime", "-d", "@2000000000", "f"], **F)
for w in ["access", "use", "mtime", "modify", "a", "m", "mo", "u"]:
    c.case(f"--time={w}", [f"--time={w}", "-d", "@2000000000", "f"], **F)
c.case("--time as two words", ["--time", "mtime", "-d", "@2000000000", "f"], **F)
c.case("--time=bogus", ["--time=bogus", "f"], **F)
c.case("--time= empty", ["--time=", "f"], **F)
c.case("--time=atime and -m", ["--time=atime", "-m", "-d", "@7", "f"], **F)

c.note("Failures: the making's reason, or the setting's.")
c.case("under a missing directory", ["x/y"], **F)
c.case("under a file", ["f/x"], **F)
c.case("a file with a slash", ["f/"], **F)
c.case("an empty name", [""], **F)
c.case("one fails, the rest are touched", ["x/y", "f", "g"], **F)
c.case("in a directory that may not be written", ["ro/g"], scratch_dirs=["ro"], scratch_modes={"ro": 0o555}, times=True)
c.case("standard output", ["-"], skip="GNU sets the times of whatever standard output is, through the descriptor; wolf sets times by name only (wolf-lang#714): refused by name, status 1")
c.case("standard output with a date", ["-d", "@1", "-"], skip="GNU sets the times of whatever standard output is, through the descriptor; wolf sets times by name only (wolf-lang#714): refused by name, status 1")

c.note("Links: followed, unless -h.")
L = {"scratch": {"f": "x\n"}, "scratch_links": {"l": "f", "dang": "nowhere", "deep": "sub/x"},
     "scratch_times": {"f": OLD, "l": "1100000000.000000000", "dang": "1100000000.000000000"}, "times": True}
c.case("a link to a file", ["-d", "@77", "l"], **L)
c.case("-h on a link to a file", ["-h", "-d", "@77", "l"], **L)
c.case("-h on a dangling link", ["-h", "-d", "@77", "dang"], **L)
c.case("a dangling link makes its target", ["-d", "@77", "dang"], **L)
c.case("-c on a dangling link", ["-c", "-d", "@77", "dang"], **L)
c.case("a link into a missing directory", ["deep"], **L)
c.case("-h on a missing name", ["-h", "-d", "@77", "nope"], **L)
c.case("-hc on a missing name", ["-hc", "nope"], **L)
c.case("-h now on a link", ["-h", "l"], **L)
c.case("-h -a on a link", ["-h", "-a", "-d", "@5", "l"], **L)

c.note("-r: each time from the reference.")
R = {"scratch": {"f": "x\n", "r": "y\n"}, "scratch_times": {"f": OLD, "r": "1234567890.123456789"},
     "scratch_atimes": {"r": "1111111111.987654321"}, "scratch_links": {"lr": "r"}, "times": True}
c.case("-r", ["-r", "r", "f"], **R)
c.case("--reference", ["--reference=r", "f"], **R)
c.case("-r a new file", ["-r", "r", "g"], **R)
c.case("-r -a", ["-a", "-r", "r", "f"], **R)
c.case("-r -m", ["-m", "-r", "r", "f"], **R)
c.case("-r a missing reference", ["-r", "nope", "f"], **R)
c.case("-r through a link", ["-r", "lr", "f"], **R)
c.case("-r -h reads the link itself", ["-h", "-r", "lr", "f"], scratch={"f": "x\n", "r": "y\n"},
       scratch_times={"f": OLD, "r": "1234567890.123456789", "lr": "1300000000.5"[:0] + "1300000000.500000000"},
       scratch_links={"lr": "r"}, times=True)
c.case("-r with -d", ["-r", "r", "-d", "@5", "f"], skip="-d with -r (a date relative to the reference's times) is not written: refused by name, status 1", **R)

c.note("-d: the forms read, in UTC.")
for d in ["@1500000000", "@1500000000.5", "@1500000000.123456789", "@1500000000,25", "@-1", "@-1.5", "@0",
          "@1.0000000001", "@+5", "2020-01-02", "2020-01-02 03:04", "2020-01-02 03:04:05", "2020-01-02T03:04:05",
          "2020-01-02t03:04:05", "2020-01-02 03:04:05.5", "2020-01-02 03:04:05,25", "2020-01-02 03:04:05Z",
          "2020-01-02 03:04:05 UTC", "2020-01-02 03:04:05 utc", "2020-01-02 03:04:05 GMT", "2020-01-02 03:04:05 +0200",
          "2020-01-02 03:04:05+02:00", "2020-01-02 03:04:05 -05", "2020-01-02T03:04:05.123456789Z",
          "2020-01-02T03:04:05.1234567891Z", " 2020-01-02 ", "1969-07-20 20:17:40", "1900-01-01", "2038-01-19 03:14:08",
          "2100-02-28 23:59:59", "2000-02-29", "03:04", "03:04:05", "23:59:59.999999999", "", "2020-01-02 03:04 Z"]:
    c.case(f"-d {d!r}", ["-d", d, "f"], env=UTC, **F)
for d in ["2020-13-01", "2020-02-30", "2019-02-29", "2020-00-10", "2020-01-00", "2020-01-02 25:00", "2020-01-02 03:60",
          "2020-01-02 03:04:61", "24:00:01"]:
    c.case(f"-d {d!r} is no date", ["-d", d, "f"], env=UTC, **F)
c.case("--date=", ["--date=2020-01-02", "f"], env=UTC, **F)
c.case("-d attached", ["-d@5", "f"], env=UTC, **F)
c.case("-d now", ["-d", "now", "f"], **F)
c.case("-d NOW", ["-d", "NOW", "f"], **F)
c.case("-d today", ["-d", "today", "f"], **F)
c.case("-d yesterday", ["-d", "yesterday", "f"], scratch={"f": "x\n"}, compare=["stdout", "stderr", "exit", "files"])
c.case("-d tomorrow", ["-d", "tomorrow", "f"], scratch={"f": "x\n"}, compare=["stdout", "stderr", "exit", "files"])
UNREAD = "GNU's date grammar takes this; boreutils reads part of it and refuses the rest by name, status 1, nothing touched"
for d in ["1 day ago", "next monday", "+1 day", "Jan 2 2020", "2 January 2020", "1/2/2020", "20200102", "noon", "2020-01-02 3pm"]:
    c.case(f"-d {d!r} is not read here", ["-d", d, "f"], env=UTC, skip=UNREAD, **F)
c.case("-d garbage", ["-d", "garbage", "f"], env=UTC, skip="GNU says 'invalid date format'; boreutils cannot tell a string GNU's grammar refuses from one it takes, so it refuses every string it does not read by name, in its own words", **F)

c.note("-d in a zone with daylight time (when the host has the zone file).")
NYE = {"TZ": "America/New_York"}
for d in ["2020-07-01 12:00", "2020-01-01 12:00", "2020-11-01 01:30", "2020-03-08 02:30", "2020-03-08 03:00",
          "2020-07-01 12:00 UTC", "1950-06-01 00:00"]:
    c.case(f"-d {d!r} in New York", ["-d", d, "f"], env=NYE, requires=NY, **F)
c.case("-d in a POSIX rule zone", ["-d", "2020-11-01 01:30", "f"], env={"TZ": "EST5EDT,M3.2.0,M11.1.0"}, **F)
c.case("-d in a fixed offset zone", ["-d", "2020-06-01 10:00", "f"], env={"TZ": "JST-9"}, **F)

c.note("-t [[CC]YY]MMDDhhmm[.ss], local time.")
for t in ["202001020304", "202001020304.05", "2001020304", "7001020304", "6901020304", "0001020304", "6801020304",
          "202001020304.60", "202001020304.59", "199912312359.59", "203801190314.07", "000001010000"]:
    c.case(f"-t {t}", ["-t", t, "f"], env=UTC, **F)
c.case("-t without a year", ["-t", "01020304", "f"], env=UTC, **F)
c.case("-t without a year, with seconds", ["-t", "01020304.59", "f"], env=UTC, **F)
for t in ["202001020304.61", "2020010203", "x", "202013020304", "202002300000", "202001022400", "202001020360",
          "20200102030", "202001020304.5", "202001020304.", ".05", "2020-01-02", "1202001020304"]:
    c.case(f"-t {t} is no date", ["-t", t, "f"], env=UTC, **F)
c.case("-t in New York", ["-t", "202007011200", "f"], env=NYE, requires=NY, **F)
c.case("-t in a skipped hour", ["-t", "202003080230", "f"], env=NYE, requires=NY, **F)
c.case("-t -a", ["-a", "-t", "202001020304", "f"], env=UTC, **F)
c.case("-t -m", ["-m", "-t", "202001020304", "f"], env=UTC, **F)
c.case("-t a new file", ["-t", "202001020304", "g"], env=UTC, **F)
c.case("-t -c a new name", ["-c", "-t", "202001020304", "g"], env=UTC, **F)

c.write(os.path.join(os.path.dirname(__file__), "..", "..", "..", "tests", "cases", "touch.toml"),
        "# touch — GNU coreutils 9.11, black-box, on linux x86-64 and macOS arm64.\n"
        "# Written by notes/bu22/gen/touch_cases.py; this file is the record.\n"
        "#\n"
        "# touch changes the file system, so every case runs in a scratch\n"
        "# directory (tools/difftest). A case that says `times = true` compares\n"
        "# every entry's access and modification time to the nanosecond, a\n"
        "# time inside the side's own run read as `now`; a fixture time is set\n"
        "# on every entry whose move to `now` the case is about.\n")
