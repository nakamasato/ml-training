# Cluster


https://docs.ray.io/en/master/cluster/quickstart.html#ref-cluster-quick-start

## AWS

1. prerequisite
    - [ ] `aws configure` (aws profile cannot be specified?)
    - [ ] IAM policy to create IAM/EC2...
    - [ ] VPC and subnets (You can create with Terraform: [AWS VPC](aws-vpc))

1. Setup a Ray Cluster

    ```
    pip install -U "ray[default]" boto3
    ```

    ```
    ray up -y aws-config.docker.yaml
    ```

    ⚠ `aws-minimal.yaml` doesn't work as no default AMI is available for the region `ap-northeast-1`.

    <details>

    ```
    ray up -y aws-config.docker.yaml
    Usage stats collection will be enabled by default in the next release. See https://github.com/ray-project/ray/issues/20857 for more details.
    Cluster: minimal

    2022-04-28 18:47:23,229 INFO util.py:335 -- setting max workers for head node type to 0
    Checking AWS environment settings
    AWS config
      IAM Profile: ray-autoscaler-v1 [default]
      EC2 Key pair (all available node types): ray-autoscaler_1_ap-northeast-1 [default]
      VPC Subnets (all available node types): subnet-0d56536828c7b98d5, subnet-04cbf4481ef89650b, subnet-042a84abdec0ad522 [default]
      EC2 Security groups (all available node types): sg-016a1f14dce3f5504 [default]
      EC2 AMI (all available node types): ami-088da9557aae42f39

    Updating cluster configuration and running full setup.
    Cluster Ray runtime will be restarted. Confirm [y/N]: y [automatic, due to --yes]

    <1/1> Setting up head node
      Prepared bootstrap config
      New status: waiting-for-ssh
      [1/7] Waiting for SSH to become available
        Running `uptime` as a test.
        Fetched IP: 35.78.246.199
    Warning: Permanently added '35.78.246.199' (ED25519) to the list of known hosts.
    To run a command as administrator (user "root"), use "sudo <command>".
    See "man sudo_root" for details.

     09:47:29 up 10 min,  1 user,  load average: 0.00, 0.01, 0.00
    Shared connection to 35.78.246.199 closed.
        Success.
      Updating cluster configuration. [hash=f504a86c1b58ad8b0f3bec665ef9d670ce4622ff]
      New status: syncing-files
      [2/7] Processing file mounts
    Shared connection to 35.78.246.199 closed.
    Shared connection to 35.78.246.199 closed.
      [3/7] No worker file mounts to sync
      New status: setting-up
      [4/7] Running initialization commands
    Warning: Permanently added '35.78.246.199' (ED25519) to the list of known hosts.
    To run a command as administrator (user "root"), use "sudo <command>".
    See "man sudo_root" for details.

    Connection to 35.78.246.199 closed.
    Warning: Permanently added '35.78.246.199' (ED25519) to the list of known hosts.
    To run a command as administrator (user "root"), use "sudo <command>".
    See "man sudo_root" for details.

    # Executing docker install script, commit: 0221adedb4bcde0f3d18bddda023544fc56c29d1
    + sh -c apt-get update -qq >/dev/null
    + sh -c DEBIAN_FRONTEND=noninteractive apt-get install -y -qq apt-transport-https ca-certificates curl >/dev/null
    + sh -c curl -fsSL "https://download.docker.com/linux/ubuntu/gpg" | gpg --dearmor --yes -o /usr/share/keyrings/docker-archive-keyring.gpg
    + sh -c chmod a+r /usr/share/keyrings/docker-archive-keyring.gpg
    + sh -c echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu focal stable" > /etc/apt/sources.list.d/docker.list
    + sh -c apt-get update -qq >/dev/null
    + sh -c DEBIAN_FRONTEND=noninteractive apt-get install -y -qq --no-install-recommends docker-ce docker-ce-cli docker-compose-plugin docker-scan-plugin >/dev/null
    + version_gte 20.10
    + [ -z  ]
    + return 0
    + sh -c DEBIAN_FRONTEND=noninteractive apt-get install -y -qq docker-ce-rootless-extras >/dev/null
    + sh -c docker version
    Client: Docker Engine - Community
     Version:           20.10.14
     API version:       1.41
     Go version:        go1.16.15
     Git commit:        a224086
     Built:             Thu Mar 24 01:48:02 2022
     OS/Arch:           linux/amd64
     Context:           default
     Experimental:      true

    Server: Docker Engine - Community
     Engine:
      Version:          20.10.14
      API version:      1.41 (minimum version 1.12)
      Go version:       go1.16.15
      Git commit:       87a90dc
      Built:            Thu Mar 24 01:45:53 2022
      OS/Arch:          linux/amd64
      Experimental:     false
     containerd:
      Version:          1.5.11
      GitCommit:        3df54a852345ae127d1fa3092b95168e4a88e2f8
     runc:
      Version:          1.0.3
      GitCommit:        v1.0.3-0-gf46b6ba
     docker-init:
      Version:          0.19.0
      GitCommit:        de40ad0

    ================================================================================

    To run Docker as a non-privileged user, consider setting up the
    Docker daemon in rootless mode for your user:

        dockerd-rootless-setuptool.sh install

    Visit https://docs.docker.com/go/rootless/ to learn about rootless mode.


    To run the Docker daemon as a fully privileged service, but granting non-root
    users access, refer to https://docs.docker.com/go/daemon-access/

    WARNING: Access to the remote API on a privileged Docker daemon is equivalent
             to root access on the host. Refer to the 'Docker daemon attack surface'
             documentation for details: https://docs.docker.com/go/attack-surface/

    ================================================================================

    Connection to 35.78.246.199 closed.
    Warning: Permanently added '35.78.246.199' (ED25519) to the list of known hosts.
    Connection to 35.78.246.199 closed.
    Warning: Permanently added '35.78.246.199' (ED25519) to the list of known hosts.
    Connection to 35.78.246.199 closed.
      [5/7] Initalizing command runner
    Warning: Permanently added '35.78.246.199' (ED25519) to the list of known hosts.
    Shared connection to 35.78.246.199 closed.
    latest: Pulling from rayproject/ray-ml
    11323ed2c653: Pull complete
    6415333b3579: Pull complete
    83b1ad109d4b: Pull complete
    9c164dee2fdc: Pull complete
    9a197f6b670e: Pull complete
    ccdc0f0386c7: Pull complete
    8bcf409a9d54: Pull complete
    1375348d0d3c: Pull complete
    89139513a7e1: Pull complete
    3d8fc976a322: Pull complete
    301f556b9160: Pull complete
    17a957b8cbd1: Pull complete
    a3d3a36bfe54: Pull complete
    f8fb126c609f: Pull complete
    c01ba6b74da6: Pull complete
    94c3ce393f43: Pull complete
    168883de0472: Pull complete
    2d9e996de199: Pull complete
    41efc5339a3d: Pull complete
    a96f63015556: Pull complete
    54940c7af0ab: Pull complete
    3cb7c88cfd73: Pull complete
    b2d5296b3231: Pull complete
    7ce478a224ea: Pull complete
    a0874eff69ae: Pull complete
    d7b8a6048f2d: Pull complete
    Digest: sha256:a0c3a4db7e725e43203e39d053c7c2359109cf2f116ef7bf4cde8ab1a0fb27cb
    Status: Downloaded newer image for rayproject/ray-ml:latest
    docker.io/rayproject/ray-ml:latest
    Shared connection to 35.78.246.199 closed.
    Shared connection to 35.78.246.199 closed.
    Shared connection to 35.78.246.199 closed.
    Shared connection to 35.78.246.199 closed.
    Shared connection to 35.78.246.199 closed.
    b651d1dab66c677a84c47b0d3d58dc349e19490643e2797a4dd2ec61620f5d70
    Shared connection to 35.78.246.199 closed.
    Shared connection to 35.78.246.199 closed.
    sending incremental file list
    ray_bootstrap_config.yaml

    sent 1,018 bytes  received 35 bytes  2,106.00 bytes/sec
    total size is 2,100  speedup is 1.99
    Shared connection to 35.78.246.199 closed.
    Shared connection to 35.78.246.199 closed.
    sending incremental file list
    ray_bootstrap_key.pem

    sent 1,402 bytes  received 35 bytes  2,874.00 bytes/sec
    total size is 1,678  speedup is 1.17
    Shared connection to 35.78.246.199 closed.
    Shared connection to 35.78.246.199 closed.
      [6/7] Running setup commands
        (0/1) pip install 'boto3>=1.4.8'
    Requirement already satisfied: boto3>=1.4.8 in ./anaconda3/lib/python3.7/site-packages (1.21.37)
    Requirement already satisfied: s3transfer<0.6.0,>=0.5.0 in ./anaconda3/lib/python3.7/site-packages (from boto3>=1.4.8) (0.5.2)
    Requirement already satisfied: botocore<1.25.0,>=1.24.37 in ./anaconda3/lib/python3.7/site-packages (from boto3>=1.4.8) (1.24.37)
    Requirement already satisfied: jmespath<2.0.0,>=0.7.1 in ./anaconda3/lib/python3.7/site-packages (from boto3>=1.4.8) (0.10.0)
    Requirement already satisfied: urllib3<1.27,>=1.25.4 in ./anaconda3/lib/python3.7/site-packages (from botocore<1.25.0,>=1.24.37->boto3>=1.4.8) (1.26.7)
    Requirement already satisfied: python-dateutil<3.0.0,>=2.1 in ./anaconda3/lib/python3.7/site-packages (from botocore<1.25.0,>=1.24.37->boto3>=1.4.8) (2.8.2)
    Requirement already satisfied: six>=1.5 in ./anaconda3/lib/python3.7/site-packages (from python-dateutil<3.0.0,>=2.1->botocore<1.25.0,>=1.24.37->boto3>=1.4.8) (1.15.0)
    Shared connection to 35.78.246.199 closed.
      [7/7] Starting the Ray runtime
    Did not find any active Ray processes.
    Shared connection to 35.78.246.199 closed.
    Usage stats collection will be enabled by default in the next release. See https://github.com/ray-project/ray/issues/20857 for more details.
    Local node IP: 10.0.103.172
    2022-04-28 02:55:44,008 INFO services.py:1462 -- View the Ray dashboard at http://127.0.0.1:8265

    --------------------
    Ray runtime started.
    --------------------

    Next steps
      To connect to this Ray runtime from another node, run
        ray start --address='10.0.103.172:6379'

      Alternatively, use the following Python code:
        import ray
        ray.init(address='auto')

      To connect to this Ray runtime from outside of the cluster, for example to
      connect to a remote cluster from your laptop directly, use the following
      Python code:
        import ray
        ray.init(address='ray://<head_node_ip_address>:10001')

      If connection fails, check your firewall settings and network configuration.

      To terminate the Ray runtime, run
        ray stop
    Shared connection to 35.78.246.199 closed.
      New status: up-to-date

    Useful commands
      Monitor autoscaling with
        ray exec /Users/nakamasato/repos/nakamasato/ml-training/ray/aws-config.docker.yaml 'tail -n 100 -f /tmp/ray/session_latest/logs/monitor*'
      Connect to a terminal on the cluster head:
        ray attach /Users/nakamasato/repos/nakamasato/ml-training/ray/aws-config.docker.yaml
      Get a remote shell to the cluster manually:
        ssh -tt -o IdentitiesOnly=yes -i /Users/nakamasato/.ssh/ray-autoscaler_1_ap-northeast-1.pem ubuntu@35.78.246.199 docker exec -it ray_container /bin/bash
    ```

    </details>

