import lxc
import sys

# Setup the container object
c = lxc.Container("apicontainer")
if c.defined:
    print("Container already exists", file=sys.stderr)
    sys.exit(1)

# Create the container rootfs
if not c.create("download", lxc.LXC_CREATE_QUIET, {"dist": "ubuntu",
                                                   "release": "lunar",
                                                   "arch": "amd64"}):
    print("Failed to create the container rootfs", file=sys.stderr)
    sys.exit(1)

# Start the container
if not c.start():
    print("Failed to start the container", file=sys.stderr)
    sys.exit(1)

# Query some information
print("Container state: %s" % c.state)
print("Container PID: %s" % c.init_pid)

# # Stop the container
# if not c.shutdown(30):
#     print("Failed to cleanly shutdown the container, forcing.")
#     if not c.stop():
#         print("Failed to kill the container", file=sys.stderr)
#         sys.exit(1)

# # Destroy the container
# if not c.destroy():
#     print("Failed to destroy the container.", file=sys.stderr)
#     sys.exit(1)