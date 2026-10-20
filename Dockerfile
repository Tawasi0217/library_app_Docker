FROM continuumio/miniconda3:24.7.1-0
WORKDIR /app
COPY requirements.txt environment.yml ./
RUN conda env create -f environment.yml && conda clean -afy
COPY . .
RUN chmod +x docker-entrypoint.sh && mkdir -p /app/instance
ENV PATH=/opt/conda/envs/library-loan-app/bin:$PATH
ENV APP_ENV=production
ENV DATABASE_URL=sqlite:////app/instance/library.db
EXPOSE 5000
ENTRYPOINT ["./docker-entrypoint.sh"]
