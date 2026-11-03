-- =============================================================================
-- SQL View: vw_powerbi_defects
-- Tujuan: Memudahkan konsumsi data shopfloor langsung oleh PowerBI Desktop / Metabase
--         tanpa perlu melakukan relasi manual di PowerBI Data Modeling.
-- =============================================================================

CREATE OR REPLACE VIEW vw_powerbi_defects AS
SELECT
    l.id AS log_id,
    l.logged_at AS timestamp_recorded,
    CAST(l.logged_at AS DATE) AS log_date,
    TO_CHAR(l.logged_at, 'HH24:MI') AS log_time,
    l.shift,
    CASE 
        WHEN l.shift = 1 THEN 'Shift 1 (Pagi)'
        WHEN l.shift = 2 THEN 'Shift 2 (Sore)'
        WHEN l.shift = 3 THEN 'Shift 3 (Malam)'
        ELSE 'Unknown Shift'
    END AS shift_name,
    
    -- Line Master Info
    ln.code AS line_code,
    ln.name AS line_name,
    ln.section AS line_section,
    
    -- Harness Part Master Info
    hp.part_number,
    hp.car_model,
    hp.description AS part_description,
    
    -- Defect Category Master Info
    dc.code AS defect_code,
    dc.name AS defect_name,
    dc.section AS defect_section,
    dc.severity AS defect_severity,
    
    -- Disposition & Quantities
    l.action_taken AS disposition,
    l.quantity,
    CASE WHEN l.action_taken = 'SCRAP' THEN l.quantity ELSE 0 END AS scrap_quantity,
    CASE WHEN l.action_taken = 'REWORK' THEN l.quantity ELSE 0 END AS rework_quantity,
    
    -- QC Operator & Notes
    l.inspector_name,
    l.notes
FROM tracking_defectlog l
JOIN tracking_line ln ON l.line_id = ln.id
JOIN tracking_harnesspart hp ON l.harness_part_id = hp.id
JOIN tracking_defectcategory dc ON l.defect_category_id = dc.id;

-- Beri hak akses SELECT ke sai_user jika diperlukan
GRANT SELECT ON vw_powerbi_defects TO sai_user;
