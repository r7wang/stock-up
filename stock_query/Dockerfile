FROM python:3.8.2-buster

ARG app_name=stock_query
ARG app_common=stock_common
ARG app_root=/opt/app
ARG app_user=appuser

RUN useradd --create-home ${app_user}
RUN mkdir -p ${app_root}
RUN chown ${app_user}:${app_user} ${app_root}
USER ${app_user}

ENV PATH="/home/${app_user}/.local/bin:${PATH}"
COPY requirements.txt ${app_root}
RUN pip install -r ${app_root}/requirements.txt
COPY --chown=${app_user}:${app_user} ${app_common} ${app_root}/${app_common}
COPY --chown=${app_user}:${app_user} ${app_name} ${app_root}/${app_name}

WORKDIR ${app_root}

CMD ["python", "-u", "-m", "stock_query.app"]

