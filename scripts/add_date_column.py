from src.config.data_base import app, init_db, db


def ensure_date_column():
    with app.app_context():
        # Inicializa o db (usa a configuração já presente em src/config/data_base.py)
        init_db(app)

        engine = db.engine
        # Verifica se a coluna 'date' existe na tabela 'sales' no schema atual
        check_sql = (
            "SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS "
            "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'sales' AND COLUMN_NAME = 'date'"
        )
        # Compatibilidade: executa via conexão
        with engine.connect() as conn:
            try:
                row = conn.execute(check_sql)
                count = row.scalar() if row is not None else 0
            except Exception:
                # Se a consulta falhar, assumimos que a coluna não existe
                count = 0

            if count and int(count) > 0:
                print("A coluna 'date' já existe na tabela 'sales'. Nada a fazer.")
                return

            # Adiciona a coluna 'date' como DATETIME NULL (coloca após total_price)
            alter_sql = "ALTER TABLE sales ADD COLUMN `date` DATETIME NULL AFTER total_price;"
            try:
                conn.execute(alter_sql)
                print("Coluna 'date' adicionada com sucesso à tabela 'sales'.")
            except Exception as e:
                print("Falha ao adicionar a coluna 'date'. Erro:", e)


if __name__ == '__main__':
    ensure_date_column()
