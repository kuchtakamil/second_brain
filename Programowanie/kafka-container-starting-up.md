# Kafka container starting up.

**Data:** 2023-05-09

---

**User:**

Co tu się zepsuło
{"log":"\u001b[38;5;6mkafka \u001b[38;5;5m20:35:03.88 \u001b[0m\n","stream":"stderr","time":"2023-05-09T20:35:03.884039427Z"}
{"log":"\u001b[38;5;6mkafka \u001b[38;5;5m20:35:03.88 \u001b[0m\u001b[1mWelcome to the Bitnami kafka container\u001b[0m\n","stream":"stderr","time":"2023-05-09T20:35:03.886090263Z"}
{"log":"\u001b[38;5;6mkafka \u001b[38;5;5m20:35:03.88 \u001b[0mSubscribe to project updates by watching \u001b[1mhttps://github.com/bitnami/containers\u001b[0m\n","stream":"stderr","time":"2023-05-09T20:35:03.888407522Z"}
{"log":"\u001b[38;5;6mkafka \u001b[38;5;5m20:35:03.88 \u001b[0mSubmit issues and feature requests at \u001b[1mhttps://github.com/bitnami/containers/issues\u001b[0m\n","stream":"stderr","time":"2023-05-09T20:35:03.890465083Z"}
{"log":"\u001b[38;5;6mkafka \u001b[38;5;5m20:35:03.89 \u001b[0m\n","stream":"stderr","time":"2023-05-09T20:35:03.892816518Z"}
{"log":"\u001b[38;5;6mkafka \u001b[38;5;5m20:35:03.89 \u001b[0m\u001b[38;5;2mINFO \u001b[0m ==\u003e ** Starting Kafka setup **\n","stream":"stderr","time":"2023-05-09T20:35:03.895282257Z"}
{"log":"\u001b[38;5;6mkafka \u001b[38;5;5m20:35:03.97 \u001b[0m\u001b[38;5;3mWARN \u001b[0m ==\u003e KAFKA_CFG_LISTENERS must include a listener for CONTROLLER\n","stream":"stderr","time":"2023-05-09T20:35:03.973807888Z"}
{"log":"\u001b[38;5;6mkafka \u001b[38;5;5m20:35:03.98 \u001b[0m\u001b[38;5;3mWARN \u001b[0m ==\u003e You set the environment variable ALLOW_PLAINTEXT_LISTENER=yes. For safety reasons, do not use this flag in a production environment.\n","stream":"stderr","time":"2023-05-09T20:35:03.983498512Z"}
{"log":"\u001b[38;5;6mkafka \u001b[38;5;5m20:35:04.00 \u001b[0m\u001b[38;5;2mINFO \u001b[0m ==\u003e Initializing Kafka...\n","stream":"stderr","time":"2023-05-09T20:35:04.002852981Z"}
{"log":"\u001b[38;5;6mkafka \u001b[38;5;5m20:35:04.01 \u001b[0m\u001b[38;5;2mINFO \u001b[0m ==\u003e No injected configuration files found, creating default config files\n","stream":"stderr","time":"2023-05-09T20:35:04.020894489Z"}
{"log":"\u001b[38;5;6mkafka \u001b[38;5;5m20:35:04.21 \u001b[0m\u001b[38;5;2mINFO \u001b[0m ==\u003e Configuring Kafka for inter-broker communications with PLAINTEXT authentication.\n","stream":"stderr","time":"2023-05-09T20:35:04.211215929Z"}
{"log":"\u001b[38;5;6mkafka \u001b[38;5;5m20:35:04.21 \u001b[0m\u001b[38;5;3mWARN \u001b[0m ==\u003e Inter-broker communications are configured as PLAINTEXT. This is not safe for production environments.\n","stream":"stderr","time":"2023-05-09T20:35:04.21726208Z"}
{"log":"\u001b[38;5;6mkafka \u001b[38;5;5m20:35:04.21 \u001b[0m\u001b[38;5;2mINFO \u001b[0m ==\u003e Configuring Kafka for external client communications with PLAINTEXT authentication.\n","stream":"stderr","time":"2023-05-09T20:35:04.219464584Z"}
{"log":"\u001b[38;5;6mkafka \u001b[38;5;5m20:35:04.22 \u001b[0m\u001b[38;5;3mWARN \u001b[0m ==\u003e External client communications are configured using PLAINTEXT listeners. For safety reasons, do not use this in a production environment.\n","stream":"stderr","time":"2023-05-09T20:35:04.222001019Z"}
{"log":"\u001b[38;5;6mkafka \u001b[38;5;5m20:35:04.22 \u001b[0m\u001b[38;5;2mINFO \u001b[0m ==\u003e Initializing KRaft...\n","stream":"stderr","time":"2023-05-09T20:35:04.23159301Z"}
{"log":"\u001b[38;5;6mkafka \u001b[38;5;5m20:35:04.23 \u001b[0m\u001b[38;5;3mWARN \u001b[0m ==\u003e KAFKA_KRAFT_CLUSTER_ID not set - If using multiple nodes then you must use the same Cluster ID for each one\n","stream":"stderr","time":"2023-05-09T20:35:04.232405185Z"}
{"log":"\u001b[38;5;6mkafka \u001b[38;5;5m20:35:05.72 \u001b[0m\u001b[38;5;2mINFO \u001b[0m ==\u003e Generated Kafka cluster ID 'V_UAhwiTQm2J4kj0SwrDQg'\n","stream":"stderr","time":"2023-05-09T20:35:05.729548912Z"}
{"log":"\u001b[38;5;6mkafka \u001b[38;5;5m20:35:05.73 \u001b[0m\u001b[38;5;2mINFO \u001b[0m ==\u003e Formatting storage directories to add metadata...\n","stream":"stderr","time":"2023-05-09T20:35:05.73226583Z"}

---

**Assistant:**

It seems that this log is from a Kafka container. The container is starting up, and some warnings and informational messages are being printed to the standard error stream. Two warnings are present in the log: `KAFKA_CFG_LISTENERS must include a listener for CONTROLLER` and `Inter-broker communications are configured as PLAINTEXT. This is not safe for production environments.` The log also includes links to the Bitnami containers project and its issue tracker.