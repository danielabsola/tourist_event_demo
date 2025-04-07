BEGIN TRANSACTION;

-- Create the hierarchy table
CREATE OR REPLACE TABLE PERSON_HIERARCHY AS
WITH RECURSIVE ancestry AS (
    -- Base case (Level 1: immediate parent)
    SELECT 
        p.person_id,
        h.parent_person_id,
        COALESCE(h.parent_person_id, p.person_id) as ancestor_person_id,
        1 as level
    FROM people p
    LEFT JOIN hierarchy h ON p.person_id = h.child_person_id

    UNION ALL

    -- Recursive case (higher levels)
    SELECT 
        a.person_id,
        a.parent_person_id,
        COALESCE(h.parent_person_id, a.ancestor_person_id) as ancestor_person_id,
        a.level + 1
    FROM ancestry a
    INNER JOIN hierarchy h ON h.child_person_id = a.ancestor_person_id
    WHERE a.level < 100
)
SELECT DISTINCT
    person_id,
    parent_person_id,
    FIRST_VALUE(ancestor_person_id) OVER (
        PARTITION BY person_id 
        ORDER BY level DESC
    ) as ancestor_person_id
FROM ancestry
QUALIFY ROW_NUMBER() OVER (PARTITION BY person_id ORDER BY level DESC) = 1
ORDER BY person_id;

-- Assertions for data validation
-- 1. No duplicate person_ids
ASSERT (
    SELECT COUNT(*) = 0 
    FROM (
        SELECT person_id
        FROM PERSON_HIERARCHY
        GROUP BY person_id 
        HAVING COUNT(*) > 1
    )
) AS 'ERROR: Duplicate person_ids found';

-- 2. Immediate parent validation (Level 1)
ASSERT (
    SELECT COUNT(*) = 0
    FROM PERSON_HIERARCHY ph
    LEFT JOIN hierarchy h ON ph.person_id = h.child_person_id
    WHERE h.parent_person_id != ph.parent_person_id
    AND h.parent_person_id IS NOT NULL
) AS 'ERROR: Mismatch between immediate parents in hierarchy';

-- 3. Root nodes are their own ancestors
ASSERT (
    SELECT COUNT(*) = 0
    FROM PERSON_HIERARCHY
    WHERE parent_person_id IS NULL
    AND person_id != ancestor_person_id
) AS 'ERROR: Root nodes must be their own ancestors';

-- 4. All person_ids exist in PEOPLE table
ASSERT (
    SELECT COUNT(*) = 0
    FROM PERSON_HIERARCHY ph
    WHERE NOT EXISTS (
        SELECT 1 
        FROM PEOPLE p 
        WHERE p.person_id = ph.person_id
    )
) AS 'ERROR: Found person_ids that dont exist in PEOPLE table';

COMMIT;

-- Show results if all assertions pass
SELECT * 
FROM PERSON_HIERARCHY 
ORDER BY person_id;