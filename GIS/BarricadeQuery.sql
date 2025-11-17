(
    Barricade_Date IS NOT NULL
  AND Barricade_PickUpDate IS NULL
)
OR (
  RollIn_Status IN ('Open', 'In Progress')
)
OR (
  INCIDENT_TYPE_ID IN (29747, 29748)
  AND Barricade_PickUpDate IS NULL
)