FROM python:3.7 as base

FROM base as builder

RUN mkdir /install
WORKDIR /install

COPY requirements /requirements
RUN pip install --install-option="--prefix=/install" -r /requirements/prod.txt

FROM base
COPY --from=builder /install /usr/local
COPY . /app
WORKDIR app
CMD ["bash"]