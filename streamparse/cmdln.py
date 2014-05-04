from docopt import docopt
from invoke import run

import json

from os import path

from bootstrap import quickstart


# XXX: these are commands we're working on still
TODO_CMDS = """
        sparse setup [-e ENV]
        sparse debug [-e ENV]
        sparse kill [-e ENV]
        sparse restart [-e ENV]
        sparse attach [-e ENV]
        sparse list [-e ENV]
        sparse logs [-e ENV]

"""


def main():
    """sparse: manage streamparse clusters.

    sparse provides a front-end to streamparse, a framework for creating Python
    projects for running, debugging, and submitting computation topologies against
    real-time streams, using Apache Storm.

    It requires the lein (Clojure build tool) to be on your $PATH, and uses
    lein and Clojure under the hood for JVM interop.

    Usage:
        sparse quickstart <proj_name>
        sparse run [-e ENV] [-t TIME]
        sparse deploy [-e ENV]
        sparse (-h | --help)
        sparse --version

    Options:
        -h --help         Show this screen.
        --version         Show version.
        -e ENV            Set environment; as described in config.json [default: local].
        -t TIME           Time (in milliseconds) to keep cluster running [default: 5000].
        --verbose         Verbose output.
        --debug           Debug output.
    """
    args = docopt(main.__doc__, version="sparse 0.1")
    if args["run"]:
        print "Running wordcount topology..."
        cfg = json.load(open("config.json"))
        topo_dir = cfg["topology_specs"]
        topo_first = cfg["topologies"][0] + ".clj"
        print path.join(topo_dir, topo_first)
        run("invoke stormlocal --topology={topology} --time={time}".format(
            topology=path.join(topo_dir, topo_first), time=args["-t"]))
    elif args["list"]:
        print "invoke (local) tasks:"
        run("invoke -l")
        print
        print "fabric (remote) tasks:"
        run("fab -l")
    elif args["quickstart"]:
        quickstart(args['<proj_name>'])


if __name__ == "__main__":
    main()