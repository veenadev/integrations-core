# Agent Check: Supervisor
{{< img src="integrations/supervisor/supervisorevent.png" alt="Supervisor Event" responsive="true" popup="true">}}
## Overview

This check monitors the uptime, status, and number of processes running under supervisord.

## Setup
### Installation

The Supervisor check is packaged with the Agent, so simply [install the Agent](https://app.datadoghq.com/account/settings#agent) on any servers that use Supervisor to manage processes.  

If you need the newest version of the Supervisor check, install the `dd-check-supervisord` package; this package's check overrides the one packaged with the Agent. See the [integrations-core](https://github.com/DataDog/integrations-core#installing-the-integrations) repository for more details.

### Configuration
#### Prepare supervisord

The Agent can collect data from Supervisor via HTTP server or UNIX socket. The Agent collects the same data no matter which collection method you configure.
##### HTTP server

Add a block like this to supervisor's main configuration file (e.g. `/etc/supervisor.conf`):

```
[inet_http_server]
port=localhost:9001
username=user  # optional
password=pass  # optional
```

##### UNIX socket 

Add blocks like these to `/etc/supervisor.conf` (if they're not already there):

```
[supervisorctl]
serverurl=unix:///var/run//supervisor.sock

[unix_http_server]
file=/var/run/supervisor.sock
chmod=777
```

If supervisor is running as root, make sure `chmod` is set so that non-root users (i.e. dd-agent) can read the socket.

---

Reload supervisord.

#### Connect the Agent

Create a file `supervisord.yaml` in the Agent's `conf.d` directory. See the [sample supervisord.yaml](https://github.com/DataDog/integrations-core/blob/master/supervisord/conf.yaml.example) for all available configuration options:

```
init_config:

instances:
  - name: supervisord0 # used to tag service checks and metrics, i.e. supervisor_server:supervisord0
    host: localhost  
    port: 9001

# To collect from the socket instead
# - name: supervisord0
#   host: http://127.0.0.1 
#   socket: unix:///var/run//supervisor.sock
```

Use the `proc_names` and/or `proc_regex` options to list processes you want the Agent to collect metrics on and create service checks for. If you don't provide either option, the Agent tracks _all_ child processes of supervisord. If you provide both options, the Agent tracks processes from both lists (i.e. the two options are not mutually exclusive).

Configuration Options

* `name` (Required) - An arbitrary name to identify the supervisord server.
* `host` (Optional) - Defaults to localhost. The host where supervisord server is running.
* `port` (Optional) - Defaults to 9001. The port number.
* `user` (Optional) - Username
* `pass` (Optional) - Password
* `proc_names` (Optional) - Dictionary of process names to monitor
* `server_check` (Optional) - Defaults to true. Service check for connection to supervisord server.
* `socket` (Optional) - If using supervisorctl to communicate with supervisor, a socket is needed.

See the [example check configuration](https://github.com/DataDog/integrations-core/blob/master/supervisord/conf.yaml.example) for comprehensive descriptions of other check options.

[Restart the Agent](https://docs.datadoghq.com/agent/faq/start-stop-restart-the-datadog-agent) to start sending Supervisor metrics to Datadog.

### Validation

[Run the Agent's `info` subcommand](https://docs.datadoghq.com/agent/faq/agent-status-and-information/) and look for `supervisord` under the Checks section:

```
  Checks
  ======
    [...]

    supervisord
    -------
      - instance #0 [OK]
      - Collected 26 metrics, 0 events & 4 service check

    [...]
```

## Compatibility

The supervisord check is compatible with all major platforms.

## Data Collected
### Metrics

See [metadata.csv](https://github.com/DataDog/integrations-core/blob/master/supervisord/metadata.csv) for a list of metrics provided by this check.

### Events
The Supervisord check does not include any event at this time.

### Service Checks

**supervisord.can_connect**:

Returns CRITICAL if the Agent cannot connect to the HTTP server or UNIX socket you configured, otherwise OK.

**supervisord.process.status**:

The Agent submits this service check for all child processes of supervisord (if neither `proc_names` nor `proc_regex` is configured) OR a set of child processes (those configured in `proc_names` and/or `proc_regex`), tagging each service check with `supervisord_process:<process_name>`.

This table shows the `supervisord.process.status` that results from each supervisord status:

|supervisord status|supervisord.process.status|
|---|---|
|STOPPED|CRITICAL|
|STARTING|UNKNOWN|
|RUNNING|OK|
|BACKOFF|CRITICAL|
|STOPPING|CRITICAL|
|EXITED|CRITICAL|
|FATAL|CRITICAL|
|UNKNOWN|UNKNOWN|

## Troubleshooting
Need help? Contact [Datadog Support](http://docs.datadoghq.com/help/).

## Further Reading

* [Supervisor monitors your processes. Datadog monitors Supervisor.](https://www.datadoghq.com/blog/supervisor-monitors-your-processes-datadog-monitors-supervisor/)
