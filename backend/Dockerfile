FROM python:3.11-slim

WORKDIR /code

ENV PYTHONPATH "${PYTHONPATH}:/code"

COPY . .

# NEU: Mach das Entrypoint-Skript ausführbar
RUN chmod +x ./entrypoint.sh

RUN pip install --no-cache-dir -r requirements.txt

# NEU: Setze unser Skript als den "Eingangspunkt" des Containers
ENTRYPOINT ["./entrypoint.sh"]

# Der CMD-Befehl wird jetzt als Argument an das Entrypoint-Skript übergeben
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]