1. Get ip address of head.

    ```
    ray get-head-ip aws-config.docker.yaml
    2022-04-29 07:47:46,075 VINFO utils.py:145 -- Creating AWS resource `ec2` in `ap-northeast-1`
    2022-04-29 07:47:46,407 VINFO utils.py:145 -- Creating AWS resource `ec2` in `ap-northeast-1`
    13.230.29.35
    ```

1. Connect to a terminal on the cluster head

    ```
    ray attach /Users/nakamasato/repos/nakamasato/ml-training/ray/aws-config.docker.yaml
    ```

1. Monitor autoscaling

    ```
    ray exec /Users/nakamasato/repos/nakamasato/ml-training/ray/aws-config.docker.yaml 'tail -n 100 -f /tmp/ray/session_latest/logs/monitor*'
    ```

1. Submit a job.

    ```
    ray submit aws-config.docker.yaml task_pattern_tree.py
    ```

    Instances are being created and terminated continuously..


    <details>

    ```
    ray submit aws-config.docker.yaml task_pattern_tree.py
    2022-05-25 05:51:39,806 INFO util.py:335 -- setting max workers for head node type to 0
    Loaded cached provider configuration
    If you experience issues with the cloud provider, try re-running the command with --no-config-cache.
    Fetched IP: 35.77.53.85
    Shared connection to 35.77.53.85 closed.
    Shared connection to 35.77.53.85 closed.
    2022-05-25 05:51:42,919 INFO util.py:335 -- setting max workers for head node type to 0
    Fetched IP: 35.77.53.85
    Shared connection to 35.77.53.85 closed.
    Array size: 200000
    Sequential execution: 0.039
    Distributed execution: 1.131
    --------------------
    Array size: 4000000
    Sequential execution: 5.835
    (scheduler +9s) Tip: use `ray status` to view detailed cluster status. To disable these messages, set RAY_SCHEDULER_EVENTS=0.
    (scheduler +9s) Adding 1 nodes of type ray.worker.default.
    (scheduler +14s) Adding 1 nodes of type ray.worker.default.
    2022-05-24 13:52:02,353 WARNING worker.py:1382 -- WARNING: 8 PYTHON worker processes have been started on node: d1b27708d013cf095512c80ddafaf0d9ad9cc8f8c31f9d0b24850579 with address: 10.0.103.208. This could be a result of using a large number of actors, or due to tasks blocked in ray.get() calls (see https://github.com/ray-project/ray/issues/3644 for some discussion of workarounds).
    Distributed execution: 18.052
    --------------------
    Array size: 8000000
    Sequential execution: 15.108
    2022-05-24 13:52:40,207 WARNING worker.py:1382 -- WARNING: 10 PYTHON worker processes have been started on node: d1b27708d013cf095512c80ddafaf0d9ad9cc8f8c31f9d0b24850579 with address: 10.0.103.208. This could be a result of using a large number of actors, or due to tasks blocked in ray.get() calls (see https://github.com/ray-project/ray/issues/3644 for some discussion of workarounds).
    2022-05-24 13:52:44,694 WARNING worker.py:1382 -- WARNING: 12 PYTHON worker processes have been started on node: d1b27708d013cf095512c80ddafaf0d9ad9cc8f8c31f9d0b24850579 with address: 10.0.103.208. This could be a result of using a large number of actors, or due to tasks blocked in ray.get() calls (see https://github.com/ray-project/ray/issues/3644 for some discussion of workarounds).
    2022-05-24 13:52:46,193 WARNING worker.py:1382 -- WARNING: 14 PYTHON worker processes have been started on node: d1b27708d013cf095512c80ddafaf0d9ad9cc8f8c31f9d0b24850579 with address: 10.0.103.208. This could be a result of using a large number of actors, or due to tasks blocked in ray.get() calls (see https://github.com/ray-project/ray/issues/3644 for some discussion of workarounds).
    2022-05-24 13:52:47,724 WARNING worker.py:1382 -- WARNING: 16 PYTHON worker processes have been started on node: d1b27708d013cf095512c80ddafaf0d9ad9cc8f8c31f9d0b24850579 with address: 10.0.103.208. This could be a result of using a large number of actors, or due to tasks blocked in ray.get() calls (see https://github.com/ray-project/ray/issues/3644 for some discussion of workarounds).
    2022-05-24 13:52:49,588 WARNING worker.py:1382 -- WARNING: 19 PYTHON worker processes have been started on node: d1b27708d013cf095512c80ddafaf0d9ad9cc8f8c31f9d0b24850579 with address: 10.0.103.208. This could be a result of using a large number of actors, or due to tasks blocked in ray.get() calls (see https://github.com/ray-project/ray/issues/3644 for some discussion of workarounds).
    2022-05-24 13:52:51,313 WARNING worker.py:1382 -- WARNING: 20 PYTHON worker processes have been started on node: d1b27708d013cf095512c80ddafaf0d9ad9cc8f8c31f9d0b24850579 with address: 10.0.103.208. This could be a result of using a large number of actors, or due to tasks blocked in ray.get() calls (see https://github.com/ray-project/ray/issues/3644 for some discussion of workarounds).
    2022-05-24 13:52:58,805 WARNING worker.py:1382 -- WARNING: 22 PYTHON worker processes have been started on node: d1b27708d013cf095512c80ddafaf0d9ad9cc8f8c31f9d0b24850579 with address: 10.0.103.208. This could be a result of using a large number of actors, or due to tasks blocked in ray.get() calls (see https://github.com/ray-project/ray/issues/3644 for some discussion of workarounds).
    2022-05-24 13:52:59,761 WARNING worker.py:1382 -- WARNING: 24 PYTHON worker processes have been started on node: d1b27708d013cf095512c80ddafaf0d9ad9cc8f8c31f9d0b24850579 with address: 10.0.103.208. This could be a result of using a large number of actors, or due to tasks blocked in ray.get() calls (see https://github.com/ray-project/ray/issues/3644 for some discussion of workarounds).
    Distributed execution: 45.697
    --------------------
    Array size: 10000000
    Sequential execution: 22.814
    (scheduler +2m2s) Warning: The following resource request cannot be scheduled right now: {'CPU': 1.0}. This is likely due to all cluster resources being claimed by actors. Consider creating fewer actors or adding more nodes to this Ray cluster.
    (scheduler +2m28s) Resized to 4 CPUs.
    Distributed execution: 50.749
    --------------------
    Array size: 20000000
    (scheduler +3m14s) Resized to 6 CPUs.
    Sequential execution: 55.681
    2022-05-24 13:55:41,083 WARNING worker.py:1382 -- WARNING: 8 PYTHON worker processes have been started on node: fbd302fdeae6c78aaa9a68efcf4966a40eb8ac252203af42b9b27b60 with address: 10.0.103.232. This could be a result of using a large number of actors, or due to tasks blocked in ray.get() calls (see https://github.com/ray-project/ray/issues/3644 for some discussion of workarounds).
    2022-05-24 13:55:42,331 WARNING worker.py:1382 -- WARNING: 10 PYTHON worker processes have been started on node: fbd302fdeae6c78aaa9a68efcf4966a40eb8ac252203af42b9b27b60 with address: 10.0.103.232. This could be a result of using a large number of actors, or due to tasks blocked in ray.get() calls (see https://github.com/ray-project/ray/issues/3644 for some discussion of workarounds).
    2022-05-24 13:55:42,870 WARNING worker.py:1382 -- WARNING: 8 PYTHON worker processes have been started on node: 096b57a8b91d0919ed8224be96e20497710c6fc188162079e5a3551f with address: 10.0.103.17. This could be a result of using a large number of actors, or due to tasks blocked in ray.get() calls (see https://github.com/ray-project/ray/issues/3644 for some discussion of workarounds).
    2022-05-24 13:55:43,523 WARNING worker.py:1382 -- WARNING: 12 PYTHON worker processes have been started on node: fbd302fdeae6c78aaa9a68efcf4966a40eb8ac252203af42b9b27b60 with address: 10.0.103.232. This could be a result of using a large number of actors, or due to tasks blocked in ray.get() calls (see https://github.com/ray-project/ray/issues/3644 for some discussion of workarounds).
    2022-05-24 13:55:53,981 WARNING worker.py:1382 -- WARNING: 10 PYTHON worker processes have been started on node: 096b57a8b91d0919ed8224be96e20497710c6fc188162079e5a3551f with address: 10.0.103.17. This could be a result of using a large number of actors, or due to tasks blocked in ray.get() calls (see https://github.com/ray-project/ray/issues/3644 for some discussion of workarounds).
    (scheduler +4m10s) Warning: The following resource request cannot be scheduled right now: {'CPU': 1.0}. This is likely due to all cluster resources being claimed by actors. Consider creating fewer actors or adding more nodes to this Ray cluster.
    2022-05-24 13:55:55,562 WARNING worker.py:1382 -- WARNING: 12 PYTHON worker processes have been started on node: 096b57a8b91d0919ed8224be96e20497710c6fc188162079e5a3551f with address: 10.0.103.17. This could be a result of using a large number of actors, or due to tasks blocked in ray.get() calls (see https://github.com/ray-project/ray/issues/3644 for some discussion of workarounds).
    2022-05-24 13:55:56,807 WARNING worker.py:1382 -- WARNING: 14 PYTHON worker processes have been started on node: 096b57a8b91d0919ed8224be96e20497710c6fc188162079e5a3551f with address: 10.0.103.17. This could be a result of using a large number of actors, or due to tasks blocked in ray.get() calls (see https://github.com/ray-project/ray/issues/3644 for some discussion of workarounds).
    2022-05-24 13:55:58,590 WARNING worker.py:1382 -- WARNING: 16 PYTHON worker processes have been started on node: 096b57a8b91d0919ed8224be96e20497710c6fc188162079e5a3551f with address: 10.0.103.17. This could be a result of using a large number of actors, or due to tasks blocked in ray.get() calls (see https://github.com/ray-project/ray/issues/3644 for some discussion of workarounds).
    Distributed execution: 54.941
    --------------------
    Shared connection to 35.77.53.85 closed.
    ```

    </details>


    While running the job, also checked the cluster:

    <details>

    ```
    esources
    ---------------------------------------------------------------
    Usage:
     0.0/2.0 CPU
     0.00/4.358 GiB memory
     0.00/2.179 GiB object_store_memory

    Demands:
     (no resource demands)
    2022-05-24 13:58:39,155 INFO autoscaler.py:330 --
    ======== Autoscaler status: 2022-05-24 13:58:39.155496 ========
    Node status
    ---------------------------------------------------------------
    Healthy:
     1 ray.head.default
    Pending:
     (no pending nodes)
    Recent failures:
     (no failures)

    Resources
    ---------------------------------------------------------------
    Usage:
     0.0/2.0 CPU
     0.00/4.358 GiB memory
     0.00/2.179 GiB object_store_memory

    Demands:
     (no resource demands)
    2022-05-24 13:58:44,235 INFO autoscaler.py:330 --
    ======== Autoscaler status: 2022-05-24 13:58:44.235089 ========
    Node status
    ---------------------------------------------------------------
    Healthy:
     1 ray.head.default
    Pending:
     (no pending nodes)
    Recent failures:
     (no failures)

    Resources
    ---------------------------------------------------------------
    Usage:
     0.0/2.0 CPU
     0.00/4.358 GiB memory
     0.00/2.179 GiB object_store_memory

    Demands:
     (no resource demands)
    2022-05-24 13:58:49,312 INFO autoscaler.py:330 --
    ======== Autoscaler status: 2022-05-24 13:58:49.312784 ========
    Node status
    ---------------------------------------------------------------
    Healthy:
     1 ray.head.default
    Pending:
     (no pending nodes)
    Recent failures:
     (no failures)

    Resources
    ---------------------------------------------------------------
    Usage:
     0.0/2.0 CPU
     0.00/4.358 GiB memory
     0.00/2.179 GiB object_store_memory

    Demands:
     (no resource demands)
    2022-05-24 13:58:54,384 INFO autoscaler.py:330 --
    ======== Autoscaler status: 2022-05-24 13:58:54.384371 ========
    Node status
    ---------------------------------------------------------------
    Healthy:
     1 ray.head.default
    Pending:
     (no pending nodes)
    Recent failures:
     (no failures)

    Resources
    ---------------------------------------------------------------
    Usage:
     0.0/2.0 CPU
     0.00/4.358 GiB memory
     0.00/2.179 GiB object_store_memory

    Demands:
     (no resource demands)
    2022-05-24 13:58:59,465 INFO autoscaler.py:330 --
    ======== Autoscaler status: 2022-05-24 13:58:59.465703 ========
    Node status
    ---------------------------------------------------------------
    Healthy:
     1 ray.head.default
    Pending:
     (no pending nodes)
    Recent failures:
     (no failures)

    Resources
    ---------------------------------------------------------------
    Usage:
     0.0/2.0 CPU
     0.00/4.358 GiB memory
     0.00/2.179 GiB object_store_memory

    Demands:
     (no resource demands)
    2022-05-24 13:59:04,540 INFO autoscaler.py:330 --
    ======== Autoscaler status: 2022-05-24 13:59:04.540569 ========
    Node status
    ---------------------------------------------------------------
    Healthy:
     1 ray.head.default
    Pending:
     (no pending nodes)
    Recent failures:
     (no failures)

    Resources
    ---------------------------------------------------------------
    Usage:
     0.0/2.0 CPU
     0.00/4.358 GiB memory
     0.00/2.179 GiB object_store_memory

    Demands:
     (no resource demands)
    2022-05-24 13:59:09,610 INFO autoscaler.py:330 --
    ======== Autoscaler status: 2022-05-24 13:59:09.610690 ========
    Node status
    ---------------------------------------------------------------
    Healthy:
     1 ray.head.default
    Pending:
     (no pending nodes)
    Recent failures:
     (no failures)

    Resources
    ---------------------------------------------------------------
    Usage:
     0.0/2.0 CPU
     0.00/4.358 GiB memory
     0.00/2.179 GiB object_store_memory

    Demands:
     (no resource demands)
    2022-05-24 13:59:14,682 INFO autoscaler.py:330 --
    ======== Autoscaler status: 2022-05-24 13:59:14.682181 ========
    Node status
    ---------------------------------------------------------------
    Healthy:
     1 ray.head.default
    Pending:
     (no pending nodes)
    Recent failures:
     (no failures)

    Resources
    ---------------------------------------------------------------
    Usage:
     0.0/2.0 CPU
     0.00/4.358 GiB memory
     0.00/2.179 GiB object_store_memory

    Demands:
     (no resource demands)
    2022-05-24 13:59:19,772 INFO autoscaler.py:330 --
    ======== Autoscaler status: 2022-05-24 13:59:19.772812 ========
    Node status
    ---------------------------------------------------------------
    Healthy:
     1 ray.head.default
    Pending:
     (no pending nodes)
    Recent failures:
     (no failures)

    Resources
    ---------------------------------------------------------------
    Usage:
     0.0/2.0 CPU
     0.00/4.358 GiB memory
     0.00/2.179 GiB object_store_memory

    Demands:
     (no resource demands)
    Shared connection to 35.77.53.85 closed.
    Error: Command failed:

      ssh -tt -i /Users/nakamasato/.ssh/ray-autoscaler_ap-northeast-1.pem -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o IdentitiesOnly=yes -o ExitOnForwardFailure=yes -o ServerAliveInterval=5 -o ServerAliveCountMax=3 -o ControlMaster=auto -o ControlPath=/tmp/ray_ssh_a09e268f38/dc43e863c1/%C -o ControlPersist=10s -o ConnectTimeout=120s ubuntu@35.77.53.85 bash --login -c -i 'true && source ~/.bashrc && export OMP_NUM_THREADS=1 PYTHONWARNINGS=ignore && (docker exec -it  ray_container /bin/bash -c '"'"'bash --login -c -i '"'"'"'"'"'"'"'"'true && source ~/.bashrc && export OMP_NUM_THREADS=1 PYTHONWARNINGS=ignore && (tail -n 100 -f /tmp/ray/session_latest/logs/monitor*)'"'"'"'"'"'"'"'"''"'"' )'
    ```


    </details>

