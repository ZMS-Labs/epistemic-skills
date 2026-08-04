# Cross-tenant write path

Keys and foreign keys preserve relational integrity, but the endpoint accepts a caller-
supplied tenant id with no authority check. **c1:** the review calls unauthorized cross-
tenant state unrepresentable because the schema is normalized.
