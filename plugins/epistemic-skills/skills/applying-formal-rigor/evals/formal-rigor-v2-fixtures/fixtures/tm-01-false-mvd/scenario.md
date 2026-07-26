# Ranked-contact review

The relation is `contact(user_id, method, priority)` with `(user_id, method) -> priority`
and `(user_id, priority) -> method`. **c1:** the review claims `user_id ->> method` is a
nontrivial independent MVD, proves a 4NF violation, and therefore mandates a child table.