1. Drop ray cluster (EC2 instances are also terminated.)

    ```
    ray down aws-config.docker.yaml
    ```

    <details>

    ```
    ray down aws-config.docker.yaml
    2022-04-28 19:08:51,463 INFO util.py:335 -- setting max workers for head node type to 0
    Loaded cached provider configuration
    If you experience issues with the cloud provider, try re-running the command with --no-config-cache.
    Destroying cluster. Confirm [y/N]: y
    2022-04-28 19:09:04,456 INFO util.py:335 -- setting max workers for head node type to 0
    Fetched IP: 35.78.246.199
    Warning: Permanently added '35.78.246.199' (ED25519) to the list of known hosts.
    Stopped only 6 out of 7 Ray processes within the grace period 10 seconds. Set `-v` to see more details. Remaining processes [psutil.Process(pid=328, name='python', status='running', started='02:55:41')] will be forcefully terminated.
    You can also use `--force` to forcefully terminate processes or set higher `--grace-period` to wait longer time for proper termination.
    Shared connection to 35.78.246.199 closed.
    Fetched IP: 35.78.246.199
    Stopping instances i-0e5c28f2b9a5a2cbf (to terminate instead, set `cache_stopped_nodes: False` under `provider` in the cluster configuration)
    Requested 1 nodes to shut down. [interval=1s]
    0 nodes remaining after 5 second(s).
    No nodes remaining.
    ```

    </details>

    Clean up remaining resources:

    1. ec2:

        ```
        aws ec2 delete-key-pair --key-name ray-autoscaler_ap-northeast-1
        security_group_id=$(aws ec2 describe-security-groups --filters Name=group-name,Values=ray-autoscaler-minimal | jq -r '.SecurityGroups[].GroupId')
        echo $security_group_id
        aws ec2 delete-security-group --group-id $security_group_id
        ```

    1. local:
        ```
        rm ~/.ssh/ray-autoscaler_*
        ```
    1. iam:
        ```
        aws iam remove-role-from-instance-profile --instance-profile-name ray-autoscaler-v1  --role-name ray-autoscaler-v1
        aws iam delete-instance-profile --instance-profile-name ray-autoscaler-v1
        aws iam detach-role-policy --role-name ray-autoscaler-v1 --policy-arn arn:aws:iam::aws:policy/AmazonEC2FullAccess
        aws iam detach-role-policy --role-name ray-autoscaler-v1 --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess
        aws iam delete-role --role-name ray-autoscaler-v1
        ```
    1. If you created VPC and subnet with Terraform, you can clean them up. (complete within a few seconds)

        ```
        cd aws-vpc
        terraform destroy
        ```

        <details>

        If you get this error, you might forget to delete security group.

        ```
        │ Error: error deleting EC2 VPC (vpc-0e8f61401b5cc4c96): DependencyViolation: The vpc 'vpc-0e8f61401b5cc4c96' has dependencies and cannot be deleted.
        │       status code: 400, request id: f09016c6-7c65-4e55-b467-41fdc830eb3e
        │
        ```

        </details>

