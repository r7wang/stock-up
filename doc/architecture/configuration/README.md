## Design Considerations

### Static
Using static configuration is the default, and can be easily done by providing environment variables to containers
prior to running an application. Any configuration changes require an application restart to re-read the environment.

If the deployment is properly orchestrated, environment changes are typically delivered by committing changes to a
configuration file within the repository, then having continuous delivery perform an upgrade to the deployment version
without service impact. Depending on the build cycle, this might take up to an hour. If the deployment isn't properly
orchestrated, having to restart containers will lead to downtime.

We can summarize the negative impact as:
* potentially lengthy deployment cycle not conducive to rapid changes
* loss of service counter metrics  

To conclude, static configuration is likely not suitable for some use cases, such as fine-grained control of feature
flags, tunable logging, rapid feedback (traffic routing), and rapid recovery.

### Dynamic
The above uses cases can all be enabled with dynamic configuration and a watch-driven design where changes to
configuration notify the application and allow it to adjust its operations. This does, however, require some level of
development discipline because we have to be conscious of dynamic configuration and frequently asking for its current
value. This can be abstracted through the use of good client libraries.

There are several services that we can use to synchronize dynamic configuration, including:
* [Apache ZooKeeper](https://zookeeper.apache.org/)
* [etcd](https://etcd.io/)
