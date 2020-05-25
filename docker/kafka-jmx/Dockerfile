FROM bitnami/kafka:2.5.0

ARG jolokia_home=/opt/jolokia
ARG jolokia_jar=${jolokia_home}/jolokia-agent.jar
ARG jmx_port=9992

USER 1001

COPY jolokia-jvm-1.6.2-agent.jar ${jolokia_jar}

ENV KAFKA_OPTS="-javaagent:${jolokia_jar}=port=${jmx_port},host=* $KAFKA_OPTS"