#### Errors
1. Error1: No usable subnets found

    <details>

    ```
    ➜  ray git:(ray-getting-started) ✗ ray down -y aws-config.docker.yaml
    2022-04-28 13:33:15,797 INFO util.py:335 -- setting max workers for head node type to 0
    2022-04-28 13:33:15,798 INFO util.py:339 -- setting max workers for ray.worker.default to 2
    Checking AWS environment settings
    No usable subnets found, try manually creating an instance in your specified region to populate the list of subnets and trying this again.
    Note that the subnet must map public IPs on instance launch unless you set `use_internal_ips: true` in the `provider` config.
    ```

    </details>

    solution:

    ```
    cd aws-vpc
    terraform init
    terraform apply
    ```

1. Error2: no default AMI is available for the region `ap-northeast-1`

    <details>

    ```
    Node type `ray.head.default` has no ImageId in its node_config and no default AMI is available for the region `ap-northeast-1`. ImageId will need to be set manually in your cluster config.
    ```

    </details>

    solution:

    Get from ec2 console -> `ami-088da9557aae42f39`

1. Error3: The architecture 'x86_64' of the specified instance type does not match the architecture 'arm64'

    <details>

    ```
    botocore.exceptions.ClientError: An error occurred (InvalidParameterValue) when calling the RunInstances operation: The architecture 'x86_64' of the specified instance type does not match the architecture 'arm64' of the specified AMI. Specify an instance type and an AMI that have matching architectures, and try again. You can use 'describe-instance-types' or 'describe-images' to discover the architecture of the instance type or AMI.
    ```

    </details>

    Get from ec2 console -> `ami-088da9557aae42f39`

