## Design Considerations

### Exchange / Queue Declaration
There are multiple approaches worth considering.

#### Node Boot from Configuration
[This](https://www.rabbitmq.com/definitions.html) approach uses a configuration file and the `load_definitions`
instruction to declare all necessary resources on node boot.

**Advantages**
* Easy to persist all configuration.
* Ensures that service is ready to serve applications upon initialization.

**Disadvantages**
* Leaks user credentials through the configuration file.

#### Custom Scripting
This approach runs a custom script as part of the deployment process to ensure that the service is properly configured
before allowing other applications to start. If deployed using Kubernetes, can potentially use [init containers](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/)
to run the custom script. Updates to the script require redeployment.

**Advantages**
* Script is easy to use during development.
 
**Disadvantages**
* Challenging to implement in Docker due to ordering of scripts. Requires the service to be started before running the
  script.
* Challenging to implement in Kubernetes because the the init container needs `rabbitmqctl` and `rabbitmqadmin` to be
  installed.

#### Runtime Declaration
This approach requires applications to perform exchange and queue declaration.

**Advantages**
* Trivial to define.

**Disadvantages**
* Application requires a user with configuration privileges. There may be ways to limit the scope of configuration
  privileges to mitigate this problem.

### Exactly Once Delivery
Avoiding duplication and data loss is very important for data quality because duplication can result in volume and
weighted averages being calculated incorrectly. Some approaches are evaluated using the `pika` client library.

At least once delivery is supported using [publisher confirms](https://www.rabbitmq.com/confirms.html#publisher-confirms)
in conjunction wtih consumer acknowledgements. A code example can be seen [here](https://www.rabbitmq.com/tutorials/tutorial-seven-java.html).

There is no built-in support for at most once delivery; this needs to be implemented by the application.

#### Publisher Confirms: BlockingConnection
If using a `pika.BlockingConnection`, setting up publisher confirms only requires that the channel be put into confirm mode.
Everything else is managed by the client library and confirms occur on a per message basis. This is easy to implement
but has slower throughput as publishers have to wait for a confirm after every single message.

#### Publisher Confirms: SelectConnection
The `pika.SelectConnection` is an asynchronous connection type that works using continuation passing and requires a thread
to handle the event loop. It allows for asynchronous publisher confirms which result in much higher throughput but is
more complicated to implement. Unconfirmed messages have to be temporarily stored in a buffer with the full message
payload and an expected delivery tag. Messages that are nacked then have to be republished, which will cause messages
to arrive out of order. If the application restarts, all messages that were in the buffer would need to reloaded,
requiring them to be persisted to disk beforehand. For mission-critical systems that need to guarantee message
delivery, this approach requires very careful consideration to the different failure modes that can occur.
