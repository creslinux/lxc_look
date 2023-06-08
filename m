lxc-start Foo 20230608125310.928 ERROR    network - ../src/lxc/network.c:lxc_create_network_unpriv_exec:2990 - lxc-user-nic failed to configure requested network: ../src/lxc/cmd/lxc_user_nic.c: 1206: main: Quota reached
lxc-start Foo 20230608125310.929 ERROR    start - ../src/lxc/start.c:lxc_spawn:1840 - Failed to create the network
lxc-start Foo 20230608125310.929 ERROR    lxccontainer - ../src/lxc/lxccontainer.c:wait_on_daemonized_start:878 - Received container state "ABORTING" instead of "RUNNING"
lxc-start Foo 20230608125310.929 ERROR    lxc_start - ../src/lxc/tools/lxc_start.c:lxc_start_main:307 - The container failed to start
lxc-start Foo 20230608125310.929 ERROR    lxc_start - ../src/lxc/tools/lxc_start.c:lxc_start_main:310 - To get more details, run the container in foreground mode
lxc-start Foo 20230608125310.929 ERROR    lxc_start - ../src/lxc/tools/lxc_start.c:lxc_start_main:312 - Additional information can be obtained by setting the --logfile and --logpriority options
lxc-start Foo 20230608125310.930 ERROR    start - ../src/lxc/start.c:__lxc_start:2107 - Failed to spawn container "Foo"
lxc-start Foobar 20230608130216.898 ERROR    lxccontainer - ../src/lxc/lxccontainer.c:do_lxcapi_start:913 - Failed checking for incomplete container creation
lxc-start Foobar 20230608130216.898 ERROR    lxc_start - ../src/lxc/tools/lxc_start.c:lxc_start_main:307 - The container failed to start
lxc-start Foobar 20230608130216.898 ERROR    lxc_start - ../src/lxc/tools/lxc_start.c:lxc_start_main:310 - To get more details, run the container in foreground mode
lxc-start Foobar 20230608130216.898 ERROR    lxc_start - ../src/lxc/tools/lxc_start.c:lxc_start_main:312 - Additional information can be obtained by setting the --logfile and --logpriority options