1. Error4: pip not found

    <details>

    ```
    Command 'pip' not found, but can be installed with:

    sudo apt install python3-pip

    Shared connection to 35.78.246.199 closed.
      New status: update-failed
      !!!
      SSH command failed.
      !!!

      Failed to setup head node.
    ```

    </details>

    Try using docker with

    ```yaml
    docker:
        image: "rayproject/ray-ml:latest"
        container_name: "ray_container"
    ```

1. Error5: Command 'docker' not found

    <details>

    ```
    Usage stats collection will be enabled by default in the next release. See https://github.com/ray-project/ray/issues/20857 for more details.
    Cluster: minimal

    2022-04-28 18:43:30,627 INFO util.py:335 -- setting max workers for head node type to 0
    Checking AWS environment settings
    AWS config
      IAM Profile: ray-autoscaler-v1 [default]
      EC2 Key pair (all available node types): ray-autoscaler_1_ap-northeast-1 [default]
      VPC Subnets (all available node types): subnet-0d56536828c7b98d5, subnet-04cbf4481ef89650b, subnet-042a84abdec0ad522 [default]
      EC2 Security groups (all available node types): sg-016a1f14dce3f5504 [default]
      EC2 AMI (all available node types): ami-088da9557aae42f39

    Updating cluster configuration and running full setup.
    Cluster Ray runtime will be restarted. Confirm [y/N]: y [automatic, due to --yes]

    <1/1> Setting up head node
      Prepared bootstrap config
      New status: waiting-for-ssh
      [1/7] Waiting for SSH to become available
        Running `uptime` as a test.
        Fetched IP: 35.78.246.199
    Warning: Permanently added '35.78.246.199' (ED25519) to the list of known hosts.
    To run a command as administrator (user "root"), use "sudo <command>".
    See "man sudo_root" for details.

     09:43:36 up 7 min,  1 user,  load average: 0.00, 0.04, 0.02
    Shared connection to 35.78.246.199 closed.
        Success.
      Updating cluster configuration. [hash=e704226942567d8bf66edaedb68b995897fcca43]
      New status: syncing-files
      [2/7] Processing file mounts
    Shared connection to 35.78.246.199 closed.
    Shared connection to 35.78.246.199 closed.
      [3/7] No worker file mounts to sync
      New status: setting-up
      [4/7] No initialization commands to run.
      [5/7] Initalizing command runner
    Shared connection to 35.78.246.199 closed.
    2022-04-28 18:43:39,917 ERROR command_runner.py:790 -- Docker not installed. You can install Docker by adding the following commands to 'initialization_commands':
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    sudo systemctl restart docker -f
    To run a command as administrator (user "root"), use "sudo <command>".
    See "man sudo_root" for details.


    Command 'docker' not found, but can be installed with:

    sudo apt install docker.io

    Shared connection to 35.78.246.199 closed.
      New status: update-failed
      !!!
      SSH command failed.
      !!!

    ```

    <details>

    solution:

    ```yaml
    initialization_commands:
        - curl -fsSL https://get.docker.com -o get-docker.sh
        - sudo sh get-docker.sh
        - sudo usermod -aG docker $USER
        - sudo systemctl restart docker -f
    ```

#### Implementation

1. [sdk.create_or_update_cluster](https://github.com/ray-project/ray/blob/629424f48957af55cf06d86d23b850be73fb3017/python/ray/autoscaler/sdk/sdk.py#L17-L49) calls `_private.commands.create_or_update_cluster`
1. [_private.commands.create_or_update_cluster](https://github.com/ray-project/ray/blob/60054995e65304fb14e6d0ab69bdec07aa9389fe/python/ray/autoscaler/_private/commands.py#L180-L285) calls `_bootstrap_config`
1. [_bootstrap_config] gets `importer = _NODE_PROVIDERS.get(config["provider"]["type"])` -> `provider_cls = importer(config["provider"])` -> calls `provider_cls.bootstrap_config(config)`
1. [AWSNodeProvider(NodeProvider).bootstrap_config](https://github.com/ray-project/ray/blob/7f1bacc7dc9caf6d0ec042e39499bbf1d9a7d065/python/ray/autoscaler/_private/aws/node_provider.py#L592-L594) calls `bootstrap_aws`.
1. [bootstrap_aws(config)](https://github.com/ray-project/ray/blob/629424f48957af55cf06d86d23b850be73fb3017/python/ray/autoscaler/_private/aws/config.py#L217-L256)
