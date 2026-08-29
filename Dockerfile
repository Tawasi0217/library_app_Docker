FROM continuumio/miniconda3:24.7.1-0

WORKDIR /app

COPY environment.yml .
RUN conda env create -f environment.yml \
    && conda clean -afy

SHELL ["conda", "run", "-n", "library-loan-app", "/bin/sh", "-c"]

COPY . .
RUN chmod +x docker-entrypoint.sh

ENV PATH=/opt/conda/envs/library-loan-app/bin:$PATH
ENV FLASK_ENV=production
ENV DATABASE_URL=sqlite:////app/instance/library.db

EXPOSE 5000

ENTRYPOINT ["./docker-entrypoint.sh"]
