# main/migrations/0002_custom_indexes.py

from django.db import migrations
from django.contrib.postgres.operations import CreateExtension


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        CreateExtension('pg_trgm'),  # for trigram similarity search on skills
        migrations.RunSQL(
            sql="""
                ALTER TABLE resumes ADD COLUMN IF NOT EXISTS search_vector tsvector;
                CREATE INDEX IF NOT EXISTS resumes_search_vector_idx
                    ON resumes USING GIN(search_vector);
                CREATE INDEX IF NOT EXISTS skills_name_trgm_idx
                    ON skills USING GIN(name gin_trgm_ops);
            """,
            reverse_sql="""
                DROP INDEX IF EXISTS resumes_search_vector_idx;
                DROP INDEX IF EXISTS skills_name_trgm_idx;
                ALTER TABLE resumes DROP COLUMN IF EXISTS search_vector;
            """
        ),
    ]