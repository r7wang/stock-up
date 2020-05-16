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
before allowing other applications to start. If deployed using Kubernetes, can potentially use init containers to run
the custom script. Updates to the script require redeployment.

**Advantages**
* Script is easy to use during development.
 
**Disadvantages**
* Challenging to implement in Docker due to ordering of scripts. Requires the service to be started before running the
  script.
* Challenging to implement in Kubernetes because the the init container needs `rabbitmqctl` and `rabbitmqadmin` to be
  installed.

#### Application Declaration
This approach requires applications to perform exchange and queue declaration.

**Advantages**
* Trivial to define.

**Disadvantages**
* Application requires a user with configuration privileges. There may be ways to limit the scope of configuration
  privileges to mitigate this problem.
